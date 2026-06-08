from database.conexao import conectar


def entrada_estoque(produto_id, quantidade):
    
    if quantidade <= 0:
        raise ValueError("A quantidade de entrada deve ser maior que zero.")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE produtos SET estoque = estoque + ? WHERE id = ?",
        (int(quantidade), produto_id),
    )
    conexao.commit()
    conexao.close()


def ajustar_estoque(produto_id, novo_valor):
    
    if novo_valor < 0:
        raise ValueError("O estoque não pode ser negativo.")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE produtos SET estoque = ? WHERE id = ?",
        (int(novo_valor), produto_id),
    )
    conexao.commit()
    conexao.close()


def consultar_estoque():
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, categoria, marca, preco, estoque
        FROM produtos
        ORDER BY nome
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]


def produtos_estoque_baixo(limite=5):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, nome, categoria, marca, preco, estoque
        FROM produtos
        WHERE estoque <= ?
        ORDER BY estoque ASC
    """, (int(limite),))
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]
