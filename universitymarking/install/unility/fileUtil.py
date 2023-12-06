import chardet
def lineReplace(fileabstractpath, originalstr, targetstr):
    """
    对文件中的某一行数据进行替换
    :param fileabstractpath:
    :param originalstr:
    :param targetstr:
    :return:
    """
    encode = detect_encoding(fileabstractpath)
    lines = []
    with open(fileabstractpath, "rb") as ini:
        for line in ini.readlines():
            if not line:
                break
            # 字段替换
            trimline = ''.join([i.strip(' ') for i in line.decode(encode)])
            for i in range(len(originalstr)):
                if trimline.startswith(originalstr[i]):
                    line = targetstr[i].encode(encode) + "\n".encode(encode)
            lines.append(line)

    with open(fileabstractpath, "wb") as ini:
        ini.writelines(lines)

def detect_encoding(fileabstractpath):
    with open(fileabstractpath, "rb") as ini:
        content = ini.read()
        result = chardet.detect(content)
        encoding = result['encoding']
        # confidence = result['confidence']
        return encoding

