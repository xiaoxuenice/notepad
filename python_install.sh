#!/bin/bash
yum -y install epel-release
yum -y install libffi-devel libffi*  wget openssl-devel vim  make zlib-devel zlib bzip2-devel expat-devel gdbm-devel tk-devel tcl-devel readline-devel sqlite-devel libX11-devel libX11  gcc gcc-c++ 
wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz
if [[ $? > 0 ]];then
  echo " wget failed!!!! "
  exit 0
fi
tar zxf Python-3.9.7.tgz
cd Python-3.9.7
mkdir /usr/local/python
./configure --with-ssl --prefix=/usr/local/python
if [[ $? > 0 ]];then
  echo " wget failed!!!! "
  exit 0
fi
make && make install
if [[ $? > 0 ]];then
  echo " make failed!!! "
  exit 0
fi
echo export PATH="$PATH:/usr/local/python/bin" >> /etc/profile
source /etc/profile
pip3 install --upgrade pip3
pip3 install ipython
if [[ $? > 0 ]];then
  echo " no pip3 install ipython "
  exit 0
fi
source /etc/profile
