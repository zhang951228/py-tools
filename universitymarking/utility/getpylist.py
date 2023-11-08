import requests
import universitymarking.utility.config as cfg


def getpylist(accesstoken: str):
    """
    获取评阅列表
    :param accesstoken:
    :return:
    """
    tokenheaders = {"Accesstoken": accesstoken}
    tokenheaders.update(cfg.headers)

    body = {"kszt": "1", "zjxkh": True, "kkdm": ""}
    url = cfg.baseurl + "/exam/py/list"
    result = requests.post(url=url, json=body, headers=tokenheaders).json()
    return result['result']['records']


def getksstdetail(accesstoken: str, ksid: int, stbh: int):
    tokenheaders = {"Accesstoken": accesstoken}
    url = cfg.baseurl + "/exam/py/detail"
    stbhlist = [stbh]
    body = {"ksid": ksid, "stbhList": stbhlist}
    result = requests.post(url=url, json=body, headers=tokenheaders).json()
    return result['result']
