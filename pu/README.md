# Prosperous Universe Shipping Ad Alert

## How to use
### Open DevTools in APEX
In the game press F12 to show the DevTools window.  
The open console, either by clicking on the tab with that name or by pressing `CTRL + '`
### Method 1
Copy the js source code and paste on console.
### Method 2
Use this code that will read the plugin directly from github:
```
var script = document.createElement('script');
script.src = "https://github.com/pemn/mods/blob/master/pu/ascw.js?raw=true"
document.head.appendChild(script);
```
## How to use
The game must be in a screen that shows shipping contracts in the LMs you are interested in. Preferably only the shipping contrats (no sell and buy).
## Stop
To stop the watcher enter:  
`ASCW.stop()`  
To start again:  
`ASCW.loop()`  
