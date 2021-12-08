import os
import string

from pyexcelerate import Workbook, Color

from core.config import config


def save_data_to_excel_file(columns, docs, id):
    letters = list(string.ascii_uppercase)
    letters+=[letter+letter for letter in letters]
    col_letter = letters[len(columns)-1]

    wb = Workbook()
    ws = wb.new_sheet("data")
    ws.range("A1", f"{col_letter}1").value = [[col for col in columns]]
    ws.range("A1", f"{col_letter}1").style.font.bold = True
    ws.range("A1", f"{col_letter}1").style.fill.background = Color(255, 255, 0, 0)

    row_number = 2
    for doc in docs:
        doc = doc["_source"]
        row = [[doc[col] for col in columns]]
        ws.range(f"A{row_number}", f"{col_letter}{row_number}").value = row
        row_number+=1
    wb.save(config.excel_file_path+f'{id}.xlsx')