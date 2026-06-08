class ItemVenda:
    

    def __init__(self, id=None, venda_id=None, produto_id=None,
                 quantidade=0, valor_unitario=0.0, subtotal=0.0):
        self.id = id
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.quantidade = int(quantidade)
        self.valor_unitario = float(valor_unitario)
        self.subtotal = float(subtotal)

    def __repr__(self):
        return (f"ItemVenda(produto_id={self.produto_id}, qtd={self.quantidade}, "
                f"subtotal={self.subtotal})")
