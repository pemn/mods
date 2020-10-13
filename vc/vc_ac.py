#!python

import os
import time
import threading
import keyboard
import mouse
import pyautogui
import pyscreeze
import numpy as np
import ctypes
import winsound

# how much of the screen each hotspot snapshot will capture
region_proportion = 0.5

def screen_size():
    """Returns the width and height of the screen as a two-integer tuple.

    Returns:
      (width, height) tuple of the screen size, in pixels.
    """
    return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

def screen_snap(proportion):
  full = screen_size()
  size = np.multiply(full, proportion)
  snap = np.subtract(mouse.get_position(), np.multiply(size, 0.5))
  # bound the origin to the corners of actual screen
  return np.concatenate([np.min([np.max([snap, [0,0]], 0), np.subtract(full,size)], 0), size])

def save_region(fp = None, proportion = None, show = True):
  print(mouse.get_position())
  bbox = None
  if proportion == 1:
    pass
  elif proportion is not None:
    print("save_region snap")
    bbox = screen_snap(proportion)
  else:
    print("save_region move")
    # capture all mouse movement until user presses a button
    rec = mouse.record(button=mouse.LEFT, target_types=(mouse.DOWN,))
    if len(rec) < 2:
      print("remove", fp)
      os.remove(fp)
      return
    # calculate the bounding box where the mouse moved
    bbox = [o(getattr(_, d) for _ in rec if isinstance(_, mouse.MoveEvent)) for o in [min, max] for d in ['x', 'y']]
    # convert bounding box to top,left,height,wight
    bbox[0] = max(0, bbox[0])
    bbox[1] = max(0, bbox[1])
    bbox[2] = max(1, bbox[2] - bbox[0])
    bbox[3] = max(1, bbox[3] - bbox[1])
  print(bbox)
  # capture the region
  if bbox is None:
    im = pyscreeze.screenshot()
  else:
    im = pyscreeze.screenshot(region=bbox)
  if fp is None:
    fp = '%d.png' % time.time()
  im.save(fp)
  print("saved", fp)
  if show:
    from tksplash import show_splash
    show_splash(fp)

def click_target(key = None, target = None):
  print('click_target', target)
  if isinstance(target, str) and os.path.isfile(target):
    point = pyautogui.locateCenterOnScreen(target)
  else:
    point = target
  if point:
    mouse.move(*point, True, 0.2)
    if key:
      keyboard.send(key)
    else:
      mouse.click()
    return True
    
  return False
  
class Step(dict):
  def __init__(self, spot, next, wait = 1, back = None):
    super().__init__(self)
    self['spot'] = spot
    self['next'] = next
    self['wait'] = wait
    self['back'] = back

  @property
  def next(self):
    return self['next']
  @property
  def wait(self):
    return self['wait']
  @property
  def back(self):
    return self['back']  
  @property
  def spot(self):
    return self['spot']
    
class Watcher(threading.Thread):
  _hotkey = []
  _worker = None
  def __init__(self, args=None):
    super().__init__(args=args, daemon = False)
    self._signal = threading.Event()
    self._hotkey.append(keyboard.add_hotkey('windows+c', save_region, (None, region_proportion)))
    self._hotkey.append(keyboard.add_hotkey('windows+o', save_region, (None, 1, False)))
    self._hotkey.append(keyboard.add_hotkey('windows+j', save_region))
    self._hotkey.append(keyboard.add_hotkey('windows+esc', self.stop))
    self._hotkey.append(keyboard.add_hotkey('windows+z', self.enable))
  
  def __del__(self):
    for _ in self._hotkey:
      keyboard.remove_hotkey(_)

  def run(self):
    print("run")
    self._signal.wait()

  def stop(self):
    print("stop")
    self._signal.set()

  def enable(self):
    print("enable")
    if self._worker and self._worker.is_alive():
      self._worker.stop()
    else:
      self._worker = Worker(args=self._args)
      self._worker.start()

class Worker(threading.Thread):
  _detail = None
  _active = False
  _signal = None
  def run(self):
    print("worker run")
    print(self._args)
    self._signal = threading.Event()
    if self.play():
      winsound.Beep(3000, 500)
      winsound.Beep(3000, 500)
      winsound.Beep(3000, 500)
    else:
      winsound.Beep(500, 500)
      winsound.Beep(500, 500)
      winsound.Beep(500, 500)

    # while not self._signal.is_set():
      # if self.play():
        # winsound.Beep(3000, 500)
      # else:
        # winsound.Beep(500, 500)
        # break

  def wait(self, duration = 1):
    while duration > 0:
      time.sleep(1)
      if self._signal.is_set():
        return False
      duration -= 1
    return True

  def stop(self):
    self._signal.set()

  def play(self):
    print("play")
    winsound.Beep(1000, 100)
    if len(self._args) > 1:
      print(self._args[1])
      if self._args[1] == 'battle':
        return self.play_battle()
      if self._args[1] == 'single':
        return self.play_single()
      if self._args[1] == 'time':
        return self.play_time()
    else:
      return self.play_multi()
      
  def play_multi(self):
    # chat
    steps = {}
    steps['vc_multi'] =  Step('vc_multi.png', 'vc_start', 1, 'vc_retry')
    steps['vc_start'] =  Step('vc_start.png', 'vc_retry', 1, 'vc_retry')
    steps['vc_retry'] =  Step('vc_retry.png', 'vc_menu', 9)
    steps['vc_menu'] =  Step('vc_menu.png', 'vc_nosta', 1, None)
    steps['vc_nosta'] =  Step('vc_nosta.png', None, 1, 'vc_retry')

    step = 'vc_multi'
    while step is not None and self.wait(1):
      print("# step", step)
      self.wait(steps[step].wait)
      if click_target(None, steps[step].spot):
        print("# next")
        step = steps[step].next
      elif steps[step].back is not None:
        print("# back")
        step = steps[step].back
      else:
        print("# same")

    print("play end")
    return True


  def play_time(self):
    print("play time")

    # chat
    steps = {}
    steps['vc_retry'] =  Step('vc_retry_escort.png', 'vc_confirm', 9, 'vc_retry_gray')
    steps['vc_confirm'] =  Step('vc_confirm.png', 'vc_retry_gray', 1)
    steps['vc_retry_gray'] =  Step('vc_retry_gray.png', None, 1, 'vc_retry')

    step = 'vc_retry'
    while step is not None and self.wait(1):
      print("# step", step)
      self.wait(steps[step].wait)
      if click_target(None, steps[step].spot):
        print("# next")
        step = steps[step].next
      elif steps[step].back is not None:
        print("# back")
        step = steps[step].back
      else:
        print("# same")

    print("play end")
    return True


  def play_battle(self):
    # chat
    steps = {}
    steps['vc_retry'] =  Step('vc_retry.png', 'vc_menu', 9)
    steps['vc_menu'] =  Step('vc_menu.png', 'vc_nosta', 1, None)
    steps['vc_nosta'] =  Step('vc_nosta.png', None, 1, 'vc_battle')
    steps['vc_battle'] =  Step('vc_battle.png', 'vc_ok', 5)
    steps['vc_ok'] =  Step('vc_ok.png', 'vc_retry', 1)

    step = 'vc_retry'
    while step is not None and self.wait(1):
      print("# step", step)
      self.wait(steps[step].wait)
      if click_target(None, steps[step].spot):
        print("# next")
        step = steps[step].next
      elif steps[step].back is not None:
        print("# back")
        step = steps[step].back
      else:
        print("# same")

    print("play end")
    return True

 


  def play_single(self):
    print("play single")

    # chat
    steps = {}
    steps['vc_retry'] =  Step('vc_retry.png', 'vc_menu', 9)
    steps['vc_menu'] =  Step('vc_menu.png', 'vc_nosta', 1, None)
    steps['vc_nosta'] =  Step('vc_nosta.png', None, 1, 'vc_retry')


    step = 'vc_retry'
    while step is not None and self.wait(1):
      print("# step", step)
      self.wait(steps[step].wait)
      if click_target(None, steps[step].spot):
        print("# next")
        step = steps[step].next
      elif steps[step].back is not None:
        print("# back")
        step = steps[step].back
      else:
        print("# same")

    print("play end")
    return True

 
if __name__ == '__main__':
  import sys
  print(__name__)
  w = Watcher(args=sys.argv)
  w.start()
  print("eof")
  #import pyautogui; print(pyautogui.locateCenterOnScreen('vc_1.png'))