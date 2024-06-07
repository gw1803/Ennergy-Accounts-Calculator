from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('front-end.kv')
Window.size = (500,700)

class Inicio(Widget):
    pass

class main(App):
    def build(self):
        Window.clearcolor = "#ffffff"
        return Inicio()

if __name__ == '__main__':
    main().run()