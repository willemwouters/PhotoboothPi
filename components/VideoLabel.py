from PIL import Image, ImageDraw, ImageFont


class VideoLabel(object):
    _overlayLabelRight = 0
    _overlayLabelLeft = 0    
    _overlayTitle = 0
    _camera = 0
    
    def __init__(self, camera):
        self._camera = camera
        print "init"
        
        
    def getDefaultTitle(self):
        return ('Welkom op de bruiloft van Suzanne en Willem!')
                
    def setDefault(self):
        self.setLabelRight("Photo")
        self.setLabelLeft("Video") 
        self.setTitle(self.getDefaultTitle())         
               
    def setTitle(self, data):
        img = Image.new('RGBA', (
            ((1280 + 31) // 32) * 32,
            ((270 + 15) // 16) * 16,
            ))
       
        text = data
        draw = ImageDraw.Draw(img)
        draw.font = ImageFont.truetype("/home/pi/recorder/rec/Pacifico.ttf", 60)
        offset = 0

        if(len(text) > 20):
            offset = 70
        elif(len(text) > 10):
            offset = 500
        elif(len(text) > 7):
            offset = 550
        elif(len(text) > 5):
            offset = 580
        elif(len(text) > 1):
            offset = 590
        else:
            offset = 617

        draw.text((offset,0), text,  fill=(255,255,0,255))

        if self._overlayTitle is 0:
            self._overlayTitle=self._camera.add_overlay(img.tobytes(), fullscreen=False, layer=6, size=img.size, alpha=32, window=(0, 75,1280,270))
            self._overlayTitle.alpha = 255
        else:
            self._overlayTitle.update(img.tobytes())
        img.close()


    def setLabelLeft(self, data = "left" ):
        img = Image.new('RGBA', (
            ((1280 + 31) // 32) * 32,
            ((200 + 15) // 16) * 16,
            ))
       
        if(self._overlayLabelLeft is not 0):
            self._camera.remove_overlay(self._overlayLabelLeft)
        self._overlayLabelLeft = 0
               
        text = data
        draw = ImageDraw.Draw(img)
        draw.font = ImageFont.truetype("/home/pi/recorder/rec/Pacifico.ttf", 45)
        offset = 0


        draw.text((offset,0), text,  fill=(255,0,0,255))

        if self._overlayLabelLeft is 0:
            self._overlayLabelLeft=self._camera.add_overlay(img.tobytes(),  fullscreen=False, layer=6, size=img.size, alpha=32, window=(170,900,1280,200))
            self._overlayLabelLeft.alpha = 255
        else:
            self._overlayLabelLeft.update(img.tobytes())
        img.close()

    def setLabelRight(self, data = "right"):
        img = Image.new('RGBA', (
            ((1280 + 31) // 32) * 32,
            ((200 + 15) // 16) * 16,
            ))
        if(self._overlayLabelRight is not 0):
            self._camera.remove_overlay(self._overlayLabelRight)
        self._overlayLabelRight = 0
               
        text = data
        draw = ImageDraw.Draw(img)
        draw.font = ImageFont.truetype("/home/pi/recorder/rec/Pacifico.ttf", 45)
        offset = 0


        draw.text((offset,0), text,  fill=(0,255,0,255))

        if self._overlayLabelRight is 0:
            self._overlayLabelRight=self._camera.add_overlay(img.tobytes(), fullscreen=False, layer=6, size=img.size, alpha=32, window=(980,900,1280,200))
            self._overlayLabelRight.alpha = 255
        else:
            self._overlayLabelRight.update(img.tobytes())
        img.close()

    def hide(self):
        if(self._overlayLabelLeft is not 0):
            self._camera.remove_overlay(self._overlayLabelLeft)
        self._overlayLabelLeft = 0
        if(self._overlayLabelRight is not 0):
            self._camera.remove_overlay(self._overlayLabelRight)
        self._overlayLabelRight = 0
        

