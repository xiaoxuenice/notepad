#!/bin/bash
#添加开机自启
#安装 rsync inotify-tools
# rsync --delete 参数表示删除目的多余的文件,斜杠要加，不然表示目录要加-r参数
#脚本表示 /test/目录如果发生变数同步到192.168.116.200:/test下
inotifywait -mrq --timefmt '%d/%m/%y %H:%M' --format '%T %w%f' -e modify,delete,create,attrib /test/ | while read file; do
rsync -avz --delete /test/ 192.168.116.200:/test1/
echo ${file} >>/var/log/rsync.log 2>&1
done

