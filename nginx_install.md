#!/bin/bash
#php 需要修改 listen 监听地址 www.conf
cd /usr/src
yum -y install gcc gcc-c++ make libtool zlib zlib-devel pcre pcre-devel openssl openssl-devel
wget http://nginx.org/download/nginx-1.14.0.tar.gz
if [ ! $? -eq 0 ];then exit 11;fi
wget https://raw.githubusercontent.com/xiaoxuenice/learn/master/openssl-1.0.2l.tar.gz
if [ ! $? -eq 0 ];then exit 22;fi
wget https://raw.githubusercontent.com/xiaoxuenice/learn/master/ngx_cache_purge-2.3.tar.gz
if [ ! $? -eq 0 ];then exit 33;fi
tar zxf nginx-1.14.0.tar.gz 
tar zxf ngx_cache_purge-2.3.tar.gz
tar zxf openssl-1.0.2l.tar.gz
groupadd www
useradd -g www www -s /sbin/nologin
cd nginx-1.14.0/
 ./configure --prefix=/usr/local/nginx --with-http_dav_module --with-http_stub_status_module --with-http_addition_module --with-http_sub_module --with-http_flv_module --with-http_mp4_module --with-pcre --with-http_ssl_module --with-http_gzip_static_module --user=www --group=www --with-openssl=/usr/src/openssl-1.0.2l --add-module=/usr/src/ngx_cache_purge-2.3
make && make install
ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/
cat >> /etc/init.d/nginx << EOF
#!/bin/bash
# chkconfig: 345 85 15
nginx=/usr/local/sbin/nginx
conf=/usr/local/nginx/conf/nginx.conf
case \$1 in
start)
\$nginx
echo "nginx is start"
;;
reload)
\$nginx -s reload
echo "nginx reload done"
;;
stop)
\$nginx -s stop
echo "nginx is stop "
;;
restart)
\$nginx -s stop 2>/dev/null
\$nginx
echo "nginx restart done"
;;
*)
echo "what do you want to do?"
;;
esac
EOF
chmod 755 /etc/init.d/nginx
chkconfig --add nginx
chkconfig nginx on
ss -anplt | grep nginx
nginx
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --reload

