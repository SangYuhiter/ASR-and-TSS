# -*- coding: utf-8 -*-
"""
@File  : PollingASR.py
@Author: SangYu
@Date  : 2019/4/2 10:08
@Desc  : 使用轮询的方式访问语音识别平台的接口,多平台，多用户
"""
import pickle
import os
import time
from ASRBaidu import asr_api_pro_baidu
from ASRXunFei import asr_api_xunfei
from multiprocessing import Process, Queue, Pool


def save_asr_user_info(user_info: dict):
    """
    保存语音识别平台的用户信息(platform_name,app_id,api_key,secret_key),添加模式
    :param user_info: 字典模式，存储用户的相关信息
    :return:
    """
    # 若user_infos 不存在，创建并添加空列表
    if not os.path.exists("user_infos"):
        with open("user_infos", "wb") as p_file:
            pickle.dump([], p_file)

    # 读出文件内容，判断内容是否重复，不重复才进行添加
    with open("user_infos", "rb") as p_file:
        info_data = pickle.load(p_file)
    if user_info not in info_data:
        info_data.append(user_info)

    # 信息写入
    with open("user_infos", "wb") as p_file:
        pickle.dump(info_data, p_file)


def load_asr_user_info() -> dict:
    """
    载入语音识别平台的用户信息
    :return: 用户信息字典列表
    """
    with open("user_infos", "rb") as p_file:
        info_data = pickle.load(p_file)
    return info_data


def asr_by_polling(q_info: Queue, q_result: Queue, file_id: int, file_path: str) -> str:
    """
    语音识别轮询
    :param q_info:用户信息队列
    :param q_result:返回信息队列
    :param file_path: 语音文件路径
    :return: 语音识别结果
    """
    print("run task %s..." % os.getpid())
    result = None
    while q_info.empty():
        time.sleep(0.1)
    info = q_info.get(True)
    if info["platform_name"] == "Baidu":
        result = asr_api_pro_baidu(info, file_path)
        q_result.put({"from": "Baidu", "file_id": file_id, "result": result})
        q_info.put(info)
    elif info["platform_name"] == "XunFei":
        result = asr_api_xunfei(info, file_path)
        q_result.put({"from": "XunFei", "file_id": file_id, "result": result})
        q_info.put(info)


if __name__ == '__main__':
    q_info = Queue()
    q_result = Queue()
    for info in load_asr_user_info():
        q_info.put(info)
    audio_files = [
        "audio/info/info1.pcm",
        "audio/info/info2.pcm",
        "audio/info/info3.pcm"]
    for i in range(len(audio_files)):
        proc = Process(target=asr_by_polling, args=(q_info, q_result, i, audio_files[i]))
        proc.start()
    proc.join()
    while not q_result.empty():
        print(q_result.get(True))
