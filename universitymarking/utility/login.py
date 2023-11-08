import requests
import universitymarking.utility.config as cfg


def login():
    body = {"device": "pc", "loginType": "web",
            "username": cfg.username, "password": cfg.password}
    loginurl = cfg.baseurl + "/system/login/in"
    result = requests.post(url=loginurl, json=body, headers=cfg.headers).json()
    return result['result']['accessToken']


if __name__ == '__main__':
    result = login()
    print(result)
