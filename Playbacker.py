import cv2 #pip install opencv-python i think lmao (laughing my ah off)
import VideoLoop
from datetime import datetime
import os
from screeninfo import get_monitors
import time
import sounddevice
import soundfile
import subprocess
from collections import deque

def main():
    """organize monitor displaying"""
    #get highest index camera
    cameraIndex = 10
    
    live = cv2.VideoCapture(cameraIndex)
    while not live.isOpened():
        cameraIndex-=1
        live.release()
        if cameraIndex < 0:
            print('No camera found. You need a camera.')
            exit()
        live = cv2.VideoCapture(cameraIndex)

    maxCamIndex = cameraIndex+1
    os.system('cls')
    print('You have ' + str(maxCamIndex) + ' camera(s).')
    live = cv2.VideoCapture(maxCamIndex-1)
    

    monitors = get_monitors()
    two = len(monitors) > 1

    
    cv2.namedWindow('Replay', cv2.WINDOW_NORMAL)


    monx = int(monitors[0].width) - 1100 #corner
    mony = int(monitors[0].height) - 600 #corner
    if two: #replay will be on the big screen.
        cv2.namedWindow('Live Video', cv2.WINDOW_NORMAL) #create live video when monitors > 2

        cv2.moveWindow('Replay', monitors[1].x, monitors[1].y)
        cv2.setWindowProperty('Replay', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.resizeWindow('Live Video', int(monitors[0].width/3*2), int(monitors[0].height/3*2))
        cv2.moveWindow('Live Video', 0, 0)
        monx = monitors[1].width - 50
        mony = monitors[1].height - 50
    else: #replay will be windowed fullscreen if theres only 1 monitor. hide live action.
        cv2.resizeWindow('Replay', monitors[0].width, monitors[0].height)
        cv2.moveWindow('Replay', 0, 0)



    """create files"""

    os.makedirs('clips', exist_ok=True)
    pathname = "clips\\" + 'session ' + str(datetime.now().strftime('%y-%b-%d'))
    os.makedirs(pathname, exist_ok=True)
    name = str(datetime.now().strftime('%H-%M')) +' stream' + '.mp4'
    fullpath = os.path.join(pathname, name)

    #handle someone creating a new stream directly after a previous one so stuff isnt deleted
    nm=0
    while os.path.exists(fullpath):
        name =  str(datetime.now().strftime('%H-%M')) +' stream ' + str(nm) + '.mp4'
        fullpath = os.path.join(pathname,name)
        nm+=1

    tempPath = os.path.join(pathname, 'tempStream.mp4')


    #get fps of camera
    fps = live.get(cv2.CAP_PROP_FPS)
    if(fps <= 0):
        fps = 30
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    out = cv2.VideoWriter(tempPath, fourcc, fps, (int(live.get(3)),int(live.get(4)))) #write to file
    jumpSize = int(fps * 5)
    stepSize = int(1 * fps / 30)
    clipLength = int(fps * 5) #clip length 5 seconds each direction
    slomoSpeed = int(fps/10)

    """declare methods lmao (laughing my ah off)"""
    play = True
    toEnd = False 
    jumpBack5 = False
    jumpForward5 = False
    stepFore = False
    stepBack = False
    clip = False
    toggleCamera = False
    slomo = False
    playslomo = False
    divide = False

    frameCur = -1
    lbound = 0
    rbound = -1
    clipCount = 0

    videoQueue = VideoLoop.CircularQueue(int(fps * 400)) #10 minutes
    cameraCooldown = 0



    #audio
    sampleRate = 44100
    blockSize = 1456
    maxSamples = sampleRate*400
    audioBuffer = deque(maxlen=maxSamples) # this stores blocks lmao.
    # audioQueue = VideoLoop.CircularQueue(int(fps*400))

    sound_path = os.path.join(pathname, 'audio.wav')
    soundOut = soundfile.SoundFile(file=sound_path, mode='w', samplerate=sampleRate,channels=1) #fix channels

    def audio_callback(indata, frames, time_info, status):
        # print("numframes: " + str(frames))
        if status:
            print(status)
        soundOut.write(indata)
        audioBuffer.extend(indata[:,0])
    

    stream = sounddevice.InputStream(
    samplerate=sampleRate,
    channels=1,
    blocksize=blockSize, #fix block size?
    callback=audio_callback
    )
    stream.start()



    """infinite loop ran fps times per second due live.read(). """
    prev_time = time.time()
    while 1:
        ret, frame = live.read()
        if not ret: break
        #frame = cv2.flip(frame, 1)
        tim = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        dat = datetime.now().strftime("%m-%d-%Y")


        monx, mony = frame.shape[:2]
        monx = monx + 60 if monx >= 720 else monx - 300
        monx = 0
        mony = mony - 600 if mony > 640 else mony - 175
        bottom_right = (monx, mony)
        cv2.putText(frame, tim, (0,40), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2, cv2.LINE_AA) #black outline
        cv2.putText(frame, tim, (0,40), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(frame, dat, bottom_right, cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 4, cv2.LINE_AA) #black outline
        cv2.putText(frame, dat, bottom_right, cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)


        out.write(frame)
        rbound += 1
        if cameraCooldown > 0:
            cameraCooldown -= 1

        if videoQueue.isFull():
            lbound += 1
            videoQueue.dequeue()

        videoQueue.enqueue(frame)
        # audioQueue.enqueue()
        
        """ \"methods\" """
        if play:
            if slomo:
                frameCur += 1 if int(rbound%slomoSpeed) == 0 else 0
            else:
                frameCur+=1
                
        else:
            frameCur = lbound if lbound >= frameCur else frameCur #max of lbound and framecur 
            if playslomo:
                play = True
                playslomo = False

        if toEnd:
            frameCur = rbound
            if slomo:
                slomo = False
            if not play:
                play = True
            toEnd = False

        if jumpBack5:
            #go back jumpSize frames. in the actual video, stop at the back and prevent wrapping
            frameCur = lbound if lbound > frameCur - jumpSize else frameCur - jumpSize # max of lbound and (framecur-jumpsize)
            jumpBack5 = False

        if jumpForward5:
            #go forward jumpSize frames. in the actual video, stop at the front and prevent wrapping
            frameCur = rbound if rbound < frameCur + jumpSize else frameCur + jumpSize #min of rbound and (framecur+jumpsize)
            jumpForward5 = False

        if stepBack:
            #go back jumpSize frames. in the actual video, stop at the back and prevent wrapping
            frameCur = lbound if lbound > frameCur - stepSize else frameCur - stepSize
            stepBack = False

        if stepFore:
            #go forward jumpSize frames. in the actual video, stop at the front and prevent wrapping
            frameCur = rbound if rbound < frameCur + stepSize else frameCur + stepSize 
            stepFore = False

        if clip:
            strt = max(frameCur - clipLength, lbound)
            end = min(frameCur + clipLength, rbound)
            nameClip = str(datetime.now().strftime('%H-%M-%S')) + ' clip-' + str(clipCount) + '.mp4'
            fullpathClip = os.path.join(pathname, nameClip)
            tempVideoPath = os.path.join(pathname, 'tempClip.mp4')
            clipFile = cv2.VideoWriter(tempVideoPath, fourcc, fps, (int(live.get(3)),int(live.get(4))))

            tempSoundPath = os.path.join(pathname, 'tempAudio.wav')
            audioFile = soundfile.SoundFile(file=tempSoundPath, mode='w', samplerate=44100,channels=1) #fix channels

            audioStrt = int(strt/fps*sampleRate)
            audioEnd = int(end/fps*sampleRate)
            for i in range(strt, end):
                clipFile.write(videoQueue.get(i%videoQueue.maxSize))
                
            audioClip = list(audioBuffer)[audioStrt:audioEnd]
            audioFile.write(audioClip)

            # cv2.putText(frame, 'clip', (30,30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2, cv2.LINE_AA)
            print('clip ' + str(clipCount) + ' was made.')
            clipFile.release()
            audioFile.close()
            subprocess.run(['ffmpeg', #program name
                            '-y', #overwrite
                            '-i', #input file 1
                            tempVideoPath,
                            '-i', #input file 2
                            tempSoundPath, 
                            '-c:v', #codec, video only
                            'copy', #dont reencode, copy video
                            '-c:a', #codec, audio only
                            'aac', #encode with aac
                            fullpathClip]) #final location
            os.remove(tempSoundPath)
            os.remove(tempVideoPath)
            clipCount += 1
            clip = False
        
        if toggleCamera:
            if cameraCooldown <= 0 and maxCamIndex > 1:
                cameraIndex = (cameraIndex + 1) % maxCamIndex
                live.release()
                live = cv2.VideoCapture(cameraIndex)

            toggleCamera = False

        if divide:
            tmp = (rbound - lbound) * (k - 49)*.1
            if k == 48:
                tmp = rbound

            frameCur = tmp + lbound if tmp > lbound else lbound # set frame to position of number keys
            divide = False
        
            

        
        """show screen"""
        playback = videoQueue.get(frameCur % videoQueue.maxSize)
        cv2.imshow("Replay", playback)
        if two: #show only if theres 2 monitors
            cv2.imshow("Live Video", frame)


        """keybinds"""
        k = cv2.waitKeyEx(1)
        if k == 13: #enter key, toLive
            toEnd = True
        if k == ord(' '): #start/stop
            play = not play
        if k == 2424832: #left arrow doesnt work. jump backwards 5 seconds
            jumpBack5 = True
        if k == 2555904: #right arrow doesnt work. jump forwards 5 seconds
            jumpForward5 = True 
        if k == ord(','): #step backwards 2 frames
            stepBack = True
        if k == ord('.'): #step forwards 2 frames
            stepFore = True
        if k == ord('c'):
            clip = True
        if k == ord('\\'):
            toggleCamera = True
        if k == ord('q'): #escape
                break
        if k == ord('l'):
            slomo = not slomo
            if slomo and not play:
                playslomo = True
        # if k > 47 and k < 58:
        #     divide = True

        elapsed = time.time() - prev_time
        wait_time = max(0, 1/fps - elapsed)
        time.sleep(wait_time)
        prev_time = time.time()
        
    live.release()
    out.release()
    cv2.destroyAllWindows()
    soundOut.close()
    subprocess.run(['ffmpeg', '-y', '-i', tempPath, '-i', sound_path, '-c:v', 'copy', '-c:a', 'aac', fullpath])
    os.remove(sound_path) #delete sound file, make sure this is right
    os.remove(tempPath)


if __name__ == "__main__":
    main()