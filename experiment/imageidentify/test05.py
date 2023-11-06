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


def analysisXsFill(jxxxjsonlist, bmh, pagenum, lt, rt, rb, lb, aminx, aminy, amaxx, amaxy):
    """ 加载实际待识别的学生图像 """
    # 读取一个模板图像
    img = cv2.imread(f"./weihai/{bmh}/{bmh}_full_{pagenum}.jpg")
    # cv_show('img', img)
    # 灰度图
    stuImgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值图像
    stuImgBinary = cv2.threshold(stuImgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # 初始化卷积核
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    tophat = cv2.morphologyEx(stuImgBinary, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    tophat = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
    # 高斯滤波
    # stuImgGray = cv2.GaussianBlur(gradX, (5, 5), 0)
    # cv_show('ref', ref)
    # cv_show('ref', ref)
    # 计算轮廓
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
    # 返回的list中每个元素都是图像中的一个轮廓
    refCnts, hierarchy = cv2.findContours(tophat, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cp = img.copy()
    cv2.drawContours(cp, refCnts, -1, (0, 0, 255), 2)
    print("len(refCnts main)", len(refCnts))
    # cv_show('cpimg', cp)

    nps = myutil.identifyfourDingdian(refCnts, img.shape[1], img.shape[0])  # 排序，从左到右，从上到下

    dst = np.array([
        [lt],
        [rt],
        [rb],
        [lb]
    ], dtype="float32")

    # dst = np.array([
    #     [127 / 1.0, 106 / 1.0],
    #     [2196 / 1.0, 120 / 1.0],
    #     [2194 / 1.0, 1509 / 1.0],
    #     [123 / 1.0, 1488 / 1.0]
    # ], dtype="float32")
    nps = np.array([
        [128 / 1.0, 104 / 1.0],
        [2197 / 1.0, 123 / 1.0],
        [2194 / 1.0, 1510 / 1.0],
        [124 / 1.0, 1490 / 1.0]
    ], dtype="float32")
    print("amaxx-aminx: ", amaxx - aminx, "amaxy - aminy: ", amaxy - aminy)
    print("nps:", nps)
    print("dst:", dst)
    M = cv2.getPerspectiveTransform(nps, dst)
    warped = cv2.warpPerspective(stuImgBinary, M, (amaxx - aminx, amaxy - aminy))
    # cv_show('warpedwarped', warped)
    cv2.imwrite("bb.jpg", warped)
    drawBoundingRect(jxxxjsonlist, warped, aminx, aminy)
    return analysisTempleteStxx(jxxxjsonlist, warped, aminx, aminy)


def main():
    # 读取答题卡json字符串
    with open('./sanfanggsdy.json', encoding='utf-8') as f:
        content = json.load(f)
    bjdlist = content['gsdy'][0]['bjd']
    # minx, miny, maxx, maxy = myutil.useDtkbjdListgetGsdysigedingdian(bjdlist)
    # 读取答题卡图片
    img = cv2.imread("./weihai/sample/sample_full_1.jpg")
    lt, rt, rb, lb, minx, miny, maxx, maxy = myutil.getrealPot(bjdlist, img.shape[0], img.shape[1])
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
    for i in range(1, 10):
        xsStbh2xx2wilteMap = analysisXsFill(content['jxxx'], f"01440221007061542000{i}", 1,
                                            lt, rt, rb, lb, minx, miny, maxx, maxy)
    for i in range(10, 21):
        xsStbh2xx2wilteMap = analysisXsFill(content['jxxx'], f"0144022100706154200{i}", 1,
                                            lt, rt, rb, lb, minx, miny, maxx, maxy)
    print("targetWidth: ", targetWidth, "targetHeight: ", targetHeight)
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
                ltpt = (positionArea['location'][0][0] + 4 - offsetx, positionArea['location'][0][1] + 6 - offsety)
                rbpt = (positionArea['location'][1][0] + 4 - offsetx, positionArea['location'][1][1] + 6 - offsety)
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


def main2(bmh="014402210070615420001", pagenum=1, offsetx=123, offsety=120, targetWidth=2074, targetHeight=1388):
    # 读取答题卡json字符串
    with open('./sanfanggsdy.json', encoding='utf-8') as f:
        content = json.load(f)
    jxxxjsonlist = content['jxxx']

    """ 加载实际待识别的学生图像 """
    # 读取一个模板图像
    img = cv2.imread(f"./weihai/{bmh}/{bmh}_full_{pagenum}.jpg")
    # cv_show('img', img)
    # 灰度图
    stuImgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    gradX = cv2.morphologyEx(stuImgGray, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    # gradX = cv2.GaussianBlur(gradX, (7, 7), 0)
    cv_show('gradX', gradX)
    # 二值图像
    stuImgBinary = cv2.threshold(gradX, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show('ref', ref)
    # 计算轮廓
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
    # 返回的list中每个元素都是图像中的一个轮廓
    refCnts, hierarchy = cv2.findContours(stuImgBinary.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    boundingBoxes = [cv2.boundingRect(c) for c in refCnts]  # 用一个最小的矩形，把找到的形状包起来x,y,h,w
    rec = []
    reb = []
    for (i, b) in enumerate(boundingBoxes):
        if b[2] > 50 and b[3] > 50:
            continue
        if (targetWidth / 4) < b[0] and abs(b[0] - targetWidth) > (targetWidth / 4):
            continue
        if (targetHeight / 4) < b[1] and abs(b[1] - targetHeight) > (targetHeight / 4):
            continue
        # 面积判断
        area = cv2.contourArea(refCnts[i])
        if area < 100:
            continue
        # 周长判断
        perimeter = cv2.arcLength(refCnts[i], True)
        if perimeter < 40:
            continue
        reb.append(b)
        rec.append(refCnts[i])
    cp = img.copy()
    cv2.drawContours(cp, rec, -1, (0, 0, 255), 2)
    print("len(rec)", len(rec))
    cv_show('cp', cp)

    nps = myutil.identifyfourDingdian(refCnts, img.shape[1], img.shape[0])  # 排序，从左到右，从上到下

    dst = np.array([
        [0 / 1.0, 0 / 1.0],
        [targetWidth / 1.0, 0 / 1.0],
        [targetWidth / 1.0, targetHeight / 1.0],
        [0 / 1.0, targetHeight / 1.0]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(nps, dst)
    warped = cv2.warpPerspective(stuImgBinary, M, (targetWidth, targetHeight))
    # drawBoundingRect(jxxxjsonlist, warped, offsetx, offsety)


if __name__ == '__main__':
    main()
