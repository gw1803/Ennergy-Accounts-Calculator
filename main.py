from asyncio import wait
from datetime import date
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from KivyMD.kivymd.uix.button import MDButton, MDButtonText
from KivyMD.kivymd.uix.pickers.datepicker.datepicker import MDModalInputDatePicker, MDModalDatePicker

contas = []


class Conta():
    
    def __init__(self, padrao_geral, padrao_wilson, padrao_celio, valor_conta, valor_kw, taxa_iluminacao, descricao, descricao_wilson, descricao_celio):
        self.padrao_geral = padrao_geral
        self.padrao_wilson = padrao_wilson
        self.padrao_celio = padrao_celio
        self.valor_conta = valor_conta
        self.valor_kw = valor_kw
        self.taxa_iluminacao = taxa_iluminacao 
        self.descricao = descricao
        self.descricao_wilson = descricao_wilson
        self.descricao_celio = descricao_celio

contas.append(Conta(padrao_geral=31100, padrao_wilson = 36050, padrao_celio=24050, valor_conta=100, valor_kw=1, descricao_wilson="", descricao_celio="", descricao="", taxa_iluminacao=""))
contas.append(Conta(padrao_geral=31100, padrao_wilson = 36050, padrao_celio=24050, valor_conta=100, valor_kw=1, descricao_wilson="", descricao_celio="", descricao="", taxa_iluminacao=""))

class Inicio(Screen):
    pass

class RealizarCalculo(Screen):
    #calculated values
    valor_wilson = 0
    valor_celio = 0
    descricao = ""
    descricao_wilson = ""
    descricao_celio = ""
    data = date.today().strftime('%d/%m/%y')

    #values from the previous account
    padrao_geral_anterior = 31000
    padrao_wilson_anterior = 36000
    padrao_celio_anterior = 24000

    #values from the form 
    padrao_geral = ""
    padrao_wilson = ""
    padrao_celio = ""
    valor_conta = ""
    valor_kw = ""
    taxa_iluminacao = 0

    def on_ok(self, instance_date_picker):
        data = str(instance_date_picker.get_date()[0].strftime('%d/%m/%y'))
        self.ids.DataText.text = data
        instance_date_picker.dismiss()

    def open_modal(self):
        date_dialog = MDModalDatePicker()
        date_dialog.date_format = 'dd/mm/yyyy'
        date_dialog.supporting_text = "Insira uma data"
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.on_cancel = date_dialog.dismiss
        date_dialog.open()

    def on_text(self, input):
        if input.text != "":
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
        if(self.ids.button.disabled == True):
            return
        kw_total_geral = self.padrao_geral - self.padrao_geral_anterior

        kw_wilson = self.padrao_wilson - self.padrao_wilson_anterior

        kw_celio = self.padrao_celio - self.padrao_celio_anterior

        if kw_total_geral > (kw_wilson + kw_celio):
            kw_restante = kw_total_geral - (kw_wilson + kw_celio)
            kw_wilson += kw_restante/2
            kw_celio += kw_restante/2
            self.descricao = self.descricao + f"{kw_restante} kw: voando -> valor divido entre os dois\n"
        elif kw_total_geral < (kw_wilson + kw_celio):
            kw_excedente = (kw_wilson + kw_celio) - kw_total_geral
            kw_wilson -= kw_excedente/2
            kw_celio -= kw_excedente/2
            self.descricao = self.descricao + f"\n{kw_excedente} kw: execedente (valor gasto pelos dois maior que o constante na conta) -> valor abatido igualmente entre os dois"

        self.valor_wilson = kw_wilson * self.valor_kw
        self.descricao_wilson += f"{kw_wilson}*{self.valor_kw} = {self.valor_wilson}"
        self.valor_celio = kw_celio * self.valor_kw
        self.descricao_celio += f"{kw_celio}*{self.valor_kw} = {self.valor_celio}"

        if self.taxa_iluminacao > 0:
            self.descricao_celio += f"\n{self.valor_celio}+{self.taxa_iluminacao/2} = {self.valor_celio + self.taxa_iluminacao/2}"
            self.valor_celio = self.valor_celio + self.taxa_iluminacao/2
            self.descricao_wilson += f"\n{self.valor_wilson}+{self.taxa_iluminacao/2} = {self.valor_wilson + self.taxa_iluminacao/2}"
            self.valor_wilson = self.valor_wilson + self.taxa_iluminacao/2
            
            self.descricao = self.descricao + f"{self.taxa_iluminacao} R$: taxa de iluminação -> valor divido entre os dois\n"
        
        if self.valor_conta > (self.valor_celio+self.valor_wilson):
            valor_restante = self.valor_conta - (self.valor_wilson + self.valor_celio)
            self.descricao_wilson += f"\n{self.valor_wilson}+{valor_restante/2} = {self.valor_wilson + valor_restante/2}"
            self.valor_wilson += valor_restante/2
            self.descricao_celio += f"\n{self.valor_celio}+{valor_restante/2} = {self.valor_celio + valor_restante/2}"
            self.valor_celio += valor_restante/2
            self.descricao = self.descricao + f"{valor_restante} R$: valor adicional(taxas de atraso, valores inseridos errado, etc) -> valor divido entre os dois\n"
        
        self.descricao_wilson += f"\nValor final: {self.valor_wilson}"
        self.descricao_celio += f"\nValor final: {self.valor_celio}"
        
        c = Conta(padrao_geral=self.padrao_geral, padrao_wilson = self.padrao_wilson, padrao_celio=self.padrao_celio, valor_conta=self.valor_conta, valor_kw=self.valor_kw, descricao_wilson=self.descricao_wilson, descricao_celio=self.descricao_celio, descricao=self.descricao, taxa_iluminacao=self.taxa_iluminacao)
        contas.append(c)

        self.ids.padrao_geral.text = ""
        self.ids.padrao_wilson.text = ""
        self.ids.padrao_celio.text = ""
        self.ids.valor_conta.text = ""
        self.ids.valor_kw.text = ""
        self.ids.taxa_iluminacao.text = ""
        data = date.today().strftime('%d/%m/%y')

        self.manager.current = "Resultado"
               
class Resultado(Screen):
    #achar instancia de RealizarCalculo
    description_verifier = True

    def reload_variables(self):
        realizar_calculo_screen = self.manager.get_screen('RealizarCalculo')
        self.ids.valor_wilson.text = realizar_calculo_screen.descricao_wilson
        self.ids.valor_celio.text = realizar_calculo_screen.descricao_celio
        self.ids.descricao.text = realizar_calculo_screen.descricao

    def on_release_descricao(self):
        if self.description_verifier:
            self.ids.button_edit.pos_hint = {'x': 1.15}
            self.ids.button_exclude.pos_hint = {'x': 1.15}
            self.ids.descricao.pos_hint = {'x': 0.15, 'y': 0.13}
            self.ids.widget.size_hint = 0.8, 0.75
            self.ids.widget.pos_hint = {'x': 0.1, 'y': 0.10}
            self.description_verifier = False
        else:
            self.ids.button_edit.pos_hint = {'x': 0.12, 'y': 0.1}
            self.ids.button_exclude.pos_hint =  {'x': 0.6, 'y': 0.1}
            self.ids.descricao.pos_hint = {'x': 1.15, 'y': 0.13}
            self.ids.widget.size_hint = 0.8, 0.6
            self.ids.widget.pos_hint = {'x': 0.1, 'y': 0.25}
            self.description_verifier = True

    def on_realease_edit(self):
        pass

class VisualizarCalculos(Screen):
    def show_buttons(self):
        y_offset = 0.7
        for c in contas:
            button = MDButton(
                MDButtonText(
                    text= "Visualizar cálculos",
                    theme_font_name= "Custom",
                    theme_font_size= "Custom",
                    font_name= 'fonts/Roboto-Light.ttf',
                    color = '#121310',
                    pos_hint= {"x": .2, "center_y": .5},
                    font_size= 25
                ),
                pos_hint = {"center_x": .5, "y": y_offset},
                height = 70,
                shadow_offset = (6, -6),
            )
            y_offset -= 0.1
            self.add_widget(button)

class WindowManager(ScreenManager):
    pass

class main(MDApp):
    def build(self):
        Window.clearcolor = "#D6E68A"
        Window.size = (375,700)
        return Builder.load_file('front-end.kv')

if __name__ == '__main__':
    main().run()