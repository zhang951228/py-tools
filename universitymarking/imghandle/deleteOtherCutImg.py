import os


def removeCutImg(path):
    """ 删除其他切图图像,只保留 full 文件"""
    #path = r"D:\sdzdf\img\青理工\218\218"
    listdir = os.listdir(path)
    for bmhfile in listdir:
        tBmh = os.listdir(path + "\\" + bmhfile)
        for stuImg in tBmh:
            if stuImg.endswith(".jpg") and not stuImg.__contains__("full"):
                removepath = path + "\\" + bmhfile + "\\" + stuImg
                print(removepath)
                os.remove(removepath)

def removeCutImg2(path):
    """ 删除其他切图图像,只保留 full 文件"""
    listdir = os.listdir(path)
    for bmhfile in listdir:
        tBmh = os.listdir(path + "\\" + bmhfile)
        for stuImg in tBmh:
            if stuImg.endswith(".jpg") and not stuImg.__contains__("full"):
                removepath = path + "\\" + bmhfile + "\\" + stuImg
                print(removepath)
                os.remove(removepath)
if __name__ == '__main__':
    # path = input("请输入路径:")
    path = r"D:\universityMarking\tomcat\webapps\Examimg\10001\20231\3"
    removeCutImg2(path)
