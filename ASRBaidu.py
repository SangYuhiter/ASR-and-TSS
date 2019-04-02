# -*- coding: utf-8 -*-
"""
@File  : ASRBaidu.py
@Author: SangYu
@Date  : 2019/4/2 10:57
@Desc  : 百度语音识别接口
"""

import json
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

from aip import AipSpeech

timer = time.perf_counter


class DemoError(Exception):
    pass


# 获取token
# noinspection PyUnresolvedReferences
def fetch_token(api_key: str, secret_key: str, score: str):
    """
    获取鉴权资格
    :param api_key:
    :param secret_key:
    :param score:
    :return:
    """
    token_url = 'http://openapi.baidu.com/oauth/2.0/token'
    params = {'grant_type': 'client_credentials',
              'client_id': api_key,
              'client_secret': secret_key}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(token_url, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        # print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()
    result = json.loads(result_str)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if score and score not in result['scope'].split(' '):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        # print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


# 普通语音api识别
# noinspection PyUnresolvedReferences,PyShadowingBuiltins
def asr_api_baidu(user_info: dict, file_path: str) -> str:
    dev_pid = 1536  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型。根据文档填写PID，选择语言及识别模型
    rate = 16000  # 固定值
    cuid = '123456PYTHON'
    asr_url = 'http://vop.baidu.com/server_api'
    scope = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
    token = fetch_token(user_info["api_key"], user_info["secret_key"], scope)
    # 文件格式
    format = file_path[-3:]  # 文件后缀只支持 pcm/wav/amr
    # speech_data = []
    with open(file_path, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': cuid, 'token': token, 'dev_pid': dev_pid}
    params_query = urlencode(params)

    headers = {
        'Content-Type': 'audio/' + format + '; rate=' + str(rate),
        'Content-Length': length
    }

    url = asr_url + "?" + params_query
    req = Request(url, speech_data, headers)
    try:
        # begin = timer()
        f = urlopen(req)
        result_str = f.read()
        # print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    # print(result_str)
    return json.loads(result_str)


# 语音极速api识别
# noinspection PyUnresolvedReferences,PyShadowingBuiltins
def asr_api_pro_baidu(user_info: dict, file_path: str) -> str:
    dev_pid = 80001
    rate = 16000  # 固定值
    cuid = '123456PYTHON'
    asr_url = 'https://vop.baidu.com/pro_api'
    scope = 'brain_enhanced_asr'  # 有此scope表示有asr能力，没有请在网页里开通极速版
    token = fetch_token(user_info["api_key"], user_info["secret_key"], scope)
    # 文件格式
    format = file_path[-3:]  # 文件后缀只支持 pcm/wav/amr
    # speech_data = []
    with open(file_path, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': cuid, 'token': token, 'dev_pid': dev_pid}
    params_query = urlencode(params)

    headers = {
        'Content-Type': 'audio/' + format + '; rate=' + str(rate),
        'Content-Length': length
    }

    url = asr_url + "?" + params_query
    req = Request(url, speech_data, headers)
    try:
        # begin = timer()
        f = urlopen(req)
        result_str = f.read()
        # print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = str(result_str, 'utf-8')
    # print(result_str)
    return json.loads(result_str)


# 语音SDK识别
# noinspection PyShadowingBuiltins
def asr_sdk_baidu(user_info: dict, file_path: str) -> str:
    # 文件格式
    format = file_path[-3:]  # 文件后缀只支持 pcm/wav/amr
    rate = 16000  # 固定值
    client = AipSpeech(user_info["app_id"], user_info["api_key"], user_info["secret_key"])
    with open(file_path, 'rb') as speech_file:
        speech_data = speech_file.read()
    # begin = timer()
    result = client.asr(speech_data, format, rate, {'dev_pid': 1536})
    # print("Request time cost %f" % (timer() - begin))
    # print(result)
    return result


if __name__ == '__main__':
    # 需要识别的文件
    # ".audio/16k.wav"
    u_info = {"platform_name": "Baidu", "app_id": "15845499", "api_key": "LDUZQI8Fa9ShIdZTXxrjC333",
              "secret_key": "YLubCcZudGKlcHKrgMciqXM7Wlxb3Gl5"}
    AUDIO_FILE = './audio/info/info1.pcm'  # 只支持 pcm/wav/amr
    # 采样率
    print("API普通版")
    result = asr_api_baidu(u_info, AUDIO_FILE)
    print(result)
    print(type(result))
    print("API极速版")
    result = asr_api_pro_baidu(u_info, AUDIO_FILE)
    print(result)
    print(type(result))
    print("SDK实现")
    result = asr_sdk_baidu(u_info, AUDIO_FILE)
    print(result)
    print(type(result))
