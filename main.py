from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

class Inicio(Screen):
    pass

class RealizarCalculo(Screen):
    #values from the previous account
    padrao_geral_anterior = 31605
    padrao_wilson_anterior = 36685
    padrao_celio_anterior = 24706

    #values from the form 
    padrao_geral = ""
    padrao_wilson = ""
    padrao_celio = ""
    valor_conta = ""
    valor_kw = ""
    taxa_iluminacao = ""

    #calculated values
    valor_wilson = 0
    valor_celio = 0
    descricao = ""

    def on_text(self, input):  
        match input:
            case self.ids.padrao_geral :
                self.padrao_geral = int(self.ids.padrao_geral.text)
            case self.ids.padrao_wilson :
                self.padrao_wilson = int(self.ids.padrao_wilson.text)
            case self.ids.padrao_celio :
                self.padrao_celio = int(self.ids.padrao_celio.text)
            case self.ids.valor_conta :
                self.valor_conta = float(self.ids.valor_conta.text)
            case self.ids.valor_kw :
                self.valor_kw = float(self.ids.valor_kw.text)
            case self.ids.taxa_iluminacao:
                self.taxa_iluminacao = float(self.ids.taxa_iluminacao.text)
        self.verify_inputs()
        

    def verify_inputs(self):
        if (self.padrao_geral != "" )& (self.padrao_wilson != "") & (self.padrao_celio!="") & (self.valor_conta != "") & (self.valor_kw != ""):
            self.ids.button.disabled = False
        else:
            self.ids.button.disabled = True

    def calculate(self):
        kw_total_geral = self.padrao_geral - self.padrao_geral_anterior

        kw_wilson = self.padrao_wilson - self.padrao_wilson_anterior

        kw_celio = self.padrao_celio - self.padrao_celio_anterior

        if kw_total_geral > (kw_wilson + kw_celio):
            kw_restante = kw_total_geral - (kw_wilson + kw_celio)
            kw_wilson += kw_restante/2
            kw_celio += kw_restante/2
            self.descricao = self.descricao + f"\n{kw_restante} kw: voando -> valor divido entre os dois"
        elif kw_total_geral < (kw_wilson + kw_celio):
            kw_excedente = (kw_wilson + kw_celio) - kw_total_geral
            kw_wilson -= kw_excedente/2
            kw_celio -= kw_excedente/2
            self.descricao = self.descricao + f"\n{kw_excedente} kw: execedente (valor gasto pelos dois maior que o constante na conta) -> valor abatido igualmente entre os dois"

        self.valor_wilson = kw_wilson * self.valor_kw
        self.valor_celio = kw_celio * self.valor_kw

        if int(self.taxa_iluminacao) > 0:
            self.valor_celio = self.valor_celio + self.taxa_iluminacao/2
            self.valor_wilson = self.valor_wilson + self.taxa_iluminacao/2
            self.descricao = self.descricao + f"\n{self.taxa_iluminacao} R$: taxa de iluminação -> valor divido entre os dois"
        
        if self.valor_conta > (self.valor_celio+self.valor_wilson):
            valor_restante = self.valor_conta - (self.valor_wilson + self.valor_celio)
            self.valor_wilson += valor_restante/2
            self.valor_celio += valor_restante/2
            self.descricao = self.descricao + f"\n{valor_restante} R$: valor adicional(taxas de atraso, valores inseridos errado, etc) -> valor divido entre os dois"

        print(f"Valor wilson: {self.valor_wilson}\nValor Célio: {self.valor_celio}\nDescrição: {self.descricao}")
        
 
        
class WindowManager(ScreenManager):
    pass


class main(MDApp):
    def build(self):
        Window.clearcolor = "#D6E68A"
        Window.size = (375,700)
        return Builder.load_file('front-end.kv')

if __name__ == '__main__':
    main().run()