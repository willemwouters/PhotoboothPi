import os
from pynput import keyboard

from components import Photobooth

path="/home/pi/storage/"
if(os.path.isdir("/media/usb0/storage/")):
    path="/media/usb0/storage/"

photo = Photobooth.Photobooth(path)
photo.start()

def quitt():
    photo.stop()
    print "stop"
    os._exit(0)

def on_press(key):
    print('Key {} pressed.'.format(key))
    #quitt()

def on_release(key):
    global photo
    print('Key {} released.'.format(key))
    if str(key) == "u'p'":
	photo.dophoto()
 
    if str(key) == "u'v'":
	photo.dovideo()
 
    if str(key) == 'Key.esc':
        print('Exiting...')
	quitt()
 



with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()

#


