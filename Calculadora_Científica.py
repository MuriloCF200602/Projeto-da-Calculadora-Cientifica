import customtkinter as ctk
import math
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculadoraCientifica(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora Científica")
        # REDUÇÃO DA ALTURA: De 620 para 580 para eliminar o espaço em branco
        self.geometry("400x580") 
        self.resizable(False, False)
        self.expressao = ""

        # --- Display ---
        self.tela = ctk.CTkEntry(self, width=380, height=80, font=("Roboto", 32), 
                                 justify="right", border_width=2, fg_color="#1a1a1a")
        # pady=20 para dar um respiro mas não exagerar
        self.tela.grid(row=0, column=0, columnspan=5, padx=10, pady=(20, 10), sticky="nsew")

        # Configurar pesos das linhas para que os botões expandam
        for i in range(1, 7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        # Layout de Botões (mantido)
        botoes = [
            ('sin', 1, 0, "#2b2b2b"), ('cos', 1, 1, "#2b2b2b"), ('tan', 1, 2, "#2b2b2b"), ('log', 1, 3, "#2b2b2b"), ('C', 1, 4, "#a13232"),
            ('√', 2, 0, "#2b2b2b"), ('x²', 2, 1, "#2b2b2b"), ('^', 2, 2, "#2b2b2b"), ('π', 2, 3, "#2b2b2b"), ('/', 2, 4, "#333333"),
            ('7', 3, 0, "#3b3b3b"), ('8', 3, 1, "#3b3b3b"), ('9', 3, 2, "#3b3b3b"), ('(', 3, 3, "#333333"), ('*', 3, 4, "#333333"),
            ('4', 4, 0, "#3b3b3b"), ('5', 4, 1, "#3b3b3b"), ('6', 4, 2, "#3b3b3b"), (')', 4, 3, "#333333"), ('-', 4, 4, "#333333"),
            ('1', 5, 0, "#3b3b3b"), ('2', 5, 1, "#3b3b3b"), ('3', 5, 2, "#3b3b3b"), ('exp', 5, 3, "#333333"), ('+', 5, 4, "#333333"),
            # Botão 0 e = ocupam 2 colunas
            ('0', 6, 0, "#3b3b3b", 2), ('.', 6, 2, "#3b3b3b"), ('=', 6, 3, "#1f6aa5", 2)
        ]

        # Criação dos botões com 'sticky="nsew"' para preencher o grid
        for b in botoes:
            texto, r, c, cor = b[0], b[1], b[2], b[3]
            span = b[4] if len(b) > 4 else 1
            # Largura/Altura fixa foi mantida para 'corner_radius' mas 'sticky' faz o ajuste fino
            ctk.CTkButton(self, text=texto, width=0, height=0, # Largura 0 p/ usar sticky
                          corner_radius=10, font=("Roboto", 18, "bold"),
                          fg_color=cor, command=lambda t=texto: self.clique(t)).grid(
                              row=r, column=c, columnspan=span, padx=4, pady=4, sticky="nsew")

    # --- Lógica (Inalterada, pois já está 100% funcional) ---
    def clique(self, tecla):
        if tecla == "C":
            self.expressao = ""
        elif tecla == "=":
            try:
                s = self.expressao
                abertos = s.count('(')
                fechados = s.count(')')
                if abertos > fechados:
                    s += ')' * (abertos - fechados)

                # Regex para trigonometria e exp
                s = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', s)
                s = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', s)
                s = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', s)
                s = re.sub(r'(\d+)exp(\d+)', r'(\1*10**\2)', s)
                
                s = s.replace('log(', 'math.log10(')
                s = s.replace('√(', 'math.sqrt(')
                s = s.replace('π', 'math.pi')
                s = s.replace('^', '**')
                
                resultado = eval(s, {"math": math})
                self.expressao = str(round(resultado, 10))
            except:
                self.expressao = "Erro"
        elif tecla == "x²":
            self.expressao += "**2"
        elif tecla in ["sin", "cos", "tan", "log", "√"]:
            self.expressao += f"{tecla}("
        else:
            if self.expressao == "Erro": self.expressao = ""
            self.expressao += str(tecla)
        self.atualizar_tela()

    def atualizar_tela(self):
        self.tela.delete(0, 'end')
        self.tela.insert(0, self.expressao)

if __name__ == "__main__":
    app = CalculadoraCientifica()
    app.mainloop()