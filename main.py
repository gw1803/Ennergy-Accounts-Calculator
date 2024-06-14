from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class Inicio(Screen):
    pass

class RealizarCalculo(Screen):
    pass 
    
class WindowManager(ScreenManager):
    pass


class main(MDApp):
    def build(self):
        Window.clearcolor = "#D6E68A"
        Window.size = (375,700)
        return Builder.load_file('front-end.kv')

if __name__ == '__main__':
    main().run()