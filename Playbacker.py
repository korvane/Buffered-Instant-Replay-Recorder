import numpy as np
import cv2 #import cv2_python i think lmao (laughing my ah off)
import tkinter as kt
import VideoLoop

live = cv2.VideoCapture("WR.mp4") 
cv2.namedWindow("Fullscreen Video", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Fullscreen Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.namedWindow("windowed", cv2.WINDOW_NORMAL)


fourcc = cv2.VideoWriter.fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(live.get(3)),int(live.get(4)))) #write to file

jumpSize = 100
toEnd = True
framez = []
frameTotal = 0
frameCur = 0
play = True
videoQueue = VideoLoop.CircularQueue(10000)

jumpBack5 = False

while 1:
    ret, frame = live.read()
    framez.append(frame)
    out.write(frame)

    if videoQueue.isFull():
        videoQueue.dequeue()
    videoQueue.enqueue(frame)
    
    if toEnd:
        frameCur = videoQueue.rear
        toEnd = False

    if play:
        frameCur+=1
        frameCur%=videoQueue.maxSize
        #frameCur = (frameCur + 1) % videoQueue.maxSize

    if jumpBack5:
        #go back 500 frames. in the actual video, stop at the back and prevent wrapping
        tmp = frameCur
        if videoQueue.isFull():
                frameCur = videoQueue.rear - jumpSize if videoQueue.rear - jumpSize >= videoQueue.rear else videoQueue.front
                print("here")
        else:
            frameCur = max(videoQueue.rear - jumpSize, 0) #stop at 0
            print("rear is " + str(videoQueue.rear) + " and jumpsize is " + str(jumpSize))
            print(videoQueue.rear-jumpSize)
            
        print("first: " + str(tmp))
        print(str(tmp-frameCur))
    jumpBack5 = False

    playback = videoQueue.get((frameCur-1) % videoQueue.maxSize)
    cv2.imshow("Fullscreen Video", frame)
    cv2.imshow("windowed", playback)
    frameTotal += 1
    k = cv2.waitKey(1)
    if k == ord('q'): #escape
        break
    if k == 13: #enter key, toLive
        toEnd = True
    if k == ord(' '): #start/stop
        play = not play
    if k == ord('o'): #left arrow doesnt work.
        jumpBack5 = True
    # if k != -1:
        #print(k)

live.release()
out.release()
cv2.destroyAllWindows()