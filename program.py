import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings


# 静默处理所有警告
warnings.filterwarnings("ignore")

def process_url(url):
    try:
        # 发送请求获取 HTML 内容
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查 HTTP 请求是否成功

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取所有 <h2> 标签
        h2_tags = soup.find_all('h2')

        # 设置文件名为第四个 <h2> 标签的内容
        if len(h2_tags) >= 4:
            file_name = f"{h2_tags[3].get_text(strip=True)}"
        else:
            file_name = "website_content.txt"  # 默认文件名

        # 替换非法字符
        file_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in file_name)
        file_name = f"{file_name}.txt"
        # 打开文件以保存内容
        with open(file_name, "w", encoding="utf-8") as file:
            # 遍历 body 中的所有元素，按顺序处理
            for element in soup.body.descendants:
                if element.name in ['h2', 'p', 'table', 'li']:
                    if element.name == 'h2':
                        # 保存 <h2> 标签内容
                        text = element.get_text(strip=True)
                        file.write(f"<h2>: {text}\n")
                    elif element.name == 'p':
                        # 保存 <p> 标签内容
                        text = element.get_text(strip=True)
                        file.write(f"<p>: {text}\n")
                    elif element.name == 'li':
                        # 保存 <li> 标签内容
                        text = element.get_text(strip=True)
                        file.write(f"<li>: {text}\n")
                    elif element.name == 'table':
                        # 尝试将表格内容解析为 DataFrame 并保存
                        try:
                            df = pd.read_html(str(element))[0]
                            file.write(f"<table>:\n{df.to_string(index=False)}\n")
                        except ValueError:
                            file.write("<table>: Unable to parse table content.\n")
        print(f"\n网站内容已保存到 '{file_name}'。")
    except requests.exceptions.RequestException as e:
        print(f"获取网站内容时出错: {e}")

if __name__ == "__main__":
    input_file = "urls.txt"
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()
            urls = content.split(",")
            # Process each URL
            for url in urls:
                if url.strip():
                    process_url(url)
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
