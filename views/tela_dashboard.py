import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from controllers import venda_controller


class TelaDashboard:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("950x650")
        self.root.configure(bg="#ecf0f3")

        
        tk.Label(root, text="Dashboard de Vendas",
                 font=("Arial", 16, "bold"),
                 bg="#ecf0f3", fg="#333").pack(pady=10)

        
        frame_btn = tk.Frame(root, bg="#ecf0f3")
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="Produtos mais vendidos", width=22,
                  command=self.grafico_mais_vendidos).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Vendas por categoria", width=22,
                  command=self.grafico_categorias).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Faturamento por mês", width=22,
                  command=self.grafico_faturamento_mes).pack(side="left", padx=5)

        
        self.frame_grafico = tk.Frame(root, bg="white", relief="sunken", bd=1)
        self.frame_grafico.pack(fill="both", expand=True, padx=15, pady=10)

        self.canvas = None

        
        self.grafico_mais_vendidos()

    def _limpar_grafico(self):
        
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def _desenhar(self, fig):
        
        self._limpar_grafico()
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    

    def grafico_mais_vendidos(self):
        dados = venda_controller.produtos_mais_vendidos(limite=5)
        fig = Figure(figsize=(8, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        if not dados:
            ax.text(0.5, 0.5, "Sem dados de vendas",
                    ha="center", va="center", fontsize=14)
            ax.axis("off")
        else:
            nomes = [d["produto"] for d in dados]
            qtds = [d["total_vendido"] for d in dados]
            ax.bar(nomes, qtds, color="#2d6cdf")
            ax.set_title("Top 5 Produtos Mais Vendidos")
            ax.set_ylabel("Quantidade Vendida")
            for tick in ax.get_xticklabels():
                tick.set_rotation(20)

        fig.tight_layout()
        self._desenhar(fig)

    def grafico_categorias(self):
        dados = venda_controller.vendas_por_categoria()
        fig = Figure(figsize=(8, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        if not dados:
            ax.text(0.5, 0.5, "Sem dados de vendas",
                    ha="center", va="center", fontsize=14)
            ax.axis("off")
        else:
            categorias = [d["categoria"] for d in dados]
            totais = [d["total"] for d in dados]
            ax.pie(totais, labels=categorias, autopct="%1.1f%%", startangle=90)
            ax.set_title("Vendas por Categoria")

        fig.tight_layout()
        self._desenhar(fig)

    def grafico_faturamento_mes(self):
        dados = venda_controller.faturamento_por_mes()
        fig = Figure(figsize=(8, 4.5), dpi=100)
        ax = fig.add_subplot(111)

        if not dados:
            ax.text(0.5, 0.5, "Sem dados de vendas",
                    ha="center", va="center", fontsize=14)
            ax.axis("off")
        else:
            meses = [d["mes"] for d in dados]
            totais = [d["total"] for d in dados]
            ax.plot(meses, totais, marker="o", color="#28a745", linewidth=2)
            ax.set_title("Faturamento por Mês")
            ax.set_ylabel("Faturamento (R$)")
            ax.grid(True, linestyle="--", alpha=0.5)
            for tick in ax.get_xticklabels():
                tick.set_rotation(30)

        fig.tight_layout()
        self._desenhar(fig)
