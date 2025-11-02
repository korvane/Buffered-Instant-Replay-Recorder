LIVE BUFFER VIDEO RECORDER
-A Python application for live video capture with instant replay functionality

HOW TO USE: 
Plug in a secondary monitor(optional). The replay will display on this monitor, otherwise it will be on the main screen.
A webcam is required to work. If you have multiple webcams, they can be cycled through with '\'.
Instructions on how to piece through the replays are below.

in the integrated terminal (otherwise program wont run):

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser    
python -m venv myvenv                                   
.\myvenv\Scripts\activate                               
pip install opencv-python                               
pip install numpy                                       
pip install screeninfo                                  

command functions:
1. allow scripts to run
2. create virtual environment
3. activate scripts
4. install OpenCV.
5. install numpy
6. install screeninfo

The file structure is organized by day. Each day contains a livestream recording and its corresponding clips.


CONTROLS:
"move forward/back 5 seconds" is 'o' and 'p'

"step forward/back 1 frame" is ',' and '.'

"pause" is space

"jump to live" is return

"clip" is c. 
-clip takes roughly 5 seconds before and 5 seconds after.

"cycle webcams" is '\'
