from database.conexao import conectar
from models.produto import Produto


def cadastrar_produto(nome, categoria, marca, preco, estoque):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, categoria, marca, preco, estoque)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, categoria, marca, float(preco), int(estoque)))
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id


def editar_produto(id_produto, nome, categoria, marca, preco, estoque):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE produtos
        SET nome = ?, categoria = ?, marca = ?, preco = ?, estoque = ?
        WHERE id = ?
    """, (nome, categoria, marca, float(preco), int(estoque), id_produto))
    conexao.commit()
    conexao.close()


def excluir_produto(id_produto):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
    conexao.commit()
    conexao.close()


def listar_produtos():
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos ORDER BY nome")
    linhas = cursor.fetchall()
    conexao.close()

    produtos = []
    for linha in linhas:
        produtos.append(Produto(
            id=linha["id"],
            nome=linha["nome"],
            categoria=linha["categoria"],
            marca=linha["marca"],
            preco=linha["preco"],
            estoque=linha["estoque"],
        ))
    return produtos


def pesquisar_produtos(termo):
    
    conexao = conectar()
    cursor = conexao.cursor()
    termo_like = f"%{termo}%"
    cursor.execute("""
        SELECT * FROM produtos
        WHERE nome LIKE ? OR categoria LIKE ? OR marca LIKE ?
        ORDER BY nome
    """, (termo_like, termo_like, termo_like))
    linhas = cursor.fetchall()
    conexao.close()

    produtos = []
    for linha in linhas:
        produtos.append(Produto(
            id=linha["id"],
            nome=linha["nome"],
            categoria=linha["categoria"],
            marca=linha["marca"],
            preco=linha["preco"],
            estoque=linha["estoque"],
        ))
    return produtos


def buscar_produto_por_id(id_produto):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return None
    return Produto(
        id=linha["id"],
        nome=linha["nome"],
        categoria=linha["categoria"],
        marca=linha["marca"],
        preco=linha["preco"],
        estoque=linha["estoque"],
    )


def buscar_ou_criar_produto(nome, categoria, marca, preco):
    
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
    linha = cursor.fetchone()

    if linha:
        produto_id = linha["id"]
    else:
        cursor.execute("""
            INSERT INTO produtos (nome, categoria, marca, preco, estoque)
            VALUES (?, ?, ?, ?, 0)
        """, (nome, categoria, marca, float(preco)))
        produto_id = cursor.lastrowid

    conexao.commit()
    conexao.close()
    return produto_id
