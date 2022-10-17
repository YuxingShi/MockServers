# coding:utf-8
import os
import base64


def get_file_base64(filename):
    with open(filename, 'rb') as fp:
        content = fp.read()
        return base64.encodebytes(content)


def check_path_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    print(get_file_base64('道路运输经营许可证.pdf'))