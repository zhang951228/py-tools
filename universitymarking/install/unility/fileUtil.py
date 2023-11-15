def lineReplace(fileabstractpath, originalstr, targetstr):
    """
    对文件中的某一行数据进行替换
    :param fileabstractpath:
    :param originalstr:
    :param targetstr:
    :return:
    """
    lines = []
    with open(fileabstractpath, "rb") as ini:
        for line in ini.readlines():
            if not line:
                break
            # 字段替换
            trimline = ''.join([i.strip(' ') for i in line.decode("UTF-8")])
            for i in range(len(originalstr)):
                if trimline.startswith(originalstr[i]):
                    line = targetstr[i].encode("UTF-8") + "\n".encode("UTF-8")
            lines.append(line)

    with open(fileabstractpath, "wb") as ini:
        ini.writelines(lines)
