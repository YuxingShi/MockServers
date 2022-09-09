# coding:utf-8
import base64


def get_file_base64(filename):
    with open(filename, 'rb') as fp:
        content = fp.read()
        return base64.encodebytes(content)


if __name__ == '__main__':
    print(get_file_base64('道路运输经营许可证.pdf'))