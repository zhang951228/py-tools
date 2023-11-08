import random

import requests
import universitymarking.utility.config as cfg


def getImg(slid: int, xnxq: int, ksid: int, bmh: int, stbh: int, num: int):
    for i in range(1, num + 1):
        imgurl = (cfg.baseimgurl + str(slid) + "/" + str(xnxq) + "/" + str(ksid) + "/" + str(bmh) + "/" +
                  str(bmh) + "_" + str(stbh) + "_" + str(i) + ".jpg?v=" + str(random.random()))
        result = requests.get(cfg.baseimgurl, imgurl)



if __name__ == '__main__':
    for i in range(1000):
        getImg(10008, 20221, 337, 110909271128100011, 5066, 2)
        print(i)
