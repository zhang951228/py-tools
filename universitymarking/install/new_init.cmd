@echo off
rem set dependent server's path
set bootpath=%cd%
set universitymarkignurl=D:/sdzdf/universityMarking_environment
set mysql_dir=%universitymarkignurl%/mysql/bin
set rocketmq_dir=%universitymarkignurl%/rocketmq/bin
set redis_dir=%universitymarkignurl%/redis
set tomcat_dir=%universitymarkignurl%/tomcat/bin
set app_dir=%universitymarkignurl%/universityMarking_8011
set nginx_dir=%universitymarkignurl%/nginx/

rem set server's init parament
set tomcat_service_name=UniversityMarkingTomcat
set mysql_service_name=UniversityMarkingMysql