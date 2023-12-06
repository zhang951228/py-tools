from PIL import Image
import os


def tiftojpg(path, targetPath):
    """
    tif文件转jpg文件.
    :param path:
    :param targetPath:
    :return:
    """
    kmdirlist = os.listdir(path)
    for km in kmdirlist:
        for bmhlist in os.listdir(path + "/" + km):
            if bmhlist.endswith(".tif"):
                image = Image.open(path + "/" + km + "/" + bmhlist)
                file_new_name = os.path.splitext(os.path.basename(bmhlist))[0] + ".jpg"
                image.save(targetPath + "/" + km + "/" + file_new_name)


if __name__ == '__main__':
    tiftojpg(r"D:\sdzdf\大学\实施\南京医科大学\tif文件", r"D:\sdzdf\大学\实施\南京医科大学\jpg文件")
