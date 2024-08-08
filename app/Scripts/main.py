from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from audio_player import AudioPlayer

class Demo(MDApp):
    def build(self):
        screen = MDScreen()
        player = AudioPlayer()

        label = MDLabel(text="HI MUM!", halign='center', theme_text_color='Custom', text_color='black', font_style='Caption')
        name = MDTextField(text="Enter name", pos_hint={
                                'center_x': 0.8, 'center_y': 0.8},
                                size_hint_x=None, width=100)
                
        # defining Button with all the parameters
        btn = player.playerBTN()
        # adding widgets to screen
        screen.add_widget(name)
        screen.add_widget(btn)
        screen.add_widget(label)
        # returning the screen
        return screen
    


if __name__ == '__main__':
    Demo().run()