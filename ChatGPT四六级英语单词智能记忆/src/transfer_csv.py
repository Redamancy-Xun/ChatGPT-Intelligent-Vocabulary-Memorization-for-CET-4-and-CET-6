import pandas as pd

def convert_xlsx_to_csv(input_path, output_path):
    # 读取xlsx文件
    df = pd.read_excel(input_path)

    # 写入csv文件
    df.to_csv(output_path, index=False)

# 定义输入和输出文件路径
input_path = '../document/trainData.xlsx'  # 输入的xlsx文件路径
output_path = '../document/trainData.csv'  # 输出的csv文件路径

# 调用函数进行文件转换
convert_xlsx_to_csv(input_path, output_path)