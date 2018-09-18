'''
Created on Aug 4, 2018

@author: wouters
'''
import pyaudio
import wave
import threading
import time
import os
globalaudio = pyaudio.PyAudio()

class AudioRecorder():


    # Audio class based on pyAudio and Wave
    def __init__(self):
        global globalaudio
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        self.audio = globalaudio
        self.recording = False
        info = globalaudio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        dev = []
        for i in range(0, numdevices):
                if (globalaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    name = globalaudio.get_device_info_by_host_api_device_index(0, i).get('name')
                    if("default" not in name):
                        dev.append(name)
                    print "Input Device id ", i, " - ", globalaudio.get_device_info_by_host_api_device_index(0, i).get('name')
        if(len(dev) == 0):
            os._exit(1)

        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.ssize = self.audio.get_sample_size(self.format)
        self.audio_frames = []
        self.stream.start_stream()
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

    def __del__(self):
        self.open = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    # Audio starts being recorded
    def record(self):
        #self.audio_frames = []
        #self.stream.start_stream()
        while(self.open == True):
            try:
                data = self.stream.read(self.frames_per_buffer) 
            except:
                os._exit(1)
            if(self.recording is True):
                self.audio_frames.append(data)

            if self.open==False:
                break


    # Finishes the audio recording therefore the thread too    
    def stop(self):
        if self.open==True:
            print "Stopping AudioRecorder" 
            time.sleep(0.3)   
            self.recording = False    
            waveFile = wave.open(self.audio_filename + ".mp3", 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.ssize)
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()
            
            #self.stream.stop_stream()

    # Launches the audio recording function using a thread
    def start(self, name):
        self.audio_filename = name
        self.audio_frames = []
        self.recording = True

