# coding:utf-8
import os
import base64
import requests
from bs4 import BeautifulSoup


def get_file_base64(filename):
    with open(filename, 'rb') as fp:
        content = fp.read()
        return base64.encodebytes(content)


def check_path_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def crawler(url: str):
    """

    :param url: 目标网址
    :return:
    """
    # 请求目标网址
    response = requests.get(url)
    # 解析网页
    soup = BeautifulSoup(response.text, 'lxml')
    # 找到所有的a标签
    links = soup.find_all('a')

    # 遍历a标签，获取链接
    for link in links:
        link_url = link.get('href')
        print(link_url)


if __name__ == '__main__':
    print(get_file_base64('道路运输经营许可证.pdf'))