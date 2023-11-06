import json
import numpy as np
import cv2

import myutil


def cv_show(name, img):
    cp_img = img.copy()
    naturalshape = cp_img.shape
    width = int(naturalshape[1] / 1)
    height = int(naturalshape[0] / 1)
    cp_img = cv2.resize(cp_img, (width, height))
    cv2.imshow(name, cp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def analysisTempleteStxx(jxxxjsonlist, binaryImg, offsetx, offsety):
    allstdict = {}
    # 循环题组
    for tzjson in jxxxjsonlist:
        # 循环各个试题
        for stxx in tzjson['stxx']:
            if stxx['stlx'] not in (1, 2, 3):
                continue
            xxdict = {}
            cntpt = 0
            for positionArea in stxx['positionArea']:
                # 统计当前选项占的像素点
                mask = np.zeros(binaryImg.shape, dtype="uint8")
                ltpt = (positionArea['location'][0][0] - offsetx, positionArea['location'][0][1] - offsety)
                rbpt = (positionArea['location'][1][0] - offsetx, positionArea['location'][1][1] - offsety)
                cv2.rectangle(mask, ltpt, rbpt, (255, 255, 255), -1)
                cntpt += cv2.countNonZero(mask)
                mask = cv2.bitwise_and(binaryImg, binaryImg, mask=mask)
                white = cv2.countNonZero(mask)
                xxdict[positionArea['index']] = white
            xxdict['CNT'] = cntpt / len(stxx['positionArea'])
            allstdict[stxx['stbh']] = xxdict
    return allstdict


def analysisXsFill(jxxxjsonlist, bmh, pagenum, offsetx, offsety, targetWidth, targetHeight):
    """ 加载实际待识别的学生图像 """
    # 读取一个模板图像
    img = cv2.imread(f"./weihai/{bmh}/{bmh}_full_{pagenum}.jpg")
    # cv_show('img', img)
    # 灰度图
    stuImgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv_show('ref', ref)
    # 二值图像
    stuImgBinary = cv2.threshold(stuImgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show('ref', ref)
    # 计算轮廓
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
    # 返回的list中每个元素都是图像中的一个轮廓
    refCnts, hierarchy = cv2.findContours(stuImgBinary.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    nps = myutil.identifyfourDingdian(refCnts, img.shape[1], img.shape[0])  # 排序，从左到右，从上到下

    dst = np.array([
        [0 / 1.0, 0 / 1.0],
        [targetWidth / 1.0, 0 / 1.0],
        [targetWidth / 1.0, targetHeight / 1.0],
        [0 / 1.0, targetHeight / 1.0]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(nps, dst)
    warped = cv2.warpPerspective(stuImgBinary, M, (targetWidth, targetHeight))
    return analysisTempleteStxx(jxxxjsonlist, warped, offsetx, offsety)


def main():
    # 读取答题卡json字符串
    with open('./sanfanggsdy.json', encoding='utf-8') as f:
        content = json.load(f)
    bjdlist = content['gsdy'][0]['bjd']
    minx, miny, maxx, maxy = myutil.useDtkbjdListgetGsdysigedingdian(bjdlist)
    # 读取答题卡图片
    img = cv2.imread("./weihai/sample/sample_full_1.jpg")
    # 使用 x y 的最大最小值,切割格式定义的答题卡,验证是否套准了
    sliceTempleteImg = img[miny: maxy, minx:maxx]
    sliceTempleteImgGray = cv2.cvtColor(sliceTempleteImg, cv2.COLOR_BGR2GRAY)
    # 二值图像
    # ref = cv2.threshold(ref, 100, 255, cv2.THRESH_BINARY)[1]
    sliceTempleteImgBinary = cv2.threshold(sliceTempleteImgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # 提前计算出模板中的各个位置的白色点数量
    templeteStbh2xx2wilteMap = analysisTempleteStxx(content['jxxx'], sliceTempleteImgBinary, minx, miny)
    # 计算出中心/期望图像的宽度/高度
    targetWidth = maxx - minx
    targetHeight = maxy - miny
    xsStbh2xx2wilteMap = analysisXsFill(content['jxxx'], "014402210070615420001", 1, minx, miny, targetWidth,
                                        targetHeight)
    print(templeteStbh2xx2wilteMap)
    print(xsStbh2xx2wilteMap)
    determineStuSel(templeteStbh2xx2wilteMap, xsStbh2xx2wilteMap)



def determineStuSel(templeteStbh2xx2wilteMap, xsStbh2xx2wilteMap):
    for (templeteSt, xsSt) in zip(templeteStbh2xx2wilteMap.items(), xsStbh2xx2wilteMap.items()):
        mean = templeteSt[1]['CNT']
        proportionList = []
        for (templeteXx, Xsxx) in zip(templeteSt[1].items(), xsSt[1].items()):
            if templeteXx[0] == 'CNT':
                continue
            zhanbi = ((mean - templeteXx[1]) - (mean - Xsxx[1])) / templeteXx[1]
            proportionList.append(zhanbi)
        proportionList.sort(reverse=True)
        print("试题编号:", templeteSt[0], "可能的选项:", proportionList)


def drawBoundingRect(jxxxjsonlist, binaryImg, offsetx, offsety):
    print("offsetx:", offsetx, "offsety:", offsety)
    binaryImg_copy = binaryImg.copy()
    allstdict = {}
    # 循环题组
    for tzjson in jxxxjsonlist:
        # 循环各个试题
        for stxx in tzjson['stxx']:
            if stxx['stlx'] not in (1, 2, 3):
                continue
            xxdict = {}
            cntpt = 0
            for positionArea in stxx['positionArea']:
                # 统计当前选项占的像素点
                mask = np.zeros(binaryImg.shape, dtype="uint8")
                ltpt = (positionArea['location'][0][0] - offsetx, positionArea['location'][0][1] - offsety)
                rbpt = (positionArea['location'][1][0] - offsetx, positionArea['location'][1][1] - offsety)
                cv2.rectangle(mask, ltpt, rbpt, (255, 255, 255), -1)
                cntpt += cv2.countNonZero(mask)
                mask = cv2.bitwise_and(binaryImg, binaryImg, mask=mask)
                print("ltpt: ", ltpt, "rbpt:", rbpt)
                binaryImg_copy = cv2.rectangle(binaryImg_copy, ltpt, rbpt, (0, 0, 255), -1)
                white = cv2.countNonZero(mask)
                xxdict[positionArea['index']] = white
            xxdict['CNT'] = cntpt / len(stxx['positionArea'])
            allstdict[stxx['stbh']] = xxdict
    cv_show("binaryImg_copy", binaryImg_copy)
    return allstdict


if __name__ == '__main__':
    main()
