import json
import numpy as np
import cv2

import myutils


def cv_show(name, img):
    cp_img = img.copy()
    naturalshape = cp_img.shape
    width = int(naturalshape[1] / 2)
    height = int(naturalshape[0] / 2)
    cp_img = cv2.resize(cp_img, (width, height))
    cv2.imshow(name, cp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def chulixuesheng():
    # 读取一个模板图像
    img = cv2.imread("./images/11090927112810001_full_2.jpg")
    # cv_show('img', img)
    # 灰度图
    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv_show('ref', ref)
    # 二值图像
    ref = cv2.threshold(ref, 100, 255, cv2.THRESH_BINARY)[1]
    # cv_show('ref', ref)
    # 计算轮廓
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
    # 返回的list中每个元素都是图像中的一个轮廓

    refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # refCnts = myutils.sort_contours(refCnts, method="left-to-right")[0]  # 排序，从左到右，从上到下
    refCnts = myutils.getfour(refCnts)  # 排序，从左到右，从上到下
    cv2.drawContours(img, refCnts, -1, (0, 0, 255), 10)
    cv_show('img', img)

    minx, miny, maxx, maxy = myutils.getsigedian(refCnts)
    img = img[miny: maxy, minx:maxx]
    cv_show('img', img)
    return minx, miny, maxx, maxy, img


if __name__ == '__main__':
    with open('./gd/dtkxx.json', encoding='utf-8') as f:
        content = json.load(f)
    bjdlist = content['gsdy'][0]['bjd']
    minx, miny, maxx, maxy = myutils.getgsdysigedian(bjdlist)
    img = cv2.imread("./gd/sample_full_1.jpg")
    img = img[miny: maxy, minx:maxx]
    # cv_show('img', img)
    imgglobalX = maxx - minx
    imgglobalY = maxy - miny

    # 学生图像
    xsminx, xsminy, xsmaxx, xsmaxy, xsimg = chulixuesheng()
    # 一共4个坐标点
    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = [xsminx, xsminy]
    rect[1] = [xsmaxx, xsminy]
    rect[2] = [xsmaxx, xsmaxy]
    rect[3] = [xsminx, xsmaxy]

    # 图像变换
    dst = np.array([
        [0 / 1.0, 0 / 1.0],
        [imgglobalX / 1.0, 0 / 1.0],
        [imgglobalX / 1.0, imgglobalY / 1.0],
        [0 / 1.0, imgglobalY / 1.0]
    ], dtype="float32")

    print("原始位置:", rect)
    print("变换后位置:", dst)
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(xsimg, M, (imgglobalX, imgglobalY))
    cv_show('img', warped)
