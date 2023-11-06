import sys

import cv2
import numpy as np


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    return cnts, boundingBoxes


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized


def getlefttopbjd(cnts):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: (b[1][1], b[1][0]), reverse=False))
    return cnts, boundingBoxes


def getlefttopbjds(cnts):
    imgw = 2468
    imgh = 1748
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    rec = []
    reb = []
    for (i, b) in enumerate(boundingBoxes):
        if b[2] > 50 and b[3] > 50:
            continue
        if (imgw / 4) < b[0] and abs(b[0] - imgw) > (imgw / 4):
            continue
        if (imgh / 4) < b[1] and abs(b[1] - imgh) > (imgh / 4):
            continue
        reb.append(b)
        rec.append(cnts[i])
    return rec, reb


def identifyfourDingdian(cnts, imgw, imgh):
    """识别出来四个角"""
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    rec = []
    reb = []
    for (i, b) in enumerate(boundingBoxes):
        if b[2] > 50 and b[3] > 50:
            continue
        if (imgw / 4) < b[0] and abs(b[0] - imgw) > (imgw / 4):
            continue
        if (imgh / 4) < b[1] and abs(b[1] - imgh) > (imgh / 4):
            continue
        # 面积判断
        area = cv2.contourArea(cnts[i])
        if area < 100:
            continue
        # 周长判断
        perimeter = cv2.arcLength(cnts[i], True)
        if perimeter < 40:
            continue
        reb.append(b)
        rec.append(cnts[i])

    # 寻找左上角
    lefttopcnts = rec[0]
    lefttopboundRect = reb[0]
    for (c, b) in zip(rec, reb):
        if b[0] + 2 * b[1] < lefttopboundRect[0] + 2 * lefttopboundRect[1]:
            lefttopcnts = c
            lefttopboundRect = b

    # 寻找右上角
    righttopcnts = rec[0]
    righttopboundRect = reb[0]
    for (c, b) in zip(rec, reb):
        if imgw - b[0] + 2 * b[1] < imgw - righttopboundRect[0] + 2 * righttopboundRect[1]:
            righttopcnts = c
            righttopboundRect = b
    # 寻找左下角
    leftbottomcnts = rec[0]
    leftbottomboundRect = reb[0]
    for (c, b) in zip(rec, reb):
        if b[0] + imgh - 2 * b[1] < leftbottomboundRect[0] + imgh - 2 * leftbottomboundRect[1]:
            leftbottomcnts = c
            leftbottomboundRect = b

    # 寻找右下角
    rightbottomcnts = rec[0]
    rightbottomboundRect = reb[0]
    for (c, b) in zip(rec, reb):
        if imgw - b[0] + imgh - 2 * b[1] < imgw - rightbottomboundRect[0] + imgh - 2 * rightbottomboundRect[1]:
            rightbottomcnts = c
            rightbottomboundRect = b

    sigedian = []
    sigedian.append(lefttopcnts)
    sigedian.append(righttopcnts)
    sigedian.append(rightbottomcnts)
    sigedian.append(leftbottomcnts)

    boundingBoxes = [cv2.boundingRect(c) for c in sigedian]
    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = [boundingBoxes[0][0], boundingBoxes[0][1]]
    rect[1] = [boundingBoxes[1][0] + boundingBoxes[1][2], boundingBoxes[1][1]]
    rect[2] = [boundingBoxes[2][0] + boundingBoxes[2][2], boundingBoxes[2][1] + boundingBoxes[2][3]]
    rect[3] = [boundingBoxes[3][0], boundingBoxes[3][1] + boundingBoxes[3][3]]

    return rect


def useDtkbjdListgetGsdysigedingdian(bjdlist):
    """解析答题卡json串中的bjd数组,返回 x y 的最大最小值 """
    minx = sys.maxsize
    miny = sys.maxsize
    maxx = 0
    maxy = 0
    for i in bjdlist:
        for x, y in i['location']:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    return minx, miny, maxx, maxy


def useDtkbjdListgetGsdysigedingdian2(bjdlist, width, height):
    lt = []
    rt = []
    rb = []
    lb = []
    for bjd in bjdlist:
        x = bjd['location'][0][0]
        y = bjd['location'][0][1]
        if x < width / 2 and y < height / 2:
            # 左上角
            lt.append(bjd['location'])
        if x > width / 2 and y < height / 2:
            # 右上角
            rt.append(bjd['location'])
        if x > width / 2 and y > height / 2:
            rb.append(bjd['location'])
        if x < width / 2 and y > height / 2:
            lb.append(bjd['location'])
    # 此处还需要排序取最边边的.
    return lt, rt, rb, lb


def getminmax2(lt, rt, rb, lb):
    minx = sys.maxsize
    miny = sys.maxsize
    maxx = 0
    maxy = 0
    for i in lt:
        for x, y in i:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    for i in rt:
        for x, y in i:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    for i in rb:
        for x, y in i:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    for i in lb:
        for x, y in i:
            minx = min(minx, x)
            miny = min(miny, y)
            maxx = max(maxx, x)
            maxy = max(maxy, y)
    return minx, miny, maxx, maxy



def getrealPot(bjdlist, width, height):
    lt, rt, rb, lb = useDtkbjdListgetGsdysigedingdian2(bjdlist, width, height)
    minx, miny, maxx, maxy = getminmax2(lt, rt, rb, lb)
    realLt = ((lt[0][0][0] - minx) / 1.0, (lt[0][0][1] - miny) / 1.0)
    realRt = ((rt[0][1][0] - minx) / 1.0, (rt[0][0][1] - miny) / 1.0)
    realRb = ((rb[0][1][0] - minx) / 1.0, (rb[0][1][1] - miny) / 1.0)
    realLb = ((lb[0][0][0] - minx) / 1.0, (lb[0][1][1] - miny) / 1.0)
    return realLt, realRt, realRb, realLb, minx, miny, maxx, maxy
