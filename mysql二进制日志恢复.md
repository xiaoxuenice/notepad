#!/bin/bash
数据库迁移
旧：mysqldump -uroot -pPwd@123456  --databases domain  > domain.sql
新：create database domain
新：source domain.sql

导入一张表 test库，user表
旧：mysqldump -u root -p Test user > a.txt
新：use Test
新：source a.txt

二进制日志恢复

vim /etc/my.cnf
max-binlog-size=1024M
log_bin=mysqlbin
max_allowed_packet=200m
interactive_timeout=600
wait_timeout=600

mysql> reset master;	   重置二进制日志（慎用）
mysql> flush logs;		添加二进制日志
mysql> show master status;
| File            | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
| mysqlbin.000001 |    12061 |              |                  |                   |
#---------------------------------------------------------------------------------------

查看二进制日志内容
mysqlbinlog mysqlbin.000001 > 1.sql;vim 1.sql
根据1.sql里面的 COMMIT/*!*/; 的上一行获取position的值

#假设100的pos是删除数据的命令99以前的内容恢复和101以后的
mysqlbinlog --no-defaults --stop-position=99   mysqlbin.000001 |mysql -uroot -pPwd@123456
mysqlbinlog --no-defaults --start-position=101 mysqlbin.000001 |mysql -uroot -pPwd@123456

#主从报错 Can t find record in 
vim /etc/my.cnf
slave-skip-errors=1032
#报错主键冲突mysql-uroot-p加-f
