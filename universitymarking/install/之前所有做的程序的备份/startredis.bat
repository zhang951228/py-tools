
echo "start redis server"
cd "%universitymarkignurl%\redis"

redis-server.exe redis.windows.conf
cd "%bootpath%"
echo "end start redis server"