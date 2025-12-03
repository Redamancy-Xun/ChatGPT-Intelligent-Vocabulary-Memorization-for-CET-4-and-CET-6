import re
import urllib.error
import urllib.request
import pandas as pd

import xlwt
from bs4 import BeautifulSoup

# 爬取的数据格式
findspan = re.compile(r'<span.*?>(.*)</span>', re.S)
findp = re.compile(r'<p data-pid=".*?"><b>(.*?)</b>：(.*?)</p>', re.S)

# 爬取的数据来源
url1 = "https://zhuanlan.zhihu.com/p/691112354#/"
url2 = "https://zhuanlan.zhihu.com/p/690535518#/"
url3 = "https://zhuanlan.zhihu.com/p/695945343#/"
url4 = "https://zhuanlan.zhihu.com/p/695929751#/"
url5 = "https://zhuanlan.zhihu.com/p/695907792#/"
url6 = "https://zhuanlan.zhihu.com/p/695890992#/"
url7 = "https://zhuanlan.zhihu.com/p/695833449#/"
url8 = "https://zhuanlan.zhihu.com/p/695782989#/"
url9 = "https://zhuanlan.zhihu.com/p/695672827#/"
url10 = "https://zhuanlan.zhihu.com/p/695628074#/"
url11 = "https://zhuanlan.zhihu.com/p/695494963#/"
url12 = "https://zhuanlan.zhihu.com/p/695473617#/"
url13 = "https://zhuanlan.zhihu.com/p/695457412#/"
url14 = "https://zhuanlan.zhihu.com/p/695408974#/"
url15 = "https://zhuanlan.zhihu.com/p/695397140#/"
url16 = "https://zhuanlan.zhihu.com/p/695238259#/"
url17 = "https://zhuanlan.zhihu.com/p/695213896#/"
url18 = "https://zhuanlan.zhihu.com/p/695056752#/"
url19 = "https://zhuanlan.zhihu.com/p/695030306#/"
url20 = "https://zhuanlan.zhihu.com/p/695014222#/"

# 请求指定URL并返回HTML内容
def askURL(url):
    # 模拟浏览器头部信息
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    # 请求
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        # 使用urllib.request.urlopen发送请求并获取响应
        response = urllib.request.urlopen(request)
        # 读取响应内容并解码
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# 爬取网页
def getDate(url):
    datalist = []
    html = askURL(url)
    # 解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('p'):
        item = str(item)
        inq = re.findall(findp, item)
        if len(inq) == 0 or len(inq[0]) != 2:
            continue
        data = [inq[0][0], inq[0][1]]
        print(data)
        datalist.append(data)
    print(datalist)
    return datalist

# 保存数据（首次保存）
def saveData(datalist, savepath):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('train', cell_overwrite_ok=True)
    col = ("prompt", "completion")
    for i in range(0, 2):
        worksheet.write(0, i, col[i])
    for i in range(0, len(datalist)):
        print("第%d条" % (i + 1))
        data = datalist[i]
        data[0] = ("你是一位教授学生趣味记忆四六级英语单词的老师，请你根据艾宾浩斯遗忘曲线来辅助我们高效记忆四六级单词，要求每个单词有相关的解释和一个有趣的记忆方法。"
                   "如：单词：amiable\n记忆方法：am+i+able，可爱的、亲切的；\n接下来请你来趣味教授单词：" + data[0])
        data[1] = ("单词：" + data[0] + "\n记忆方法：" + data[1])
        print(data)
        if len(data) != 2:
            continue
        for j in range(0, 2):
            worksheet.write(i + 1, j, data[j])

    workbook.save(savepath)

# 保存数据（追加保存）
# 这个函数实际上已经可以替代上面的saveData，已包含了上面的功能
def addData(new_datalist, savepath):
    # 读取已有的Excel文件
    try:
        df = pd.read_excel(savepath)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["prompt", "completion"])  # 如果文件不存在，创建一个空的DataFrame

    # 处理新数据
    for i in range(0, len(new_datalist)):
        word = new_datalist[i][0]
        new_datalist[i][0] = ("你是一位教授学生趣味记忆四六级英语单词的老师，请你根据艾宾浩斯遗忘曲线来辅助我们高效记忆四六级单词，要求每个单词有相关的解释和一个有趣的记忆方法。"
                              "如：单词：amiable\n记忆方法：am+i+able，可爱的、亲切的；\n接下来请你来趣味教授单词：" + word)
        new_datalist[i][1] = ("单词：" + word + "\n记忆方法：" + new_datalist[i][1])

    # 将新数据添加到DataFrame中
    new_data = pd.DataFrame(new_datalist, columns=["prompt", "completion"])
    df = df._append(new_data, ignore_index=True)

    # 保存DataFrame到Excel文件
    df.to_excel(savepath, index=False)


def main():
    # 保存路径
    savepath = "../document/trainData.xlsx"

    # 爬取数据
    for i in range(1, 21):
        url = eval("url" + str(i))
        datalist = getDate(url)
        addData(datalist, savepath)


if __name__ == '__main__':
    main()
    print("爬取完毕")
