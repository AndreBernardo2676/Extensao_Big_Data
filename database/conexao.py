import os
import sqlite3



PASTA_BANCO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "banco")
CAMINHO_BANCO = os.path.join(PASTA_BANCO, "vendas.db")


def conectar():
   
    if not os.path.exists(PASTA_BANCO):
        os.makedirs(PASTA_BANCO)

    conexao = sqlite3.connect(CAMINHO_BANCO)
    
    conexao.execute("PRAGMA foreign_keys = ON")
    
    conexao.row_factory = sqlite3.Row
    return conexao
