from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.audio import SoundLoader

class AudioPlayer():

    def __init__(self):
        self.sound = SoundLoader.load("../Assets/Audio/bwu.mp3")
        self.playing = False
    
    def playerBTN(self, xPos=0.5, yPos=0.3):    
        self.button = MDRectangleFlatButton(text='>', pos_hint={
                                    'center_x': xPos, 'center_y': yPos},
                                    on_release=lambda btn: self.btnfunc(btn))
        return self.button

    def btnfunc(self, obj):

        if not self.playing:
            self.sound.play()
            self.playing = True
            self.button.text = '||'
        else:
            self.sound.stop()
            self.playing = False
            self.button.text = '>'