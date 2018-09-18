from PIL import Image

class VideoSlideshow(object):
    _overlay = 0
    _camera = 0
    _lastname = 0
    def __init__(self, overlay, camera, labelInterface):
        self._overlay = overlay
        self._camera = camera
        self._labelInterface = labelInterface
        print "init"
        
    def show_slideshow(self, name, hideright = False):
        if(self._overlay is not 0):
            self._camera.remove_overlay(self._overlay)
        self._overlay = 0
        self.build_slideshow(name)

        if(hideright is False):
            self._labelInterface.setLabelRight("Next")
        else:
            self._labelInterface.setLabelRight("")
        self._labelInterface.setLabelLeft("Stop Slideshow") 
       
    def next_slideshow(self, name):
        self.build_slideshow(name)
        
    def hide(self):
        if(self._overlay is not 0):
            self._camera.remove_overlay(self._overlay)
        self._overlay = 0    
                    
    def stop_slideshow(self):
    
        if(self._overlay is not 0):
            self._camera.remove_overlay(self._overlay)
        self._overlay = 0



    def build_slideshow(self, name):
        otmp = 0
        if(self._lastname is not 0):
            img = Image.open(self._lastname)
            pad = Image.new('RGB', (
                ((1280 + 31) // 32) * 32,
                ((1024 + 15) // 16) * 16,
                ))

            img = img.resize((1000,750), Image.ANTIALIAS)
            pad.paste(img, (150, 250))
            otmp = self._camera.add_overlay(pad.tobytes(), size=pad.size, window=(0,0,1280,1024))
            pad.close()
            otmp.alpha = 255
            otmp.layer = 2
                   
        if(self._overlay is not 0):
            self._camera.remove_overlay(self._overlay)
        self._overlay = 0
                
        img = Image.open(name)
        pad = Image.new('RGB', (
            ((1280 + 31) // 32) * 32,
            ((1024 + 15) // 16) * 16,
            ))

        img = img.resize((1000,750), Image.ANTIALIAS)
        pad.paste(img, (150, 250))
        if self._overlay is 0:
            self._overlay = self._camera.add_overlay(pad.tobytes(), size=pad.size, window=(0,0,1280,1024))
        else:
            self._overlay.update(pad.tobytes())
        pad.close()
        self._overlay.alpha = 255
        self._overlay.layer = 2
        self._lastname = name
        
        if(otmp is not 0):
            self._camera.remove_overlay(otmp)

