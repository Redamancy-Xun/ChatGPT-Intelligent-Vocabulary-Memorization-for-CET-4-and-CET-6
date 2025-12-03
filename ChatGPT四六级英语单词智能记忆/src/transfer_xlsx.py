from docx import Document
import pandas as pd

doc = Document("../document/wordList.docx")

all_data = []
for table in doc.tables:
    data = []
    first_row = True  # 用于跟踪第一行
    for row in table.rows:
        # 跳过第一行
        if first_row:
            first_row = False
            continue
        row_data = []
        for cell in row.cells:
            row_data.append(cell.text)
        data.append(row_data)
    all_data.extend(data)

df = pd.DataFrame(all_data)

# 创建Excel文件
with pd.ExcelWriter('../document/wordList.xlsx') as writer:
    df.to_excel(writer, sheet_name='WordList', index=False)