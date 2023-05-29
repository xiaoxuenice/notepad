yum -y install rsync
cat >>  /etc/rsync.conf < EOF
use chroot = no
uid = root
gid = root
port = 30001
max connections = 4
log file = /var/log/rsyncd.log
pid file = /var/run/rsyncd.pid
# 安全配置
use chroot = no
secrets file = /etc/rsync.secrets

#模块web参数配置，可配置多个模块
[backup]
comment = backup
read only = no
path = /data/backup
auth users = rsyncuser 
exclude = .env attached storage .svn
hosts allow = 192.168.1.23
EOF
echo rsyncuser:asdfasdf > /etc/rsync.secrets
chmod 600  /etc/rsync.secrets




# 远程备份服务器 登录账户
RemoteUser=rsyncuser

# 远程备份服务器 IP地址
RemoteIP=192.168.1.10
echo asdfasdf > passwd.txt
chmod 600 passwd.txt
/usr/bin/rsync -aq --progress --port=30001 $tar_file_name  $RemoteUser@$RemoteIP::backup  --password-file=passwd.txt
rm -f passwd.txt
