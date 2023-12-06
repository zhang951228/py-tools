set "universitymarkignurl=E:/universitymarking"
echo "start mysql server"
cd "%universitymarkignurl%\mysql\bin"
echo "%cd%"

mysqld --initialize-insecure
mysqld -install
net start mysql
mysqladmin -u root password anquanshengchan$996
mysql -uroot -panquanshengchan$996 < E:/universitymarking/install/batch.sql