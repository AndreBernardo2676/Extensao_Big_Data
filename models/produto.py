class Produto:
    

    def __init__(self, id=None, nome="", categoria="", marca="", preco=0.0, estoque=0):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.marca = marca
        self.preco = float(preco)
        self.estoque = int(estoque)

    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome}, preco={self.preco}, estoque={self.estoque})"
