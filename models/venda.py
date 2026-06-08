class Venda:
    

    def __init__(self, id=None, data_venda="", cliente="", valor_total=0.0):
        self.id = id
        self.data_venda = data_venda
        self.cliente = cliente
        self.valor_total = float(valor_total)

    def __repr__(self):
        return f"Venda(id={self.id}, cliente={self.cliente}, total={self.valor_total})"
