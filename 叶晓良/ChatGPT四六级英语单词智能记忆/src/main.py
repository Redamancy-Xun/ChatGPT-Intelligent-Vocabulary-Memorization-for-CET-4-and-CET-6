import openai
import pandas as pd


# 调用openai的API生成记忆方法
def create(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "你是一位教授学生趣味记忆四六级英语单词的老师，请你根据艾宾浩斯遗忘曲线来辅助我们高效记忆四六级单词，要求每个单词有一个有趣的记忆方法。"
                                          "如：单词：amiable\n记忆方法：am+i+able，可爱的、亲切的；"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# 读取单词列表
df = pd.read_excel('../document/wordList.xlsx')

results = []
count = 0

# 遍历 df 中的每一行，提取单词，构建提示prompt，调用create函数获取有趣的记忆方法answer
for index, row in df.iterrows():
    if count <= 160:
        count += 1
        continue
    if count == 200:
        break
    word = row[1]
    prompt = (f"你是一位教授学生趣味记忆四六级英语单词的老师，请你根据艾宾浩斯遗忘曲线来辅助我们高效记忆四六级单词，要求每个单词有一个有趣的记忆方法。"
              f"如：单词：amiable\n记忆方法：am+i+able，可爱的、亲切的；\n接下来请你来趣味教授单词：{word}")
    answer = create(prompt)
    results.append({'单词': word, '记忆方法': answer})
    count += 1

# 将结果存储到result.xlsx
try:
    df = pd.read_excel("../document/result.xlsx")
except FileNotFoundError:
    # 如果文件不存在，创建一个空的DataFrame
    df = pd.DataFrame(columns=["单词", "记忆方法"])
result_df = pd.DataFrame(results)
result_df = df._append(result_df, ignore_index=True)
result_df.to_excel('../document/result.xlsx', index=False)