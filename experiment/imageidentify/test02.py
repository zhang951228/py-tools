import json
import numpy as np
import cv2

import myutils


def cv_show(name, img):
    cp_img = img.copy()
    naturalshape = cp_img.shape
    width = int(naturalshape[1] / 3)
    height = int(naturalshape[0] / 3)
    cp_img = cv2.resize(cp_img, (width, height))
    cv2.imshow(name, cp_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def chulixuesheng():
    """ 加载实际待识别的学生图像 """
    # 读取一个模板图像
    img = cv2.imread("./images/11090927112810001_full_2.jpg")
    orgimg = img.copy()
    # cv_show('img', img)
    # 灰度图
    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv_show('ref', ref)
    # 二值图像
    # ref = cv2.threshold(ref, 100, 255, cv2.THRESH_BINARY)[1]
    ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show('ref', ref)
    # 计算轮廓
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）,cv2.RETR_EXTERNAL只检测外轮廓，cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
    # 返回的list中每个元素都是图像中的一个轮廓
    refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = myutils.getfours(refCnts, img.shape[1], img.shape[0])  # 排序，从左到右，从上到下
    cv2.drawContours(img, refCnts, -1, (0, 0, 255), 10)
    cv_show(r'xuesheng dingwei sigejiao', img)

    # minx, miny, maxx, maxy = myutils.getsigedians(refCnts)
    nps = myutils.getsigedianss(refCnts)
    # img = img[miny: maxy, minx:maxx]
    # cv_show(r'xuesehngtuxiang  sigejiaowei dingdian', img)
    return nps, orgimg, ref


def main():
    # 读取答题卡json字符串
    with open('./gd/dtkxx.json', encoding='utf-8') as f:
        content = json.load(f)
    bjdlist = content['gsdy'][0]['bjd']
    minx, miny, maxx, maxy = myutils.getgsdysigedian(bjdlist)
    # 读取答题卡图片
    img = cv2.imread("./gd/sample_full_1.jpg")
    # 使用 x y 的最大最小值,切割格式定义的答题卡,验证是否套准了
    biaozhun_gsdytx = img[miny: maxy, minx:maxx]
    biaozhun_huidu = cv2.cvtColor(biaozhun_gsdytx, cv2.COLOR_BGR2GRAY)
    # cv_show('ref', ref)
    # 二值图像
    # ref = cv2.threshold(ref, 100, 255, cv2.THRESH_BINARY)[1]
    biaozhun_erzhi = cv2.threshold(biaozhun_huidu, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show('img', img)
    # 计算出中心/期望图像的宽度/高度
    imgglobalX = maxx - minx
    imgglobalY = maxy - miny

    # 学生图像
    rect, xsimg, huidutuxiang = chulixuesheng()
    # 一共4个坐标点

    # 图像变换
    dst = np.array([
        [0 / 1.0, 0 / 1.0],
        [imgglobalX / 1.0, 0 / 1.0],
        [imgglobalX / 1.0, imgglobalY / 1.0],
        [0 / 1.0, imgglobalY / 1.0]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    aa = imgglobalX
    bb = imgglobalY
    warped = cv2.warpPerspective(xsimg, M, (aa, bb))
    cv_show('img', warped)

    # 循环读取模板中的选项, 例如:第一题的选项Ａ 统计方格内模板的填充数量,统计学生作答的学生数量. 统计框选区域中的像素数量.
    # 使用mask来判断结果
    mask = np.zeros(huidutuxiang.shape, dtype="uint8")
    cv2.rectangle(mask, (167 - minx, 589 - miny), (199 - minx, 605 - miny), (255, 255, 255), -1)
    # cv2.drawContours(mask, xuanxiangA, -1, (0, 0, 255), -1)  # -1表示填充
    mask_org = mask.copy()
    mask = cv2.bitwise_and(huidutuxiang, huidutuxiang, mask=mask)
    cv_show('mask2', mask)
    total = cv2.countNonZero(mask_org)
    print("学生数量", total)

    cv_show('biaozhun_erzhi', biaozhun_erzhi)
    #cv2.imwrite("aa.jpg", biaozhun_erzhi)
    # 整理格式定义卡:
    gsdy_mask = np.zeros(biaozhun_erzhi.shape, dtype="uint8")
    print("minx:", minx, "miny", miny)
    cv2.rectangle(gsdy_mask, (167 - minx, 589 - miny), (199 - minx, 605 - miny), (255, 255, 255), -1)
    #cv2.calcHist()
    cv_show('gsdy_mask', gsdy_mask)
    gsdy_mask_org = gsdy_mask.copy()
    gsdy_mask = cv2.bitwise_and(biaozhun_erzhi, biaozhun_erzhi, mask=gsdy_mask)
    cv_show('mask3', gsdy_mask)
    total2 = cv2.countNonZero(gsdy_mask)
    print("模板数量", total2)

    zhanbi = ((561 - total) - ( 561 - total2))/ total2
    print(zhanbi)
    print(max(0, zhanbi))

def test():
    rect = np.array([
        [34.0, 56.0],
        [1694.0, 56.0],
        [1694.0, 2418.0],
        [34.0, 2418.0]
    ], dtype="float32")
    dst = np.array([
        [0.0, 0.0],
        [2340.0, 0.0],
        [2340.0, 1653.0],
        [0.0, 1653.0]
    ], dtype="float32")
    xsimg = cv2.imread("./images/11090927112810001_full_2.jpg")
    ref = cv2.cvtColor(xsimg, cv2.COLOR_BGR2GRAY)
    # cv_show('ref', ref)
    # 二值图像
    ref = cv2.threshold(ref, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(ref, M, (2340, 1653))
    cv_show('img', warped)


if __name__ == '__main__':
    main()
