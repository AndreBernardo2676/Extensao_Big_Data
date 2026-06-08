# Sistema de Controle de Vendas e Estoque

Projeto acadêmico desenvolvido em **Python** com **Tkinter** (interface gráfica),
**SQLite** (banco de dados local), **Pandas** + **Openpyxl** (importação/exportação Excel)
e **Matplotlib** (gráficos do dashboard).

---

## Tecnologias utilizadas

- Python 3.13
- Tkinter (padrão da linguagem)
- SQLite (padrão da linguagem)
- Pandas
- Openpyxl
- Matplotlib

---

## Estrutura do Projeto

```
Projeto_Vendas/
│
├── main.py                       # Ponto de entrada (login + tela principal)
│
├── database/
│   ├── conexao.py                # Conexão com SQLite
│   └── criar_banco.py            # Cria tabelas se não existirem
│
├── models/
│   ├── produto.py                # Classe Produto
│   ├── venda.py                  # Classe Venda
│   └── item_venda.py             # Classe ItemVenda
│
├── controllers/
│   ├── produto_controller.py     # CRUD de produtos
│   ├── estoque_controller.py     # Entrada/Ajuste/Consulta de estoque
│   └── venda_controller.py       # Registro e relatórios de vendas
│
├── views/
│   ├── tela_principal.py         # Menu principal
│   ├── tela_produtos.py          # Cadastro/edição/exclusão/pesquisa
│   ├── tela_estoque.py           # Gestão de estoque
│   ├── tela_vendas.py            # Carrinho e finalização de venda
│   ├── tela_relatorios.py        # Relatórios + exportação Excel
│   └── tela_dashboard.py         # Gráficos com Matplotlib
│
├── utils/
│   ├── importar_excel.py         # Importação Excel via Pandas
│   └── exportar_excel.py         # Exportação Excel via Openpyxl
│
├── banco/
│   └── vendas.db                 # Criado automaticamente na 1ª execução
│
├── requirements.txt
├── README.md
└── PowerBI_Instrucoes.txt
```

---

## Como executar

### 1. Pré-requisitos
- Ter **Python 3.13** instalado.
- (Recomendado) criar um ambiente virtual.

### 2. Instalar dependências

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

> Observação: `tkinter` e `sqlite3` já vêm instalados com o Python padrão.

### 3. Executar o sistema

```bash
python main.py
```

### 4. Login

- **Usuário:** `admin`
- **Senha:** `admin`

---

## Funcionalidades

### Produtos
- Cadastrar, editar, excluir, pesquisar e listar produtos (Treeview).

### Estoque
- Entrada de estoque
- Ajuste manual de estoque
- Consulta com destaque para produtos com estoque baixo (≤ 5)

### Vendas
- Selecionar produto → informar quantidade → adicionar ao carrinho
- Cálculo automático de subtotal e total
- Finalização: registra a venda, os itens e **abate o estoque automaticamente**
- **Não permite venda com estoque insuficiente**

### Relatórios
- Produtos cadastrados
- Estoque atual
- Produtos com estoque baixo
- Histórico de vendas
- **Exportação para Excel (.xlsx)**

### Importação Excel
A planilha deve conter as colunas:

```
Data da Venda | Produto | Categoria | PrecoUnitario | Marca |
Qtd. Vendida | Nome | Sobrenome | País | Continente
```

Acesse o menu **Importar Excel** na tela principal para escolher o arquivo.

### Dashboard
Três gráficos prontos com Matplotlib:
- Produtos mais vendidos (barras)
- Vendas por categoria (pizza)
- Faturamento por mês (linha)

---

## Power BI

O banco SQLite gerado em `banco/vendas.db` pode ser conectado ao Power BI.
Veja o arquivo **`PowerBI_Instrucoes.txt`** para o passo a passo de conexão
e medidas DAX prontas (Faturamento Total, Quantidade Vendida, Ticket Médio).

---

## Observações Acadêmicas

- Projeto desenvolvido com foco em simplicidade, clareza e atendimento aos requisitos de Projeto de Extensão.
- Sem uso de frameworks web, APIs REST ou tecnologias corporativas.
