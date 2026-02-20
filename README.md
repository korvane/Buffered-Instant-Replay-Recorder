LIVE BUFFER VIDEO RECORDER
-A Python application for live video capture with instant replay functionality

HOW TO USE: 
Plug in a secondary monitor(optional). The replay will display on this monitor, otherwise it will be on the main screen.
A webcam is required to work. If you have multiple webcams, they can be cycled through with '\'.
Instructions on how to piece through the replays are below.

in the integrated terminal (otherwise program wont run):

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser    
winget install Python.Python.3.10 (do this if you dont have python 3.10, or find another way to get python 3.10)
py -3.10 -m venv myvenv
(select yes if using VS Code)
.\myvenv\Scripts\activate                               
pip install numpy opencv-python screeninfo 
repoen vscode


command functions:
1. allow scripts to run
2. install python 3.10
3. create virtual environment
4. activate scripts
5. install OpenCV, numpy, screeninfo
6. reboot vscode

The file structure is organized by day. Each day contains a livestream recording and its corresponding clips.


CONTROLS:
"move forward/back 5 seconds" is 'right arrow' and 'left arrow'.

"step forward/back 1 frame" is ',' and '.'

"pause" is space

"jump to live" is return

"clip" is c. 
-clip takes roughly 5 seconds before and 5 seconds after.

"cycle webcams" is '\' (clipping is not enabled after this)

"slo-mo" is 'l' (L)