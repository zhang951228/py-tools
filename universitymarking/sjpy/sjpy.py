import universitymarking.utility as util


if __name__ == '__main__':
    accessToken = util.login()
    print("accessToken: ", accessToken)
    pylist = util.getpylist(accessToken)
    print("pylist: ", pylist)


