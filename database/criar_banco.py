
from database.conexao import conectar


def criar_banco():
    
    conexao = conectar()
    cursor = conexao.cursor()

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT    NOT NULL,
            categoria TEXT,
            marca     TEXT,
            preco     REAL    NOT NULL DEFAULT 0,
            estoque   INTEGER NOT NULL DEFAULT 0
        )
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda   TEXT    NOT NULL,
            cliente      TEXT,
            valor_total  REAL    NOT NULL DEFAULT 0
        )
    """)

    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id       INTEGER NOT NULL,
            produto_id     INTEGER NOT NULL,
            quantidade     INTEGER NOT NULL,
            valor_unitario REAL    NOT NULL,
            subtotal       REAL    NOT NULL,
            FOREIGN KEY (venda_id)   REFERENCES vendas(id)   ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    
    criar_banco()
    print("Banco de dados criado/verificado com sucesso.")
