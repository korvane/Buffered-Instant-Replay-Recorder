LIVE BUFFER VIDEO RECORDER


in the integrated terminal:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser     #allow scripts to run
python -m venv myvenv                                   #create virtual environment
.\myvenv\Scripts\activate                               #activate scripts
pip install opencv-python                               #install OpenCV.
pip install numpy                                       #install numpy
pip install screeninfo                                  #install screeninfo


The file structure is organized by day. Each day contains a livestream recording and its corresponding clips.


CONTROLS:
"move forward/back 100 frames" is 'o' and 'p'

"step forward/back 1 frame" is ',' and '.'

"pause" is space

"jump to live" is return

"clip" is c. 
-clip takes roughly 5 seconds before and 5 seconds after.