import os
import sys

import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        if len(sys.argv) != 2:
            input("输入参数非法,请输入一个待执行的cmd命令文件")
        else:
            os.system(sys.argv[1])
            input("系统参数初始化完成,请手动执行个bat文件,按任意键退出......")
    # 主程序写在这里
    else:
        # 以管理员权限重新运行程序
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[1], None, 1)
