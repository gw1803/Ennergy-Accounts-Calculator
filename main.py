from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.widget import Widget

Window.size = (375,700)


class Inicio(Widget):
    ...

class main(MDApp):
    def build(self):
        Window.clearcolor = "#D6E68A"
        return Builder.load_file('front-end.kv')

if __name__ == '__main__':
    main().run()