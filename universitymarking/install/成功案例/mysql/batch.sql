use mysql;
update user set host = '%' where user = 'root';
create user 'sdzdf'@'%' identified by 'anquanshengchan$007';
flush privileges;
grant all privileges on *.* to  'sdzdf'@'%';
flush privileges;