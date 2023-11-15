set "universitymarkignurl=C:\Users\z151\Desktop"
echo "¿ªÊ¼Æô¶¯mysql"
cd "%universitymarkignurl%\mysql\bin"
echo "%cd%"

mysqld --initialize-insecure
mysqld -install
net start mysql
mysqladmin -u root password anquanshengchan$996
mysql -uroot -panquanshengchan$996 < C:/myftp/batch.sql