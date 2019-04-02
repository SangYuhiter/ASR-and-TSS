# -*- coding: utf-8 -*-
"""
@File  : ASRXunFei.py
@Author: SangYu
@Date  : 2019/4/2 13:44
@Desc  : 讯飞语音识别接口
"""

import requests
import time
import hashlib
import base64


def getHeader(aue, engineType, user_info):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
    # print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    # print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((user_info["api_key"] + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    # print('checkSum:{}'.format(checkSum))
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': user_info["app_id"],
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    # print(header)
    return header


def getBody(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    # print(data)
    # print('data:{}'.format(type(data['audio'])))
    # print("type(data['audio']):{}".format(type(data['audio'])))
    return data


def asr_api_xunfei(user_info: dict, file_path: str) -> str:
    URL = "http://api.xfyun.cn/v1/service/v1/iat"
    aue = "raw"
    engineType = "sms16k"
    r = requests.post(URL, headers=getHeader(aue, engineType, user_info), data=getBody(file_path))
    return r.content.decode('utf-8')


if __name__ == '__main__':
    f_path = "./audio/info/info1.pcm"
    u_info = {"platform_name": "XunFei", "app_id": "5c22dc4a", "api_key": "bdb820019f9b56fe7cba6663d17863c1"}
    print(asr_api_xunfei(u_info, f_path))
