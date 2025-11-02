LIVE BUFFER VIDEO RECORDER
-A Python application for live video capture with instant replay functionality


in the integrated terminal (otherwise program wont run):

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser    
python -m venv myvenv                                   
.\myvenv\Scripts\activate                               
pip install opencv-python                               
pip install numpy                                       
pip install screeninfo                                  

#allow scripts to run
#create virtual environment
#activate scripts
#install OpenCV.
#install numpy
#install screeninfo

The file structure is organized by day. Each day contains a livestream recording and its corresponding clips.


CONTROLS:
"move forward/back 100 frames" is 'o' and 'p'

"step forward/back 1 frame" is ',' and '.'

"pause" is space

"jump to live" is return

"clip" is c. 
-clip takes roughly 5 seconds before and 5 seconds after.
