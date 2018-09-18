'''
Created on Aug 4, 2018

@author: wouters
'''
from components.VideoSlideshow import VideoSlideshow
from components.VideoLabel import VideoLabel
from components.VideoPhotoPreview import VideoPhotoPreview

class VideoInterface(object):
    '''
    classdocs
    '''
    _isRunning = False
    _height = 0
    _width = 0
    _camera = 0
    _picture_overlay = 0

    _lastname = 0
    _videoSlideshow = 0
    _videoLabel = 0
    _videoPhotoPreview = 0
    
    def getSlideshowInterface(self):
        return self._videoSlideshow    
    
    def __init__(self, camera = 0, framerate = 32, width = 1920, height = 1080):
        ''' Constructor. '''
        
        self._frameRateSet = framerate  
        self._width = width
        self._height = height
        self._camera = camera
        
        self._videoLabel = VideoLabel(camera) # used for showing labels on the screen
        self._videoSlideshow = VideoSlideshow(self._picture_overlay, camera, self._videoLabel)  # used for slideshow display
        self._videoPhotoPreview = VideoPhotoPreview(self._picture_overlay, self._videoSlideshow, self._videoLabel, camera) # used for fullscreen preview when photo is made
                
    def setDefaults(self):
        self._videoPhotoPreview.buildHeader()
        self._videoLabel.setDefault()
                                

    def startPreview(self):
        self._camera.resolution = (self._width, self._height)       
        self._camera.framerate = self._frameRateSet      
        self._camera.start_preview(fullscreen=False, window=(150,250,1000,750),hflip=True)

    def stopPreview(self):
        self._camera.stop_preview()          

    def start(self):        
        self._isRunning = True
        self._videoLabel.setDefault()
        self._videoPhotoPreview.buildHeader()
        self.startPreview()
        
    def setTitle(self, text):
        self._videoLabel.setTitle(text)
        
    def hideLabels(self):
        self._videoLabel.hide()
        
    def showPhoto(self, name):
        self._videoPhotoPreview.show_picture(name)
        
    def hidePhoto(self):
        self._videoPhotoPreview.hide_picture()
        self.setDefaults()                            
