import tkinter as tk
from tkinter import ttk, messagebox

from controllers import produto_controller, venda_controller


class TelaVendas:
    

    def __init__(self, root):
        self.root = root
        self.root.title("Vendas")
        self.root.geometry("900x600")
        self.root.configure(bg="#ecf0f3")

        
        self.carrinho = []

        
        self.produtos = produto_controller.listar_produtos()
        self.mapa_produtos = {p.nome: p for p in self.produtos}

        
        tk.Label(root, text="Registro de Venda",
                 font=("Arial", 16, "bold"),
                 bg="#ecf0f3", fg="#333").pack(pady=10)

       
        frame_cli = tk.Frame(root, bg="#ecf0f3")
        frame_cli.pack(fill="x", padx=15)
        tk.Label(frame_cli, text="Cliente:", bg="#ecf0f3").pack(side="left")
        self.entry_cliente = tk.Entry(frame_cli, width=40)
        self.entry_cliente.pack(side="left", padx=5)

        
        frame_sel = tk.LabelFrame(root, text="Adicionar produto ao carrinho",
                                  bg="#ecf0f3", padx=10, pady=10)
        frame_sel.pack(fill="x", padx=15, pady=10)

        tk.Label(frame_sel, text="Produto:", bg="#ecf0f3").grid(row=0, column=0, padx=5)
        self.combo_produto = ttk.Combobox(frame_sel,
                                          values=list(self.mapa_produtos.keys()),
                                          state="readonly", width=35)
        self.combo_produto.grid(row=0, column=1, padx=5)

        tk.Label(frame_sel, text="Qtd:", bg="#ecf0f3").grid(row=0, column=2, padx=5)
        self.entry_qtd = tk.Entry(frame_sel, width=6)
        self.entry_qtd.grid(row=0, column=3, padx=5)
        self.entry_qtd.insert(0, "1")

        tk.Button(frame_sel, text="Adicionar", bg="#28a745", fg="white",
                  width=12, command=self.adicionar_item).grid(row=0, column=4, padx=5)
        tk.Button(frame_sel, text="Recarregar Produtos",
                  command=self.recarregar_produtos).grid(row=0, column=5, padx=5)

        
        colunas = ("produto", "qtd", "valor_unit", "subtotal")
        self.tree = ttk.Treeview(root, columns=colunas, show="headings", height=10)
        for col, texto, largura in [
            ("produto", "Produto", 320),
            ("qtd", "Quantidade", 100),
            ("valor_unit", "Valor Unit. (R$)", 130),
            ("subtotal", "Subtotal (R$)", 130),
        ]:
            self.tree.heading(col, text=texto)
            self.tree.column(col, width=largura, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)

     
        frame_total = tk.Frame(root, bg="#ecf0f3")
        frame_total.pack(fill="x", padx=15, pady=10)

        self.label_total = tk.Label(frame_total, text="Total: R$ 0,00",
                                    font=("Arial", 14, "bold"),
                                    bg="#ecf0f3", fg="#2d6cdf")
        self.label_total.pack(side="left")

        tk.Button(frame_total, text="Remover item", bg="#dc3545", fg="white",
                  width=14, command=self.remover_item).pack(side="right", padx=5)
        tk.Button(frame_total, text="Limpar carrinho", width=14,
                  command=self.limpar_carrinho).pack(side="right", padx=5)
        tk.Button(frame_total, text="Finalizar Venda", bg="#2d6cdf", fg="white",
                  width=18, font=("Arial", 10, "bold"),
                  command=self.finalizar_venda).pack(side="right", padx=5)

    

    def recarregar_produtos(self):
        
        self.produtos = produto_controller.listar_produtos()
        self.mapa_produtos = {p.nome: p for p in self.produtos}
        self.combo_produto["values"] = list(self.mapa_produtos.keys())

    def adicionar_item(self):
        nome = self.combo_produto.get()
        if not nome:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        try:
            qtd = int(self.entry_qtd.get().strip())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        produto = self.mapa_produtos[nome]

        
        qtd_no_carrinho = sum(i["quantidade"] for i in self.carrinho
                              if i["produto_id"] == produto.id)
        if (qtd_no_carrinho + qtd) > produto.estoque:
            messagebox.showerror(
                "Estoque insuficiente",
                f"Estoque disponível para '{produto.nome}': {produto.estoque}\n"
                f"Já no carrinho: {qtd_no_carrinho}"
            )
            return

        subtotal = qtd * produto.preco
        self.carrinho.append({
            "produto_id": produto.id,
            "produto_nome": produto.nome,
            "quantidade": qtd,
            "valor_unitario": produto.preco,
            "subtotal": subtotal,
        })
        self.atualizar_tabela()

    def remover_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um item no carrinho.")
            return
        indice = self.tree.index(sel[0])
        del self.carrinho[indice]
        self.atualizar_tabela()

    def limpar_carrinho(self):
        self.carrinho = []
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = 0.0
        for i in self.carrinho:
            self.tree.insert("", "end", values=(
                i["produto_nome"], i["quantidade"],
                f"{i['valor_unitario']:.2f}", f"{i['subtotal']:.2f}"
            ))
            total += i["subtotal"]
        self.label_total.config(text=f"Total: R$ {total:.2f}".replace(".", ","))

    def finalizar_venda(self):
        if not self.carrinho:
            messagebox.showwarning("Atenção", "O carrinho está vazio.")
            return
        cliente = self.entry_cliente.get().strip() or "Consumidor"

        itens = [{
            "produto_id": i["produto_id"],
            "quantidade": i["quantidade"],
            "valor_unitario": i["valor_unitario"],
        } for i in self.carrinho]

        try:
            venda_id = venda_controller.registrar_venda(cliente, itens)
            messagebox.showinfo("Venda concluída",
                                f"Venda #{venda_id} registrada com sucesso!")
            self.carrinho = []
            self.entry_cliente.delete(0, tk.END)
            self.atualizar_tabela()
            self.recarregar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
