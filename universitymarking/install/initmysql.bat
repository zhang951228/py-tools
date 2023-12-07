echo "start mysql server"
cd "%universitymarkignurl%\mysql\bin"

mysqld -install
net start mysql

cd "%bootpath%"
echo "end start mysql server"