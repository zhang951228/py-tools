import os
from urllib import request
from lxml import etree
import ssl
from urllib.error import HTTPError
import time


def Path(pages: str) -> list:
    return etree.HTML(pages).xpath('.//ul[@class="comma-separated"]/li/text()')


def CreatUrlList(urls: list) -> list:
    lists = []
    for line in urls:
        lists.append(f"https://{line}.ipaddress.com")
    return lists


def GetIp(page_url: str) -> str:
    try:

        context1 = ssl._create_unverified_context()
        r = request.urlopen(page_url, context=context1)
        page = r.read().decode()
        html = Path(page)
        return list(set(html))[0]
    except HTTPError as er:
        print(er.code)


url_list = ["github.com", "github-cloud.s3.amazonaws.com", "codeload.github.com", "github.global.ssl.fastly.net",
            "github-cloud.s3.amazonaws.com"]


if __name__ == '__main__':
    lists_url = CreatUrlList(url_list)
    lists = []
    # 在py文件目录下生产一个host.txt文件以便大家添加Host记录
    path = os.getcwd() + "/host.txt"
    print(path)
    file = open(path, 'w', encoding="utf-8")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    file.write(f"# GitHub网址爬取 {now}\n", )
    for url in lists_url:
        ip = GetIp(url)
        url = ip + "\t" + url.replace("https://", "").replace(".ipaddress.com", "")
        try:
            file.write(url + "\n")
        except Exception as e:
            print(e)
        finally:
            print(url)
    file.close()
    print("GitHub地址爬取完成！")