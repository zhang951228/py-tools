echo "start rocketmq server"
cd "%universitymarkignurl%\rocketmq\bin"
start mqnamesrv.cmd -c  ..\conf\namesrv.properties
cd "%universitymarkignurl%\rocketmq\bin"
mqbroker.cmd -c ..\conf\broker.conf

cd "%bootpath%"
echo "end start rocketmq server"