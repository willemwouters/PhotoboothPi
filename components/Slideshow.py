'''
Created on Aug 10, 2018

@author: wouters
'''

import os
import random

class Slideshow(object):
    '''
    classdocs
    '''
    _slideshowInterface = 0
    _videoInterface = 0
    
    _path = 0
    _isStopped = True
    _random = True
    _currentIndex = 0
    _filelist = 0

    def __init__(self, videoInterface, path):
        '''
        Constructor
        '''
        self._slideshowInterface = videoInterface.getSlideshowInterface()
        self._videoInterface = videoInterface
        self._path = path      
        print ("constructor called \r\n")

    def stop(self):
        print "Stopping Buttonretreiver"     
        self._slideshowInterface.hide()
        self._videoInterface.setDefaults() 
        self._videoInterface.startPreview() 
              
    def start(self, r = True):
        self._random = r
        self._currentIndex = 0
        self._videoInterface.stopPreview() 
        
        self._filelist = [s for s in os.listdir(self._path) if s.endswith('.jpeg')]  
        if(len(self._filelist) == 0):
            return False

        self._filelist.reverse()
        if(self._random is True):    
            self._currentIndex = random.randrange(0, len(self._filelist))

        self._slideshowInterface.show_slideshow("%s%s" % (self._path, self._filelist[self._currentIndex]), r)
        return True
       
    def next(self):     
        if(len(self._filelist) < 2): #nuffin to do
            return False

            if(self._random is True):       
                n = random.randrange(0, len(self._filelist))
            while(n == self._currentIndex):
                n = random.randrange(0, len(self._filelist))

            self._currentIndex = n
        else:
            self._currentIndex = self._currentIndex + 1
            if(self._currentIndex >= len(self._filelist)):
                self._currentIndex = 0

        self._slideshowInterface.next_slideshow("%s%s" % (self._path, self._filelist[self._currentIndex]))


    
    
