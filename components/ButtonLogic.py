'''
Created on Aug 10, 2018

@author: wouters
'''
from components import ButtonRetreiver
import threading

AUDIODEVICE = "hw:0,0"
MRL = ""

import sched, time


class ButtonLogic(object):
    '''
    classdocs
    '''

    _ledcallback = 0
    _labelupdatecallback = 0
    _dophotocallback = 0
    _dovideostartcallback = 0
    _dophotocallbackstart = 0
    _dovideoprestartclb = 0
    _slideshow = 0
    _slideshowrunning = False
    _delaystartcounter = 0
    enableslideshowtimeoutstart = True
    ignorenext = False
    btn = 0
    running = False
    
    def __init__(self,  labelupdatecallback, videoprestartclb, dovideostartcallback, dovideostopcallback, dophotocallbackstart, dophotocallback, slideshow):
        '''
        Constructor
        '''
        self._dovideostartcallback = dovideostartcallback
        self._dovideostopcallback = dovideostopcallback
        self._dophotocallback = dophotocallback
        self._labelupdatecallback = labelupdatecallback
        self.btn = ButtonRetreiver.ButtonRetreiver(self.serialcallback)
        self._dophotocallbackstart = dophotocallbackstart
        self._dovideoprestartclb = videoprestartclb
        self._slideshow = slideshow
        self.manualslideshow = True
        self.enableslideshowtimeoutstart = True

    def triggervideotimer(self):
        self._dovideostartcallback()
        self.countdownStart(15, self._dovideostopcallback, 2, True, True)

    def start(self):
        self.btn.start()
        
    def stop(self):
        self.btn.stop()


    def videopressed(self):
        if(self._slideshowrunning  is True):
            self._slideshow.stop()
            self._slideshowrunning = False
            self._delaystartcounter  = 0
            self.setButtonsEqual(0)
            self.setFrequency(40,1)
            self.setFrequency(40,2)
            return

        self._dovideoprestartclb()      
        self._delaystartcounter = -4
        self.countdownStart(3, self.triggervideotimer, 2, False)

    def photopressed(self):
        if(self._slideshowrunning  is True and self.manualslideshow is False):
            self._slideshow.stop()
            self._slideshowrunning = False
            self._delaystartcounter  = 0
            self.setButtonsEqual(0)
            self.setFrequency(40,1)
            self.setFrequency(40,2)
            return

        if(self._slideshowrunning  is True and self.manualslideshow is True):
            self._slideshow.next() 
            return  
        self._dophotocallbackstart()
        self._delaystartcounter = 0
        self.countdownStart(3, self._dophotocallback, 1)

    def doublepressed(self):
        self.ignorenext = True
        if(self._slideshowrunning  is False):
            self.manualslideshow = True
            r = self._slideshow.start(False) # not random
            if(r is True):
                self._slideshowrunning = True
                self.setButtonsEqual(1)

    def buttontimeout(self):
        if(self.enableslideshowtimeoutstart is True):
            if(self._slideshowrunning  is False):
                self._delaystartcounter = self._delaystartcounter + 1
                if(self._delaystartcounter > 8):
                    r = self._slideshow.start(True) # random
                    if(r is False):  # failed to start, 
                        return
                    self.setButtonsEqual(1)
                    self.setFrequency(50,1)
                    self.setFrequency(50,2)
                    self._slideshowrunning = True
            else:
                    self._slideshow.next() 

    def serialcallback(self, data): 
        if(self.ignorenext is True):
            self.ignorenext = False
            return

        if (data is "C"):
            self.doublepressed()


        if (data is "S"):
            self.buttontimeout()

        if self.running is False:
            if (data is "A"):
                self.photopressed()

            if (data is "B"):
                self.videopressed()

        else:
            self.btn.flush()
                    
    def setFrequency(self, freq, led):
        self.btn.setFrequency(freq, led)
        self.btn.flush()
     
    def enableLight(self, state):
        self.btn.enableLight(state)
        self.btn.flush()
    
    def setButtonsEqual(self, state):
        self.btn.setButtonsEqual(state)
        self.btn.flush()
        
    def getdefaultlabel(self):
        return ('Welkom op de bruiloft van Suzanne en Willem!')
                   
    def displayCountdown(self, buttonled, final, callback):      
        text = ""
        timeshow = 1
        if(final is True and buttonled is 2):  
            text = "Recording "

        if(final is False and buttonled is 2):  
            text = "Get ready in "

        if(final is True and buttonled is 1):  
            text = "Picture in "

        self.setFrequency(self.countdown+1*1,buttonled)

        if (self.countdown < 5 and buttonled is 2 and final is True):  # 
            text = "Hurry! "  
 
        if (self.countdown == 1 and final is True and buttonled is 1): # photo
            text = "Say Cheese!"
            timeshow = 0


        if (self.countdown <= 0 ):
            callback()
            
            if(final is True):
                self.running = False
                self._labelupdatecallback(self.getdefaultlabel())
            return False

        if(timeshow is 1):
            self._labelupdatecallback('%s%s' % (text, str(self.countdown)))
        else:
            self._labelupdatecallback('%s%s' % ("", text))

        self.countdown = self.countdown - 1
        threading.Timer(1, self.displayCountdown, [buttonled, final, callback]).start()
        return True

    def countdownStart(self, amount, callback, buttonled, final=True, forcestart=False):
        if self.running is True and forcestart is False:
            return False
        self.running = True
        self.countdown = amount
        threading.Timer(0, self.displayCountdown, [buttonled, final, callback]).start()     
        


   

