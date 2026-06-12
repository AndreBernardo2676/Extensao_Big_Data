import pandas as pd
from datetime import datetime

from database.conexao import conectar


COLUNAS_ESPERADAS = [
    "Data da Venda", "Produto", "Categoria", "PrecoUnitario",
    "Marca", "Qtd. Vendida", "Nome", "Sobrenome", "País", "Continente",
]


def _formatar_data(valor):
    
    if pd.isna(valor):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        dt = pd.to_datetime(valor)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _buscar_ou_criar_produto(cursor, nome, categoria, marca, preco, qtd):
    cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
    linha = cursor.fetchone()

    if linha:
        cursor.execute("""
            UPDATE produtos
            SET estoque = estoque + ?
            WHERE id = ?
        """, (qtd, linha["id"]))

        return linha["id"]

    cursor.execute("""
        INSERT INTO produtos
        (nome, categoria, marca, preco, estoque)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, categoria, marca, float(preco), qtd))

    return cursor.lastrowid


def importar_planilha_excel(caminho_arquivo):
  
    df = pd.read_excel(caminho_arquivo)

    
    faltando = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
    if faltando:
        raise ValueError(
            "A planilha não contém as colunas esperadas. "
            f"Faltando: {', '.join(faltando)}"
        )

    conexao = conectar()
    cursor = conexao.cursor()
    importados = 0

    for _, linha in df.iterrows():
        try:
            nome_prod = str(linha["Produto"]).strip()
            if not nome_prod or nome_prod.lower() == "nan":
                continue

            categoria = str(linha["Categoria"]).strip() if not pd.isna(linha["Categoria"]) else ""
            marca = str(linha["Marca"]).strip() if not pd.isna(linha["Marca"]) else ""
            preco = float(linha["PrecoUnitario"]) if not pd.isna(linha["PrecoUnitario"]) else 0.0
            qtd = int(linha["Qtd. Vendida"]) if not pd.isna(linha["Qtd. Vendida"]) else 0
            if qtd <= 0:
                continue

            
            nome_cli = str(linha["Nome"]).strip() if not pd.isna(linha["Nome"]) else ""
            sobrenome = str(linha["Sobrenome"]).strip() if not pd.isna(linha["Sobrenome"]) else ""
            cliente = f"{nome_cli} {sobrenome}".strip() or "Cliente Importado"

            data_venda = _formatar_data(linha["Data da Venda"])

            
            produto_id = _buscar_ou_criar_produto(
                cursor, nome_prod, categoria, marca, preco, qtd
)

            valor_total = qtd * preco

            
            cursor.execute("""
                INSERT INTO vendas (data_venda, cliente, valor_total)
                VALUES (?, ?, ?)
            """, (data_venda, cliente, valor_total))
            venda_id = cursor.lastrowid

            
            cursor.execute("""
                INSERT INTO itens_venda
                    (venda_id, produto_id, quantidade, valor_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (venda_id, produto_id, qtd, preco, valor_total))

            
            # cursor.execute(
            #     "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            #     (qtd, produto_id),
            # )

            importados += 1
        except Exception:
           
            continue

    conexao.commit()
    conexao.close()
    return importados
