import os
import time
import sys

if(len(sys.argv) is 1):
    path="/home/pi/storage/"
else:
    path=sys.argv[1]

try:
    arr=[]
    for filename in os.listdir(path):
        if("2018-09" in filename):
            arr.append(filename)
    
    for f in arr:
        filen = os.path.splitext(f)[0]
        if(("%s.h264" % filen) in arr) and (("%s.mp3" % filen) in arr and ("%s.mp4" % filen) not in arr):
            if(("%s.h264" % filen) == f):
                time.sleep(1)
                os.system("ffmpeg -i %s -i %s -c:v copy -c:a aac -strict experimental %s" % (path + f, path + filen + ".mp3", path + filen + ".mp4"))
                os.system("rm %s %s" % (path + filen + ".mp3", path + f))
except:
    print "d"