# coding: utf-8
import json

from flask import Flask
from flask import render_template, send_from_directory, request, make_response, jsonify, redirect, url_for
import os
import time
import logging
from datetime import datetime
from loguru import logger
import openai

from my_function import get_file_base64, check_path_exists


openai.api_key = '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'
# 创建项目
app = Flask(__name__)
flasklog = logging.getLogger('werkzeug')
flasklog.disabled = True
cur_path = os.path.split(os.path.realpath(__file__))[0]
check_path_exists(os.path.join(cur_path, 'logs'))
logfile = os.path.join(cur_path, 'logs', 'chatgpt.log')
logger.add(logfile, level="INFO", rotation="500MB", encoding="utf-8", enqueue=True, retention="30 days")


@app.route("/chatgpt", methods=['GET'])
def chatgpt():
    """
    chatgpt
    :return:
    """
    message = {}
    question = request.args.get('QUESTION')
    remote_host = request.remote_addr
    logger.info('主机【{}】请求数据:{}'.format(remote_host, question))
    if question:
        try:
            response = openai.Completion.create(model="text-davinci-003", prompt=question, temperature=0.1, max_tokens=2000)
            result = response.get('choices')[0].get('text')
            message['code'] = 0
            message['result'] = result
        except Exception as e:
            print(str(e))
            message['code'] = 1
            message['result'] = 'ChatGPT调用失败！请重试！'
    else:
        message['code'] = 2
        message['result'] = '请求参数为空！'
    logger.info('主机【{}】问题【{}】答案:{}'.format(remote_host, question, message.get('result')))
    return make_response(jsonify(message), 200)


if __name__ == '__main__':
    # 在局域网上开启端口
    # app.run(host="0.0.0.0", port=8857, debug=True, ssl_context=('cert/server.crt', 'cert/server.key'))
    app.run(host="0.0.0.0", port=5555, debug=True)
