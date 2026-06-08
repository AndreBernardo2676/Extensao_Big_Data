from openpyxl import Workbook


def exportar_para_excel(dados, colunas, caminho_destino):
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatorio"

    
    ws.append([str(c).capitalize() for c in colunas])

    
    for d in dados:
        linha = [d.get(c, "") for c in colunas]
        ws.append(linha)

    
    for col_idx, col in enumerate(colunas, start=1):
        max_len = max(
            [len(str(d.get(col, ""))) for d in dados] + [len(col)]
        )
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = max_len + 2

    wb.save(caminho_destino)
