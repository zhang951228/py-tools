set "universitymarkignurl=C:\myftp"
echo "start rocketmq server"
cd "%universitymarkignurl%\rocketmq\bin"
echo "%cd%"
start mqnamesrv.cmd -c  ..\conf\namesrv.properties
cd "%universitymarkignurl%\rocketmq\bin"
mqbroker.cmd -c ..\conf\broker.conf