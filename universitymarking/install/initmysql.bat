set "universitymarkignurl=E:/universitymarking"
echo "start mysql server"
cd "%universitymarkignurl%\mysql\bin"
echo "%cd%"


mysqld -install
net start mysql
