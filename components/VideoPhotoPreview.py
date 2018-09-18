from PIL import Image


class VideoPhotoPreview(object):
    _overlay = 0
    _overlayHeader = 0
    _camera = 0
    _videoLabel = 0
    _videoSlideshow = 0
    
    def __init__(self, overlayPicture, videoSlideshow, videoLabel, camera):
        self._overlay = overlayPicture
        self._videoLabel = videoLabel
        self._videoSlideshow = videoSlideshow
        self._camera = camera
        print "init"
        
    def show_picture(self, name):
        if(self._overlayHeader is not 0):
            self._camera.remove_overlay(self._overlayHeader)        
        self._videoLabel.hide()
        self._videoSlideshow.hide()
        self.build_picture(name)

    def hide_picture(self):
        self._overlayHeader = 0
        if(self._overlay is not 0):
            self._camera.remove_overlay(self._overlay)
        self._overlay = 0
  
    def buildHeader(self):
        img = Image.open('/home/pi/recorder/rec/header.png')

        pad = Image.new('RGBA', (
            ((1280 + 31) // 32) * 32,
            ((1024 + 15) // 16) * 16,
            ))
        # Paste the original image into the padded one
        pad.paste(img, (0, 0))

        if self._overlayHeader is 0:
            self._overlayHeader = self._camera.add_overlay(pad.tobytes(), size=pad.size, window=(0,0-200,1080,668))
        else:
            self._overlayHeader.update(pad.tobytes())

        self._overlayHeader.alpha = 255
        self._overlayHeader.layer = 5

    def build_picture(self, name):
        img = Image.open(name) #.transpose(Image.FLIP_LEFT_RIGHT)
        pad = Image.new('RGB', (
            ((1280 + 31) // 32) * 32,
            ((1024 + 15) // 16) * 16,
            ))
        img = img.resize((1280,1024), Image.ANTIALIAS)
        pad.paste(img, (0, 0))

        if self._overlay is 0:
            self._overlay = self._camera.add_overlay(pad.tobytes(), size=pad.size, window=(0,0-200,1080,668))
        else:
            self._overlay.update(pad.tobytes())

        img.close()
        pad.close()
        self._overlay.alpha = 255
        self._overlay.layer = 2

