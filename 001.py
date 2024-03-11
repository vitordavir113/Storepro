import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class Produto:
    def __init__(self, nome, preco, codigo_barra):
        self.nome = nome
        self.preco = preco
        self.codigo_barra = codigo_barra

class Loja:
    def __init__(self):
        self.estoque = {}

    def adicionar_produto(self, produto, quantidade):
        if produto.codigo_barra not in self.estoque:
            self.estoque[produto.codigo_barra] = {'produto': produto, 'quantidade': 0}
        self.estoque[produto.codigo_barra]['quantidade'] += quantidade

    def vender_produto(self, codigo_barra, quantidade):
        if codigo_barra in self.estoque and self.estoque[codigo_barra]['quantidade'] >= quantidade:
            self.estoque[codigo_barra]['quantidade'] -= quantidade
            return self.estoque[codigo_barra]['produto'].preco * quantidade
        else:
            return None

class App:
    def __init__(self, loja):
        self.loja = loja
        self.window = tk.Tk()
        self.window.title("StorePro")  # Mudar o título da janela para "StorePro"
        self.window.state('zoomed')  # Maximizar a janela
        self.window.configure(bg='black')  # Mudar a cor de fundo para preto

        # Criar barra superior com 6 quadrados
        self.top_bar = tk.Frame(self.window, bg='black')
        self.top_bar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # Adicione fill=tk.BOTH, expand=True aqui
        for _ in range(6):
            tk.Button(self.top_bar, bg='gray', width=2, height=2).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adicione fill=tk.BOTH, expand=True aqui

        # Criar barra lateral com 6 quadrados
        self.side_bar = tk.Frame(self.window, bg='black')
        self.side_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adicione fill=tk.BOTH, expand=True aqui
        for _ in range(6):
            tk.Button(self.side_bar, bg='gray', width=2, height=2).pack(fill=tk.BOTH, expand=True)  # Adicione fill=tk.BOTH, expand=True aqui

        # Adicionar botões para criar e vender produtos
        self.estoque_icon = ImageTk.PhotoImage(Image.open('estoqueicon.png').resize((50, 50), 3))  # Redimensionar a imagem do ícone para caber no botão
        self.create_button = tk.Button(self.top_bar, image=self.estoque_icon, command=self.adicionar_produto, bg='gray')  # Mudar a cor do botão para cinza
        self.create_button.pack(side=tk.LEFT)

        self.vendas_icon = ImageTk.PhotoImage(Image.open('vendasicon.png').resize((50, 50), 3))  # Redimensionar a imagem do ícone para caber no botão
        self.sell_button = tk.Button(self.side_bar, image=self.vendas_icon, command=lambda: self.vender_produto(), bg='gray')  # Mudar a cor do botão para cinza
        self.sell_button.pack()

        # Adicionar imagem central
        self.image = Image.open('storeprologo.png').resize((self.window.winfo_screenwidth() // 2, self.window.winfo_screenheight() // 2), 3)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.window, width=self.window.winfo_screenwidth(), height=self.window.winfo_screenheight(), bg='black')  # Mudar a cor de fundo para preto
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image_on_canvas = self.canvas.create_image(self.window.winfo_screenwidth() // 2, self.window.winfo_screenheight() // 2, image=self.photo_image)

        # Redimensionar a imagem quando a janela é redimensionada
        self.window.bind('<Configure>', self.resize_image)

    def resize_image(self, event):
        # Não redimensione a imagem aqui
        pass

    def adicionar_produto(self):
        nome = simpledialog.askstring("Adicionar produto", "Digite o nome do produto:")
        preco = simpledialog.askfloat("Adicionar produto", "Digite o preço do produto:")
        codigo_barra = simpledialog.askstring("Adicionar produto", "Digite o código de barras do produto:")
        quantidade = simpledialog.askinteger("Adicionar produto", "Digite a quantidade do produto:")
        produto = Produto(nome, preco, codigo_barra)
        self.loja.adicionar_produto(produto, quantidade)

    def vender_produto(self):
        codigo_barra = simpledialog.askstring("Vender produto", "Digite o código de barras do produto:")
        quantidade = simpledialog.askinteger("Vender produto", "Digite a quantidade do produto:")
        total = self.loja.vender_produto(codigo_barra, quantidade)
        if total is not None:
            pago = simpledialog.askfloat("Total", "O total é {}. Digite o valor pago pelo cliente:".format(total))
            troco = pago - total
            messagebox.showinfo("Troco", "O troco do cliente é {}".format(troco))
        else:
            messagebox.showinfo("Erro", "Produto não disponível em estoque suficiente.")

    def run(self):
        self.window.mainloop()

def main():
    loja = Loja()
    app = App(loja)
    app.run()

if __name__ == "__main__":
    main()

