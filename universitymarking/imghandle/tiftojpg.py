from PIL import Image
import os


def tiftojpg(sourcePath, targetPath):
    """
    tif文件转jpg文件.
    :param sourcePath:
    :param targetPath:
    :return:
    """
    for bmhlist in os.listdir(sourcePath):
        if bmhlist.endswith(".png"):
            image = Image.open(sourcePath + "/" + bmhlist)
            file_new_name = os.path.splitext(os.path.basename(bmhlist))[0] + ".jpg"
            image.save(targetPath + "/" + file_new_name)


def pngToJpg(sourcePath, targetPath):
    """
    tif文件转jpg文件.
    :param sourcePath:
    :param targetPath:
    :return:
    """
    for bmhlist in os.listdir(sourcePath):
        if bmhlist.endswith(".png"):
            image = Image.open(sourcePath + "/" + bmhlist).convert("RGB")
            file_new_name = os.path.splitext(os.path.basename(bmhlist))[0] + ".jpg"
            image.save(targetPath + "/" + file_new_name)


if __name__ == '__main__':
    pngToJpg(r"D:\sdzdf\大学\实施\测试png转jpg", r"D:\sdzdf\大学\实施\测试png转jpg")
