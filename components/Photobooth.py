from components import VideoInterface
from components import AudioRecorder
from components import Slideshow
from components import ButtonLogic
from picamera import PiCamera
import time
import datetime
import os
from compress import path

class Photobooth(object):

    audiorecorder = AudioRecorder.AudioRecorder()
    camera = PiCamera()
    btnLogic = 0
    videoInterface = 0
    slideshow = 0
    _path = 0
    
    def __init__(self, path):
        self._path = path
        self.videoInterface = VideoInterface.VideoInterface(self.camera, 25, 1000, 750)
        self.slideshow = Slideshow.Slideshow(self.videoInterface, self._path)
        self.btnLogic = ButtonLogic.ButtonLogic(self.setlabelclb, self.videoprestartclb, self.videostartclb, self.videostopclb,  self.photoclbstart, self.photoclb, self.slideshow)
                   
    def start(self):
        self.btnLogic.start()    
        self.videoInterface.start()
                
    def stop(self):
        try:
            self.audiorecorder.stop()
        except:
            print "oops"
        try:
            self.videoInterface.stop()
        except:
            print "oops"
        self.btnLogic.stop()
                  
    def dophoto(self):
        self.btnLogic.photopressed()

    def dovideo(self):
        self.btnLogic.videopressed()
                  
    def photoclbstart(self): # photo button pressed
        self.camera.resolution =  (3200, 2400) #(3280, 2464) # (1920, 1080) #(640, 480)  
        self.videoInterface.hideLabels()
        self.btnLogic.enableLight(1)        
        self.btnLogic.setFrequency(99,1)
        self.btnLogic.setFrequency(0,2)
    
    def photoclb(self):  # 3 seconds over, make photo
        filen = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        f = '%s%s.jpg' % (self._path, filen)
        ft = '%s%s.jpeg' % (self._path, filen)
        self.camera.capture(f, format='jpeg')
        self.btnLogic.setFrequency(40,1)
        self.btnLogic.setFrequency(40,2)
        self.videoInterface.setTitle("")
        self.videoInterface.stopPreview()
        os.system("ffmpeg -i %s -vf scale=1280:1024 %s" % (f, ft))
        self.btnLogic.enableLight(0)        
        self.videoInterface.showPhoto('%s%s.jpeg' % (self._path, filen))
        time.sleep(3)
        self.videoInterface.hidePhoto()
        self.btnLogic.setButtonsEqual(0)
        self.videoInterface.startPreview() # reset default preview settings
        self.videoInterface.setDefaults()
    
    def videoprestartclb(self): # video button pressed
        print "start"
        self.camera.stop_preview()
        self.camera.resolution = (1640, 922) # (1920, 1080) #(640, 480)  
        self.camera.start_preview(fullscreen=False, window=(120,300,1080,562),hflip=True)
        self.btnLogic.enableLight(1)
        self.btnLogic.setFrequency(0,1)
        self.btnLogic.setFrequency(99,2)
        self.videoInterface.hideLabels()
    
    def videostartclb(self): # 3 seconds countdown done, start video recorder

        self.camera.stop_preview()
        self.camera.start_preview(fullscreen=False, window=(120,300,1080,562),hflip=True)
        filen = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.camera.start_recording('%s%s.h264' % (self._path, filen))
        self.audiorecorder.start("%s%s" % (self._path, filen))
        
    def videostopclb(self): # 15 seconds countdown done, stop video recorder
        self.btnLogic.setFrequency(40,1)
        self.btnLogic.setFrequency(40,2)
        self.btnLogic.setButtonsEqual(0)
        self.camera.stop_recording()
        try:
            self.audiorecorder.stop()   
        except:
            print 'e'
    
        print "videoclbstop"    
        try:
            self.videoInterface.stopPreview()
            self.videoInterface.startPreview() # reset default preview settings
        except:
            print 'e'
    
        self.videoInterface.setDefaults()
        os.system("/home/pi/recorder/rec/compress.sh " + self._path)
        self.btnLogic.enableLight(0)
    
    def setlabelclb(self, data):
        self.videoInterface.setTitle(data)
        print(data)
