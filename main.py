from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class Inicio(Screen):
    pass

class RealizarCalculo(Screen):
    padrao_geral = ""
    padrao_wilson = ""
    padrao_celio = ""
    valor_conta = ""
    valor_kw = ""
    taxa_iluminacao = ""

    def on_text(self, input):  
        match input:
            case self.ids.padrao_geral :
                self.padrao_geral = self.ids.padrao_geral.text
            case self.ids.padrao_wilson :
                self.padrao_wilson = self.ids.padrao_wilson.text
            case self.ids.padrao_celio :
                self.padrao_celio = self.ids.padrao_celio.text
            case self.ids.valor_conta :
                self.valor_conta = self.ids.valor_conta.text
            case self.ids.valor_kw :
                self.valor_kw = self.ids.valor_kw.text
            case self.ids.taxa_iluminacao:
                self.taxa_iluminacao = self.ids.taxa_iluminacao.text
        self.verify_inputs()
        

    def verify_inputs(self):
        if (self.padrao_geral != "" )& (self.padrao_wilson != "") & (self.padrao_celio!="") & (self.valor_conta != "") & (self.valor_kw != ""):
            self.ids.button.disabled = False
        else:
            self.ids.button.disabled = True
 
        
class WindowManager(ScreenManager):
    pass


class main(MDApp):
    def build(self):
        Window.clearcolor = "#D6E68A"
        Window.size = (375,700)
        return Builder.load_file('front-end.kv')

if __name__ == '__main__':
    main().run()