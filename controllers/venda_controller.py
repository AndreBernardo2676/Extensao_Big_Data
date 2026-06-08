from datetime import datetime
from database.conexao import conectar


def registrar_venda(cliente, itens):
    
    if not itens:
        raise ValueError("Não é possível registrar venda sem itens.")

    conexao = conectar()
    cursor = conexao.cursor()

    
    for item in itens:
        cursor.execute(
            "SELECT nome, estoque FROM produtos WHERE id = ?",
            (item["produto_id"],),
        )
        linha = cursor.fetchone()
        if linha is None:
            conexao.close()
            raise ValueError(f"Produto ID {item['produto_id']} não encontrado.")
        if linha["estoque"] < item["quantidade"]:
            conexao.close()
            raise ValueError(
                f"Estoque insuficiente para o produto '{linha['nome']}' "
                f"(disponível: {linha['estoque']}, solicitado: {item['quantidade']})."
            )

   
    total = sum(i["quantidade"] * i["valor_unitario"] for i in itens)
    data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    cursor.execute("""
        INSERT INTO vendas (data_venda, cliente, valor_total)
        VALUES (?, ?, ?)
    """, (data_venda, cliente, total))
    venda_id = cursor.lastrowid

    
    for item in itens:
        subtotal = item["quantidade"] * item["valor_unitario"]
        cursor.execute("""
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, valor_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (venda_id, item["produto_id"], item["quantidade"],
              item["valor_unitario"], subtotal))

        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    conexao.commit()
    conexao.close()
    return venda_id


def listar_vendas():
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id, data_venda, cliente, valor_total
        FROM vendas
        ORDER BY data_venda DESC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]


def itens_da_venda(venda_id):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT iv.id, iv.venda_id, p.nome AS produto, iv.quantidade,
               iv.valor_unitario, iv.subtotal
        FROM itens_venda iv
        JOIN produtos p ON p.id = iv.produto_id
        WHERE iv.venda_id = ?
    """, (venda_id,))
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]




def produtos_mais_vendidos(limite=5):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT p.nome AS produto, SUM(iv.quantidade) AS total_vendido
        FROM itens_venda iv
        JOIN produtos p ON p.id = iv.produto_id
        GROUP BY p.id
        ORDER BY total_vendido DESC
        LIMIT ?
    """, (int(limite),))
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]


def vendas_por_categoria():
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT COALESCE(p.categoria, 'Sem categoria') AS categoria,
               SUM(iv.subtotal) AS total
        FROM itens_venda iv
        JOIN produtos p ON p.id = iv.produto_id
        GROUP BY p.categoria
        ORDER BY total DESC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]


def faturamento_por_mes():
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT substr(data_venda, 1, 7) AS mes,
               SUM(valor_total) AS total
        FROM vendas
        GROUP BY mes
        ORDER BY mes ASC
    """)
    linhas = cursor.fetchall()
    conexao.close()
    return [dict(row) for row in linhas]
