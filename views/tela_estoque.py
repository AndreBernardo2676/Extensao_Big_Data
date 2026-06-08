import tkinter as tk
from tkinter import ttk, messagebox

from controllers import estoque_controller, produto_controller


class TelaEstoque:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Estoque")
        self.root.geometry("820x560")
        self.root.configure(bg="#ecf0f3")

        self.produto_selecionado_id = None

        
        tk.Label(root, text="Controle de Estoque",
                 font=("Arial", 16, "bold"),
                 bg="#ecf0f3", fg="#333").pack(pady=10)

        
        frame_op = tk.LabelFrame(root, text="Operações", bg="#ecf0f3", padx=10, pady=10)
        frame_op.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_op, text="Quantidade:", bg="#ecf0f3").grid(row=0, column=0, padx=5, pady=4)
        self.entry_qtd = tk.Entry(frame_op, width=10)
        self.entry_qtd.grid(row=0, column=1, padx=5, pady=4)

        tk.Button(frame_op, text="Entrada (+)", bg="#28a745", fg="white", width=12,
                  command=self.entrada).grid(row=0, column=2, padx=5)
        tk.Button(frame_op, text="Ajustar (=)", bg="#17a2b8", fg="white", width=12,
                  command=self.ajustar).grid(row=0, column=3, padx=5)
        tk.Button(frame_op, text="Atualizar lista", width=14,
                  command=self.carregar_lista).grid(row=0, column=4, padx=5)

        tk.Label(frame_op,
                 text="(Selecione um produto na lista e informe a quantidade)",
                 font=("Arial", 9, "italic"), bg="#ecf0f3", fg="#666"
                 ).grid(row=1, column=0, columnspan=5, pady=4)

        
        colunas = ("id", "nome", "categoria", "marca", "preco", "estoque")
        self.tree = ttk.Treeview(root, columns=colunas, show="headings", height=14)
        for col, texto, largura in [
            ("id", "ID", 50),
            ("nome", "Nome", 220),
            ("categoria", "Categoria", 120),
            ("marca", "Marca", 120),
            ("preco", "Preço (R$)", 90),
            ("estoque", "Estoque", 80),
        ]:
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=largura, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar)

        self.carregar_lista()

    def carregar_lista(self):
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in estoque_controller.consultar_estoque():
            
            tag = "baixo" if p["estoque"] <= 5 else ""
            self.tree.insert("", "end", values=(
                p["id"], p["nome"], p["categoria"], p["marca"],
                f"{p['preco']:.2f}", p["estoque"]
            ), tags=(tag,))
        self.tree.tag_configure("baixo", background="#ffe0e0")

    def selecionar(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        valores = self.tree.item(sel[0])["values"]
        self.produto_selecionado_id = valores[0]

    def _ler_quantidade(self):
        try:
            return int(self.entry_qtd.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return None

    def entrada(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        qtd = self._ler_quantidade()
        if qtd is None:
            return
        try:
            estoque_controller.entrada_estoque(self.produto_selecionado_id, qtd)
            messagebox.showinfo("Sucesso", "Entrada de estoque registrada.")
            self.entry_qtd.delete(0, tk.END)
            self.carregar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def ajustar(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        qtd = self._ler_quantidade()
        if qtd is None:
            return
        try:
            estoque_controller.ajustar_estoque(self.produto_selecionado_id, qtd)
            messagebox.showinfo("Sucesso", "Estoque ajustado.")
            self.entry_qtd.delete(0, tk.END)
            self.carregar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
