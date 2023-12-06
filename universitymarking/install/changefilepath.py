import configparser
import os
import chardet


def lineReplaceStartWith(fileabstractpath, originalstr, targetstr):
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


def lineReplaceContains(fileabstractpath, originalstr, targetstr):
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
                if trimline.__contains__(originalstr[i]):
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


def initmysql(targeturl: str, existurl: str):
    """
    初始化mysql
    :param targeturl:
    :return:
    """
    originalstr = ["basedir=", "datadir="]
    targetstr = [f"basedir={targeturl}/mysql",
                 f"datadir={targeturl}/mysql/data"]
    lineReplaceStartWith(f"{existurl}/mysql/my.ini",
                         originalstr, targetstr)


def initrocketmq(targeturl: str, existurl: str):
    """
    初始化rocketmq
    :param targeturl:
    :return:
    """
    # 配置文件中地址的修改
    originalstr = ["storePathRootDir=", "storePathCommitLog=", "storePathConsumeQueue",
                   "storePathindex=", "storeCheckpoint=", "abortFile="]
    targetstr = [f"storePathRootDir={targeturl}/rocketmq/store",
                 f"storePathCommitLog={targeturl}/rocketmq/store/commitlog",
                 f"storePathConsumeQueue={targeturl}/rocketmq/store/consumequeue",
                 f"storePathindex={targeturl}/rocketmq/store/index",
                 f"storeCheckpoint={targeturl}/rocketmq/store/checkpoint",
                 f"abortFile={targeturl}/rocketmq/store/abort",
                 ]
    lineReplaceStartWith(f"{existurl}/rocketmq/conf/broker.conf",
                         originalstr, targetstr)
    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={targeturl}/rocketmq\""]
    lineReplaceStartWith(f"{existurl}/rocketmq/bin/mqnamesrv.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={targeturl}/jdk/jdk8\""]
    lineReplaceStartWith(f"{existurl}/rocketmq/bin/runserver.cmd",
                         originalstr, targetstr)

    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={targeturl}/rocketmq\""]
    lineReplaceStartWith(f"{existurl}/rocketmq/bin/mqbroker.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={targeturl}/jdk/jdk8\""]
    lineReplaceStartWith(f"{existurl}/rocketmq/bin/runbroker.cmd",
                         originalstr, targetstr)
    originalstr = ["set\"targeturl"]
    targetstr = [f"set \"targeturl={targeturl}\""]
    lineReplaceStartWith(f"{existurl}/starter/startrocketmq.bat",
                         originalstr, targetstr)


def initredis(targeturl: str, existurl: str):
    originalstr = ["logfile"]
    targetstr = [f"logfile {targeturl}/redis/logs/rediswin.log"]
    lineReplaceStartWith(f"{existurl}/redis/redis.windows.conf",
                         originalstr, targetstr)

    originalstr = ["logfile"]
    targetstr = [f"logfile {targeturl}/redis/logs/redisser.log"]
    lineReplaceStartWith(f"{existurl}/redis/redis.windows-service.conf",
                         originalstr, targetstr)
    originalstr = ["set\"targeturl"]
    targetstr = [f"set \"targeturl={targeturl}\""]
    lineReplaceStartWith(f"{existurl}/starter/startredis.bat",
                         originalstr, targetstr)


def inittomcat(targeturl: str, existurl: str):
    originalstr = ["set\"JAVA_HOME"]
    targetstr = [f"set \"JAVA_HOME={targeturl}/jdk/jdk8\""]
    lineReplaceStartWith(f"{existurl}/tomcat/bin/catalina.bat",
                         originalstr, targetstr)
    originalstr = ["set\"targeturl"]
    targetstr = [f"set \"targeturl={targeturl}\""]
    lineReplaceStartWith(f"{existurl}/starter/starttomcat.bat",
                         originalstr, targetstr)


def initapp(targeturl: str, existurl: str):
    originalstr = ["file-profile"]
    targetstr = [f"  file-profile: {targeturl} #文件存放路径 "]
    lineReplaceStartWith(f"{existurl}/universityMarking_8011/application-local.yml",
                         originalstr, targetstr)
    # 缺少初始化sdzdf.bat的
    originalstr = ["set\"JAVA="]
    targetstr = [f"set \"JAVA={targeturl}/jdk/jdk17/bin/java.exe\""]
    lineReplaceStartWith(f"{existurl}/universityMarking_8011/sdzdf17.bat", originalstr, targetstr)
    # 12服务器,
    originalstr = ["file-profile"]
    targetstr = [f"  file-profile: {targeturl} #文件存放路径 "]
    lineReplaceStartWith(f"{existurl}/universityMarking_8012/application-local.yml",
                         originalstr, targetstr)
    # 缺少初始化sdzdf.bat的
    originalstr = ["set\"JAVA="]
    targetstr = [f"set \"JAVA={targeturl}/jdk/jdk17/bin/java.exe\""]
    lineReplaceStartWith(f"{existurl}/universityMarking_8012/sdzdf17.bat", originalstr, targetstr)


def initnginx(targeturl: str, existurl: str):
    panfu = targeturl[0:2]
    originalstr = ["SETNGINX_PATH", "SETNGINX_DIR="]
    targetstr = [f"SET NGINX_PATH={panfu}", f"SET NGINX_DIR={targeturl}/nginx/"]
    lineReplaceStartWith(f"{existurl}/nginx/nginxstartup.bat",
                         originalstr, targetstr)
    lineReplaceStartWith(f"{existurl}/starter/startnginx.bat",
                         originalstr, targetstr)
    # config文件没有修改.
    originalstr = ["教师端项目部署位置", "学生端项目部署位置", "题库项目部署位置"]
    targetstr = [f"			root  {targeturl}/view_marking; # 教师端项目部署位置",
                 f"			alias  {targeturl}/stu; # 学生端项目部署位置",
                 f"			alias  {targeturl}/qbank; # 题库项目部署位置"]
    lineReplaceContains(f"{existurl}/nginx/conf/nginx.conf",
                        originalstr, targetstr)


def updateinitstate(targeturl: str, existurl: str):
    originalstr = ["initmysql=", "initrocketmq=", "initredis=", "inittomcat=",
                   "initapplication=", "initnginx="]
    targetstr = ["initmysql=false", "initrocketmq=false", "initredis=false",
                 "inittomcat=false", "initapplication=false", "initnginx=false"]
    lineReplaceStartWith(f"{existurl}/starter/umcfg.ini",
                         originalstr, targetstr)


if __name__ == '__main__':
    # 读取跟路径
    config = configparser.ConfigParser()
    config.read("umcfg.ini")
    targeturl = config.get("universitymarking", "targeturl")
    existurl = config.get("universitymarking", "existurl")

    # 启动mysql
    if config.getboolean("mysql", "initmysql"):
        initmysql(targeturl, existurl)
        print("初始化 mysql 完毕")

    # 初始化rocketmq
    if config.getboolean("rocketmq", "initrocketmq"):
        initrocketmq(targeturl, existurl)
        print("初始化 rocketmq 完毕")

    # 初始化redis
    if config.getboolean("redis", "initredis"):
        initredis(targeturl, existurl)
        print("初始化 redis 完毕")

    # 初始化tomcat
    if config.getboolean("tomcat", "inittomcat"):
        inittomcat(targeturl, existurl)
        print("初始化 tomcat 完毕")

    # 初始化应用
    if config.getboolean("application", "initapplication"):
        initapp(targeturl, existurl)
        print("初始化 application 完毕")

    # 初始化nginx
    if config.getboolean("nginx", "initnginx"):
        initnginx(targeturl, existurl)
        print("初始化 nginx 完毕")

    # 将所有的init设置都改为false.
    updateinitstate(targeturl, existurl)
    print("更新初始化配置文件完毕")

    input("系统参数初始化完成,请手动执行个bat文件,按任意键退出......")
    if config.getboolean("universitymarking", "autostart"):
        # 开始启动各个项目

        print("start mysql")
        os.popen(f"{targeturl}/starter/startmysql.bat.bat")
        print("start rocketmq")
        os.popen(f"{targeturl}/starter/startrocketmq.bat")
        print("start redis")
        os.popen(f"{targeturl}/starter/startredis.bat")
        print("start tomcat")
        os.popen(f"{targeturl}/starter/starttomcat.bat")
        print("start app")
        os.popen(f"{targeturl}/starter/startapp.bat")
        print("start nginx")
        os.popen(f"{targeturl}/starter/startnginx.bat")
