#!python
# minimal tk app to display a image

import tkinter as tk
import PIL.Image, PIL.ImageTk

class Splash(tk.Canvas):
  def __init__(self, fn = 'splash.png', timeout = 3000):
    super().__init__()
    
    self.image = PIL.ImageTk.PhotoImage(PIL.Image.open(fn))
    self.master.overrideredirect(True)
    image_w = self.image.width()
    image_h = self.image.height()
    self['height'] = image_h
    self['width'] = image_w
    pos_x = (self.winfo_screenwidth() - image_w) * 0.5
    pos_y = (self.winfo_screenheight() - image_h) * 0.5
    self.master.geometry("%dx%d+%d+%d" % (image_w, image_h, pos_x, pos_y))
    self.create_image(0, 0, anchor=tk.NW, image=self.image)
    self.create_text(image_w * 0.5, image_h * 0.5, text='⚫')
    self.place(x=0, y=0)

    self.bind('<1>', lambda event: self.quit())

    self.master.attributes("-topmost", True)

    if timeout:
      self.after(timeout, self.quit)

def show_splash(fn):
  print("show_splash", fn)
  import multiprocess
  multiprocess.Process(None, lambda fn: Splash(fn).mainloop(), None, (fn,)).start()

def crop_image(fn, box, output):
  im = PIL.Image.open(fn)
  print("%s x %s" % (im.width, im.height))
  if isinstance(box, str):
    box = list(map(int, box.split(',')))
    box[2] += box[0]
    box[3] += box[1]
  im = im.crop(box)
  print("%s x %s" % (im.width, im.height))
  im.save(output)

def compare_image(fn1, fn2):
  import matplotlib.pyplot as plt
  import numpy as np
  im1 = PIL.Image.open(fn1)
  im2 = PIL.Image.open(fn2)
  im1d = np.asarray(im1)
  im2d = np.asarray(im2)
  print(im1d)
  print(im2d)
  # for d in range(min(len(im1d), len(im2d))):
  #   im3d.append(d)
  # im3 = PIL.Image.
  # print(im1.getdata() - im2.getdata())
  # print(im3d)
  plt.subplot(221)
  plt.imshow(im1d)
  plt.subplot(222)
  plt.imshow(im2d)
  plt.subplot(223)
  plt.imshow(im1d - im2d)
  plt.subplot(224)
  plt.imshow(im2d - im1d)
  plt.tight_layout(0.2)
  plt.show()

def main():
  import sys
  print(len(sys.argv))
  if len(sys.argv) >= 4:
    crop_image(sys.argv[1], sys.argv[2], sys.argv[3])
    Splash(sys.argv[3]).mainloop()
  elif len(sys.argv) >= 3:
    compare_image(sys.argv[1], sys.argv[2])
  elif len(sys.argv) > 1:
    Splash(sys.argv[1]).mainloop()
  else:
    Splash().mainloop()

if __name__ == "__main__":
  main()
  
