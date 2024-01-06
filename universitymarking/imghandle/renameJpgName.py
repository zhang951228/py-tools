import os


def rename(path):
    """  文件重命名  """
    # path = r"D:\sdzdf\img\青理工\218\218"
    imgs = os.listdir(path)
    for img in imgs:
        if img.endswith(".jpg"):
            name = img.split(".")[0]
            if name.__contains__("HGScan"):
                name = name.replace("HGScan", "")
            if len(name) == 3:
                newName = "100" + name + ".jpg"
            elif len(name) == 4:
                newName = "10" + name + ".jpg"
            os.rename(path + "\\" + img, path + "\\" + newName)


if __name__ == '__main__':
    path = input("请输入路径:")
    # path = r"D:\sdzdf\img\南京医科大学\testimg"
    rename(path)
