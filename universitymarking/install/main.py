import configparser

from universitymarking.install.unility import fileUtil


def initmysql(universitymarkingbasedir: str):
    """
    启动mysql
    :param universitymarkingbasedir:
    :return:
    """
    originalstr = ["basedir=", "datadir="]
    targetstr = [f"basedir={universitymarkingbasedir}/mysql",
                 f"datadir={universitymarkingbasedir}/mysql/data"]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/mysql/my.ini",
                         originalstr, targetstr)


def initrocketmq(universitymarkingbasedir: str):
    """
    启动rocketmq
    :param universitymarkingbasedir:
    :return:
    """
    # 配置文件中地址的修改
    originalstr = ["storePathRootDir=", "storePathCommitLog=", "storePathConsumeQueue",
                   "storePathindex=", "storeCheckpoint=", "abortFile="]
    targetstr = [f"storePathRootDir={universitymarkingbasedir}/rocketmq/store",
                 f"storePathCommitLog={universitymarkingbasedir}/rocketmq/store/commitlog",
                 f"storePathConsumeQueue={universitymarkingbasedir}/rocketmq/store/consumequeue",
                 f"storePathindex={universitymarkingbasedir}/rocketmq/store/index",
                 f"storeCheckpoint={universitymarkingbasedir}/rocketmq/store/checkpoint",
                 f"abortFile={universitymarkingbasedir}/rocketmq/store/abort",
                 ]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/rocketmq/conf/broker1.conf",
                         originalstr, targetstr)
    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={universitymarkingbasedir}/rocketmq\""]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/rocketmq/bin/mqnamesrv.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={universitymarkingbasedir}/jdk/jdk8\""]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/rocketmq/bin/runserver.cmd",
                         originalstr, targetstr)

    # 设置ROCKETMQ_HOME
    # 设置server的java环境变量
    originalstr = ["set\"ROCKETMQ_HOME="]
    targetstr = [f"set \"ROCKETMQ_HOME={universitymarkingbasedir}/rocketmq\""]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/rocketmq/bin/mqbroker.cmd",
                         originalstr, targetstr)

    # 设置server的java环境变量
    originalstr = ["set\"JAVA_HOME="]
    targetstr = [f"set \"JAVA_HOME={universitymarkingbasedir}/jdk/jdk8\""]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/rocketmq/bin/runbroker.cmd",
                         originalstr, targetstr)

def initredis(universitymarkingbasedir: str):

    originalstr = ["logfile"]
    targetstr = [f"logfile {universitymarkingbasedir}/redis/logs/rediswin.log"]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/redis/redis.windows.conf",
                         originalstr, targetstr)

    originalstr = ["logfile"]
    targetstr = [f"logfile {universitymarkingbasedir}/redis/logs/redisser.log"]
    fileUtil.lineReplace(f"{universitymarkingbasedir}/redis/redis.windows-service.conf",
                         originalstr, targetstr)



if __name__ == '__main__':
    # 读取跟路径
    config = configparser.ConfigParser()
    config.read("umcfg.ini")
    baseurl = config.get("universitymarking", "universitymarkingbasedir")

    # 启动mysql
    # if config.getboolean("mysql", "initmysql"):
    #    initmysql(baseurl)

    # 初始化rocketmq
    # initrocketmq(baseurl)

    # 初始化redis
    initredis(baseurl)
