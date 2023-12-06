import configparser
import os

from universitymarking.install.unility import fileUtil


def initmysql(universitymarkignurl: str):
    """
    初始化mysql
    :param universitymarkignurl:
    :return:
    """
    originalstr = ["basedir=", "datadir="]
    targetstr = [f"basedir={universitymarkignurl}/mysql",
                 f"datadir={universitymarkignurl}/mysql/data"]
    fileUtil.lineReplace(f"{universitymarkignurl}/mysql/my.ini",
                         originalstr, targetstr)
    originalstr = ["set\"universitymarkignurl", "mysql-uroot-panquanshengchan$996"]
    targetstr = [f"set \"universitymarkignurl={universitymarkignurl}\"",
                 f"mysql -uroot -panquanshengchan$996  < {universitymarkignurl}/starter/batch.sql"]
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/initmysql.bat",
                         originalstr, targetstr)


def initrocketmq(universitymarkignurl: str):
    """
    启动rocketmq
    :param universitymarkignurl:
    :return:
    """
    # 配置文件中地址的修改
    originalstr = ["storePathRootDir=", "storePathCommitLog=", "storePathConsumeQueue",
                   "storePathindex=", "storeCheckpoint=", "abortFile="]
    targetstr = [f"storePathRootDir={universitymarkignurl}/rocketmq/store",
                 f"storePathCommitLog={universitymarkignurl}/rocketmq/store/commitlog",
                 f"storePathConsumeQueue={universitymarkignurl}/rocketmq/store/consumequeue",
                 f"storePathindex={universitymarkignurl}/rocketmq/store/index",
                 f"storeCheckpoint={universitymarkignurl}/rocketmq/store/checkpoint",
                 f"abortFile={universitymarkignurl}/rocketmq/store/abort",
                 ]
    fileUtil.lineReplace(f"{universitymarkignurl}/rocketmq/conf/broker.conf",
                         originalstr, targetstr)
    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={universitymarkignurl}/rocketmq\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/rocketmq/bin/mqnamesrv.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={universitymarkignurl}/jdk/jdk8\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/rocketmq/bin/runserver.cmd",
                         originalstr, targetstr)

    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={universitymarkignurl}/rocketmq\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/rocketmq/bin/mqbroker.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={universitymarkignurl}/jdk/jdk8\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/rocketmq/bin/runbroker.cmd",
                         originalstr, targetstr)
    originalstr = ["set\"universitymarkignurl"]
    targetstr = [f"set \"universitymarkignurl={universitymarkignurl}\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/startrocketmq.bat",
                         originalstr, targetstr)


def initredis(universitymarkignurl: str):
    originalstr = ["logfile"]
    targetstr = [f"logfile {universitymarkignurl}/redis/logs/rediswin.log"]
    fileUtil.lineReplace(f"{universitymarkignurl}/redis/redis.windows.conf",
                         originalstr, targetstr)

    originalstr = ["logfile"]
    targetstr = [f"logfile {universitymarkignurl}/redis/logs/redisser.log"]
    fileUtil.lineReplace(f"{universitymarkignurl}/redis/redis.windows-service.conf",
                         originalstr, targetstr)
    originalstr = ["set\"universitymarkignurl"]
    targetstr = [f"set \"universitymarkignurl={universitymarkignurl}\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/startredis.bat",
                         originalstr, targetstr)


def inittomcat(universitymarkignurl: str):
    originalstr = ["set\"JAVA_HOME"]
    targetstr = [f"set \"JAVA_HOME={universitymarkignurl}/jdk/jdk8\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/tomcat/bin/catalina.bat",
                         originalstr, targetstr)
    originalstr = ["set\"universitymarkignurl"]
    targetstr = [f"set \"universitymarkignurl={universitymarkignurl}\""]
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/starttomcat.bat",
                         originalstr, targetstr)

def initapp(universitymarkignurl: str):
    originalstr = ["file-profile"]
    targetstr = [f"  file-profile: {universitymarkignurl} #文件存放路径"]
    fileUtil.lineReplace(f"{universitymarkignurl}/universityMarking_8011/application-local.yml",
                         originalstr, targetstr)

def initnginx(universitymarkignurl: str):
    panfu = universitymarkignurl[0:2]
    originalstr = ["SETNGINX_PATH", "SETNGINX_DIR="]
    targetstr = [f"SET NGINX_PATH={panfu}", f"SET NGINX_DIR={universitymarkignurl}/nginx/"]
    fileUtil.lineReplace(f"{universitymarkignurl}/nginx/nginxstartup.bat",
                         originalstr, targetstr)
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/startnginx.bat",
                         originalstr, targetstr)

def updateinitstate(universitymarkignurl: str):
    originalstr = ["initmysql=", "initrocketmq=", "initredis=", "inittomcat=",
                   "initapplication=", "initnginx="]
    targetstr = ["initmysql=false", "initrocketmq=false", "initredis=false",
                 "inittomcat=false", "initapplication=false", "initnginx="]
    fileUtil.lineReplace(f"{universitymarkignurl}/starter/umcfg.ini",
                         originalstr, targetstr)


if __name__ == '__main__':
    # 读取跟路径
    config = configparser.ConfigParser()
    config.read("umcfg.ini")
    baseurl = config.get("universitymarking", "universitymarkignurl")

    # # 启动mysql
    # if config.getboolean("mysql", "initmysql"):
    #     initmysql(baseurl)
    #
    # # 初始化rocketmq
    # if config.getboolean("rocketmq", "initrocketmq"):
    #     initrocketmq(baseurl)
    #
    # # 初始化redis
    # if config.getboolean("redis", "initredis"):
    #     initredis(baseurl)
    #
    # # 初始化tomcat
    # if config.getboolean("tomcat", "inittomcat"):
    #     inittomcat(baseurl)
    #
    # # 初始化应用
    # if config.getboolean("application", "initapplication"):
    #     initapp(baseurl)
    #
    # # 初始化nginx
    # if config.getboolean("nginx", "initnginx"):
    #     initnginx(baseurl)

    # 将所有的init设置都改为false.
    updateinitstate(baseurl)
    # i = input("系统参数初始化完成,请手动执行个bat文件,按任意键退出")
    # 开始启动各个项目
    print("start rocketmq")
    os.popen(f"{baseurl}/starter/startrocketmq.bat")
    print("start redis")
    os.popen(f"{baseurl}/starter/startredis.bat")
    print("start tomcat")
    os.popen(f"{baseurl}/starter/starttomcat.bat")
    print("start app")
    os.popen(f"{baseurl}/starter/startapp.bat")
    print("start nginx")
    os.popen(f"{baseurl}/starter/startnginx.bat")

