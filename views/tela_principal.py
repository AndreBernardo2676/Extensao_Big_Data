import tkinter as tk
from tkinter import ttk, messagebox

from views.tela_produtos import TelaProdutos
from views.tela_estoque import TelaEstoque
from views.tela_vendas import TelaVendas
from views.tela_relatorios import TelaRelatorios
from views.tela_dashboard import TelaDashboard
from utils.importar_excel import importar_planilha_excel


class TelaPrincipal:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Vendas e Estoque")
        self.root.geometry("820x520")
        self.root.configure(bg="#ecf0f3")

        
        cabecalho = tk.Frame(root, bg="#2d6cdf", height=70)
        cabecalho.pack(fill="x")
        tk.Label(
            cabecalho,
            text="Sistema de Controle de Vendas e Estoque",
            font=("Arial", 18, "bold"),
            bg="#2d6cdf",
            fg="white",
        ).pack(pady=18)

        
        container = tk.Frame(root, bg="#ecf0f3")
        container.pack(expand=True)

        tk.Label(
            container,
            text="Menu Principal",
            font=("Arial", 14, "bold"),
            bg="#ecf0f3",
            fg="#333",
        ).grid(row=0, column=0, columnspan=3, pady=20)

        
        botoes = [
            ("Produtos", self.abrir_produtos),
            ("Estoque", self.abrir_estoque),
            ("Vendas", self.abrir_vendas),
            ("Relatórios", self.abrir_relatorios),
            ("Dashboard", self.abrir_dashboard),
            ("Importar Excel", self.importar_excel),
        ]

        for i, (texto, comando) in enumerate(botoes):
            linha = (i // 3) + 1
            coluna = i % 3
            btn = tk.Button(
                container,
                text=texto,
                width=20,
                height=3,
                font=("Arial", 11, "bold"),
                bg="#ffffff",
                fg="#2d6cdf",
                activebackground="#2d6cdf",
                activeforeground="white",
                relief="raised",
                bd=2,
                command=comando,
            )
            btn.grid(row=linha, column=coluna, padx=15, pady=15)

        
        rodape = tk.Label(
            root,
            text="Projeto Acadêmico - Python + Tkinter + SQLite",
            bg="#ecf0f3",
            fg="#666",
            font=("Arial", 9),
        )
        rodape.pack(side="bottom", pady=8)

    

    def abrir_produtos(self):
        janela = tk.Toplevel(self.root)
        TelaProdutos(janela)

    def abrir_estoque(self):
        janela = tk.Toplevel(self.root)
        TelaEstoque(janela)

    def abrir_vendas(self):
        janela = tk.Toplevel(self.root)
        TelaVendas(janela)

    def abrir_relatorios(self):
        janela = tk.Toplevel(self.root)
        TelaRelatorios(janela)

    def abrir_dashboard(self):
        janela = tk.Toplevel(self.root)
        TelaDashboard(janela)

    def importar_excel(self):
        
        from tkinter import filedialog
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha Excel",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")],
        )
        if not caminho:
            return
        try:
            qtd = importar_planilha_excel(caminho)
            messagebox.showinfo(
                "Importação concluída",
                f"{qtd} linhas importadas com sucesso!",
            )
        except Exception as e:
            messagebox.showerror("Erro na importação", str(e))
