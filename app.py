import json

from flask import Flask
from flask import render_template, send_from_directory, request, make_response, jsonify, redirect, url_for
import os
import time
from datetime import datetime

from my_function import get_file_base64

# 全局变量 共享的文件夹路径 可以根据需求更改
DIRECTORY_PATH = r"F:\桌面\电子证照第三方服务模拟"

# 创建项目
app = Flask(__name__)
app.config['SECURE_KEY'] = 'askydiqyddiudhiudiwuhdhdyjqoijd'

pdf_file_data = get_file_base64('道路运输经营许可证.pdf')


# 获取文件信息的函数
def get_files_data():
    files = []
    for i in os.listdir(DIRECTORY_PATH):
        if len(i.split(".")) == 1:  # 判断此文件是否为一个文件夹
            continue

        # 拼接路径
        file_path = DIRECTORY_PATH + "/" + i
        name = i
        size = os.path.getsize(file_path)  # 获取文件大小
        ctime = time.localtime(os.path.getctime(file_path))  # 格式化创建当时的时间戳

        # 列表信息
        files.append({
            "name": name,
            "size": size,
            "ctime": "{}年{}月{}日".format(ctime.tm_year, ctime.tm_mon, ctime.tm_mday),  # 拼接年月日信息
        })
    return files


@app.route("/")
def index():
    """共享文件主页"""
    return render_template("index.html", files=get_files_data())


@app.route("/download_file/<filename>")
def file_content(filename):
    """下载文件的URL"""
    if filename in os.listdir(DIRECTORY_PATH):  # 如果需求下载文件存在
        # 发送文件 参数：文件夹路径，文件路径，文件名
        return send_from_directory(DIRECTORY_PATH, DIRECTORY_PATH + "/" + filename, filename)
    else:
        # 否则返回错误页面
        return render_template("download_error.html", filename=filename)


@app.route("/upload_file", methods=['GET', 'POST'])
def upload():
    """上传文件的URL 支持GET/POST请求"""
    if request.method == "POST":
        # 获取文件 拼接存储路径并保存
        upload_file = request.files.get("upload_file")
        upload_file.save(os.path.join(DIRECTORY_PATH, upload_file.filename))
        #  返回上传成功的模板
        return render_template("upload_ok.html", filename=upload_file.filename)
        # 上传的网页
    return render_template("upload.html")


@app.route("/GatewayMsg/http/api/proxy/invoke", methods=['GET', 'POST'])
def login():
    x_tif_serviceId = request.headers.get('x-tif-serviceId')
    access_token = request.args.get('access_token')
    req_data = request.get_data(parse_form_data=True, as_text=True)
    print('请求数据', 'x_tif_serviceId', x_tif_serviceId, 'access_token', access_token, 'req_data', req_data)
    message = {}
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    message['ack_code'] = 'SUCCESS'
    message['errors'] = []
    message['timestamp'] = timestamp
    if x_tif_serviceId == 'D1593589959893':  # 登录
        message['access_token'] = '1234567890'
    if x_tif_serviceId == 'D1597131569652':  # 制证签发数据
        message['sign'] = 'null'
        message['sign_method'] = 'null'
        message['correlation_id'] = '2b7bcfde-f621-4945-b282-f49873311436'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
        message['data'] = {"license_code": "440000201800000001",
                           "auth_code": "440200106000201180103110507XCV7"}
    elif x_tif_serviceId == 'D1597132378846':  # 创建制证数据
        message['access_token'] = '1234567890'
        message['correlation_id'] = 'null'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
        message['data'] = {'license_code': '440000201800000001',
                           'auth_code': '440200106000201180103110507XCV7'}
    elif x_tif_serviceId == 'D1597132425087':  # 签发一张证照
        message['sign'] = 'null'
        message['sign_method'] = 'null'
        message['correlation_id'] = 'null'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
    elif x_tif_serviceId == 'D1597132462444':  # 修改制证数据
        message['sign'] = 'null'
        message['sign_method'] = 'null'
        message['correlation_id'] = 'null'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
    elif x_tif_serviceId == 'D1597132486022':  # 删除制证数据
        message['correlation_id'] = 'null'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
    elif x_tif_serviceId == 'D1597135080112':  # 废止一张证照
        message['correlation_id'] = 'null'
        message['response_id'] = 'dfc1be0d-ca4f-4a98-bb71-bad846434f8d'
    elif x_tif_serviceId == 'D1593590066290':  # 归档电子文件
        message['data'] = {"file_name": "44000016D000020.pdf", "file_data": pdf_file_data}
    print('返回数据', message)
    return make_response(jsonify(message), 200)


if __name__ == '__main__':
    # 在局域网上开启端口
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=('cert/server.crt', 'cert/server.key'))
