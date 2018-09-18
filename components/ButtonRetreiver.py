'''
Created on Aug 10, 2018

@author: wouters
'''
import serial.tools.list_ports


from threading import Thread
import time
import os
USBDEVICE = "/dev/ttyUSB0"
serial_port = 0


class ButtonRetreiver(Thread):
    '''
    classdocs
    '''
    _buttoncallback = 0
    serial_port = 0
    _serialfound = False
    firstconnect = True
    def __init__(self, buttoncallback):
        '''
        Constructor
        '''
        self._buttoncallback = buttoncallback        

                   
        print ("constructor called \r\n")
        Thread.__init__(self)
                    
        
    def handle_data(self, data):
        if "A" in data:
            self._buttoncallback("A")
    
        if "B" in data:
            self._buttoncallback("B")
    
        if "C" in data:
            self._buttoncallback("C")
    
    def stop(self):
        print "Stopping Buttonretreiver"        
        self._isRunning = False

                   
    def run(self):        
        self._isRunning = True
        print "Starting Buttonretreiver"        
        for p in serial.tools.list_ports.comports():
            print(p)

        try:
            arduino_ports = [
                p.device
                for p in serial.tools.list_ports.comports()
                if 'Serial' in p.description
            ]
            if len(arduino_ports) > 1:
                print "no ports"
                os._exit(1)
            
            self.serial_port = serial.Serial(arduino_ports[0], 115200, timeout=25)
            self._serialfound = True
        except Exception as e: 
            print(e)
            self._serialfound = False
            print ("too bad, no button \r\n")
            os._exit(1)

        while (self._serialfound is False):
            time.sleep(1)
                        
        while(self._isRunning):
            self.serial_port.flush()
            reading = 0
            try:
                reading = self.serial_port.read(2)
            except:
                os._exit(1)

            #print  (reading)
            if(len(reading) == 0):
                self._buttoncallback("S")
            #print  len(reading)
            self.handle_data(reading)
            if(self.firstconnect is True):
                self.setFrequency(40,1)
                self.setFrequency(40,2)
                self.setButtonsEqual(0)
                self.firstconnect = False

    def flush(self):
        self.serial_port.flush()

    def enableLight(self, state):
        self.serial_port.write("LIGHTSTATE=%s\n" % state)
    
    def setButtonsEqual(self, state):
        self.serial_port.write("SETEQSTATE=%s\n" % state)
    
    
    def setFrequency(self, freq, led):
        if(led == 1):
            self.serial_port.write("LED1SPEED=%s\n" % freq)
    
        if(led == 2):
            self.serial_port.write("LED2SPEED=%s\n" % freq)

    
    
