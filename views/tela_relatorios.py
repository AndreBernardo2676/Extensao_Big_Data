import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from controllers import produto_controller, estoque_controller, venda_controller
from utils.exportar_excel import exportar_para_excel


class TelaRelatorios:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Relatórios")
        self.root.geometry("900x600")
        self.root.configure(bg="#ecf0f3")

        self.dados_atuais = []     # lista de dicts
        self.colunas_atuais = []   # lista de chaves

      
        tk.Label(root, text="Relatórios",
                 font=("Arial", 16, "bold"),
                 bg="#ecf0f3", fg="#333").pack(pady=10)

        
        frame_btn = tk.Frame(root, bg="#ecf0f3")
        frame_btn.pack(fill="x", padx=15, pady=5)

        tk.Button(frame_btn, text="Produtos Cadastrados", width=22,
                  command=self.rel_produtos).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Estoque Atual", width=18,
                  command=self.rel_estoque).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Estoque Baixo (≤5)", width=18,
                  command=self.rel_estoque_baixo).pack(side="left", padx=4)
        tk.Button(frame_btn, text="Histórico de Vendas", width=20,
                  command=self.rel_vendas).pack(side="left", padx=4)

        tk.Button(root, text="Exportar para Excel",
                  bg="#28a745", fg="white", width=20,
                  command=self.exportar).pack(pady=5)

      
        self.tree = ttk.Treeview(root, show="headings", height=18)
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def _atualizar_treeview(self, dados, colunas, cabecalhos):
        
        self.dados_atuais = dados
        self.colunas_atuais = colunas

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = colunas
        for col, cab in zip(colunas, cabecalhos):
            self.tree.heading(col, text=cab)
            self.tree.column(col, width=140, anchor="center")
        for d in dados:
            valores = [d.get(c, "") for c in colunas]
            self.tree.insert("", "end", values=valores)

  

    def rel_produtos(self):
        produtos = produto_controller.listar_produtos()
        dados = [{
            "id": p.id, "nome": p.nome, "categoria": p.categoria,
            "marca": p.marca, "preco": p.preco, "estoque": p.estoque
        } for p in produtos]
        self._atualizar_treeview(
            dados,
            ["id", "nome", "categoria", "marca", "preco", "estoque"],
            ["ID", "Nome", "Categoria", "Marca", "Preço", "Estoque"],
        )

    def rel_estoque(self):
        dados = estoque_controller.consultar_estoque()
        self._atualizar_treeview(
            dados,
            ["id", "nome", "categoria", "marca", "preco", "estoque"],
            ["ID", "Nome", "Categoria", "Marca", "Preço", "Estoque"],
        )

    def rel_estoque_baixo(self):
        dados = estoque_controller.produtos_estoque_baixo(limite=5)
        self._atualizar_treeview(
            dados,
            ["id", "nome", "categoria", "marca", "preco", "estoque"],
            ["ID", "Nome", "Categoria", "Marca", "Preço", "Estoque"],
        )

    def rel_vendas(self):
        dados = venda_controller.listar_vendas()
        self._atualizar_treeview(
            dados,
            ["id", "data_venda", "cliente", "valor_total"],
            ["ID", "Data", "Cliente", "Total (R$)"],
        )


    def exportar(self):
        if not self.dados_atuais:
            messagebox.showwarning("Atenção",
                                   "Carregue um relatório antes de exportar.")
            return
        caminho = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx")],
        )
        if not caminho:
            return
        try:
            exportar_para_excel(self.dados_atuais, self.colunas_atuais, caminho)
            messagebox.showinfo("Sucesso",
                                f"Relatório exportado para:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exportar: {e}")
