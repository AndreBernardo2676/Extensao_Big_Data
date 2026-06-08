import tkinter as tk
from tkinter import ttk, messagebox

from controllers import produto_controller


class TelaProdutos:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Produtos")
        self.root.geometry("820x560")
        self.root.configure(bg="#ecf0f3")

        self.produto_selecionado_id = None

        
        tk.Label(root, text="Gestão de Produtos",
                 font=("Arial", 16, "bold"),
                 bg="#ecf0f3", fg="#333").pack(pady=10)

        
        frame_form = tk.LabelFrame(root, text="Dados do Produto", bg="#ecf0f3", padx=10, pady=10)
        frame_form.pack(fill="x", padx=15, pady=5)

        
        tk.Label(frame_form, text="Nome:", bg="#ecf0f3").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Categoria:", bg="#ecf0f3").grid(row=0, column=2, sticky="e", padx=5, pady=4)
        self.entry_categoria = tk.Entry(frame_form, width=20)
        self.entry_categoria.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Marca:", bg="#ecf0f3").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        self.entry_marca = tk.Entry(frame_form, width=30)
        self.entry_marca.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Preço:", bg="#ecf0f3").grid(row=1, column=2, sticky="e", padx=5, pady=4)
        self.entry_preco = tk.Entry(frame_form, width=20)
        self.entry_preco.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Estoque:", bg="#ecf0f3").grid(row=2, column=0, sticky="e", padx=5, pady=4)
        self.entry_estoque = tk.Entry(frame_form, width=30)
        self.entry_estoque.grid(row=2, column=1, padx=5, pady=4)

        
        frame_botoes = tk.Frame(root, bg="#ecf0f3")
        frame_botoes.pack(pady=5)

        tk.Button(frame_botoes, text="Cadastrar", width=12, bg="#28a745", fg="white",
                  command=self.cadastrar).grid(row=0, column=0, padx=4)
        tk.Button(frame_botoes, text="Editar", width=12, bg="#ffc107",
                  command=self.editar).grid(row=0, column=1, padx=4)
        tk.Button(frame_botoes, text="Excluir", width=12, bg="#dc3545", fg="white",
                  command=self.excluir).grid(row=0, column=2, padx=4)
        tk.Button(frame_botoes, text="Limpar", width=12,
                  command=self.limpar_campos).grid(row=0, column=3, padx=4)

        
        frame_pesquisa = tk.Frame(root, bg="#ecf0f3")
        frame_pesquisa.pack(fill="x", padx=15, pady=5)
        tk.Label(frame_pesquisa, text="Pesquisar:", bg="#ecf0f3").pack(side="left")
        self.entry_pesquisa = tk.Entry(frame_pesquisa, width=40)
        self.entry_pesquisa.pack(side="left", padx=5)
        tk.Button(frame_pesquisa, text="Buscar",
                  command=self.pesquisar).pack(side="left", padx=4)
        tk.Button(frame_pesquisa, text="Mostrar Todos",
                  command=self.carregar_lista).pack(side="left", padx=4)

        
        colunas = ("id", "nome", "categoria", "marca", "preco", "estoque")
        self.tree = ttk.Treeview(root, columns=colunas, show="headings", height=12)
        for col, texto, largura in [
            ("id", "ID", 50),
            ("nome", "Nome", 200),
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
        for p in produto_controller.listar_produtos():
            self.tree.insert("", "end", values=(
                p.id, p.nome, p.categoria, p.marca,
                f"{p.preco:.2f}", p.estoque
            ))

    def pesquisar(self):
        
        termo = self.entry_pesquisa.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in produto_controller.pesquisar_produtos(termo):
            self.tree.insert("", "end", values=(
                p.id, p.nome, p.categoria, p.marca,
                f"{p.preco:.2f}", p.estoque
            ))

    def selecionar(self, event):
        
        sel = self.tree.selection()
        if not sel:
            return
        valores = self.tree.item(sel[0])["values"]
        self.produto_selecionado_id = valores[0]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, valores[1])
        self.entry_categoria.delete(0, tk.END)
        self.entry_categoria.insert(0, valores[2])
        self.entry_marca.delete(0, tk.END)
        self.entry_marca.insert(0, valores[3])
        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, valores[4])
        self.entry_estoque.delete(0, tk.END)
        self.entry_estoque.insert(0, valores[5])

    def limpar_campos(self):
        
        self.produto_selecionado_id = None
        self.entry_nome.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_estoque.delete(0, tk.END)

    def _obter_dados_formulario(self):
        
        nome = self.entry_nome.get().strip()
        categoria = self.entry_categoria.get().strip()
        marca = self.entry_marca.get().strip()
        preco_txt = self.entry_preco.get().strip().replace(",", ".")
        estoque_txt = self.entry_estoque.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome do produto.")
            return None
        try:
            preco = float(preco_txt) if preco_txt else 0.0
            estoque = int(estoque_txt) if estoque_txt else 0
        except ValueError:
            messagebox.showerror("Erro", "Preço ou estoque inválido.")
            return None

        return nome, categoria, marca, preco, estoque

    def cadastrar(self):
        dados = self._obter_dados_formulario()
        if dados is None:
            return
        produto_controller.cadastrar_produto(*dados)
        messagebox.showinfo("Sucesso", "Produto cadastrado.")
        self.limpar_campos()
        self.carregar_lista()

    def editar(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto na lista.")
            return
        dados = self._obter_dados_formulario()
        if dados is None:
            return
        produto_controller.editar_produto(self.produto_selecionado_id, *dados)
        messagebox.showinfo("Sucesso", "Produto atualizado.")
        self.limpar_campos()
        self.carregar_lista()

    def excluir(self):
        if self.produto_selecionado_id is None:
            messagebox.showwarning("Atenção", "Selecione um produto na lista.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir o produto?"):
            return
        try:
            produto_controller.excluir_produto(self.produto_selecionado_id)
            messagebox.showinfo("Sucesso", "Produto excluído.")
            self.limpar_campos()
            self.carregar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")
