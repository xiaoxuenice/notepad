linux根扩容（ext4直接调整大小。xfs只能增加。详情看下面）

df -Th  lsblk partprobe
#################################################################3
1，添加硬盘
fdisk /dev/sdb
n 回车 回车 回车
t   8e   w

2，格式化，根据类型（xfs，ext4）
mkfs.xfs /dev/sdb1
mkfs.ext4 /dev/sdb1
lsblk

3，创建pv物理卷
pvcreate /dev/sdb1

4，添加到系统所在的centos卷组
vgdisplay
vgextend centos /dev/sdb1

5，扩充根所在的逻辑卷
lvextend -l +100%FREE /dev/centos/root

6，执行调整，根据类型（xfs，ext4）
xfs_growfs /dev/mapper/centos-home
resize2fs /dev/mapper/centos-home

7，查看
df -Th
###########################################################################################

###########################################################################################
xfs 减小分区空间，减小前必须要先卸载这个分区

1，先卸载调整的分区
fuser -m -k /home  (无法卸载，有进程占用使用)
umount  /home

2，减小lv的分区
 lvreduce -L -100G /dev/mapper/centos-home

3，重新格式化这个逻辑卷 (没有数据)
mkfs.xfs /dev/mapper/centos-home -f

------------------------  格式化为 ext4 ---------------------------
mkfs.ext4 /dev/mapper/centos-home   
cat /etc/fstab  （将home分区的开机挂载设置里的xfs改为ext4）|
-------------------------------------------------------------------
4，挂载 mount /dev/mapper/centos-home /home/

5, partprobe (重新识别，lsblk查看)
##########################################################
   
  config显示和操作配置信息
  devtypes显示已识别的内置块设备类型
  dumpconfig显示和操作配置信息
  格式列出可用的元数据格式
  help显示命令帮助
  fullreport显示完整报告
  lastlog显示最后一个命令的日志报告
  lvchange更改逻辑卷的属性
  lvconvert更改逻辑卷布局
  lvcreate创建逻辑卷
  lvdisplay显示有关逻辑卷的信息
  lvextend为逻辑卷添加空间
  lvmchange使用设备映射器，这是过时的，什么都不做。
  lvmconfig显示和操作配置信息
  lvmdiskscan列出可用作物理卷的设备
  lvmsadc收集活动数据
  lvmsar创建活动报告
  lvreduce减小逻辑卷的大小
  lvremove从系统中删除逻辑卷
  lvrename重命名逻辑卷
  lvresize调整逻辑卷的大小
  lvs显示有关逻辑卷的信息
  lvscan列出所有卷组中的所有逻辑卷
  pvchange更改物理卷的属性
  pvresize调整物理卷的大小
  pvck检查物理卷的一致性
  pvcreate初始化LVM使用的物理卷
  pvdata显示物理卷的磁盘元数据
  pvdisplay显示物理卷的各种属性
  pvmove将范围从一个物理卷移动到另一个物理卷
  lvpoll继续在逻辑卷上启动轮询操作
  pvremove从物理卷中删除LVM标签
  pvs显示有关物理卷的信息
  pvscan列出所有物理卷
  segtypes列出可用的段类型
  systemid显示当前在此主机上设置的系统ID（如果有）
  tags此主机上定义的列表标签
  vgcfgbackup备份卷组配置
  vgcfgrestore还原卷组配置
  vgchange更改卷组属性
  vgck检查卷组的一致性
  vgconvert更改卷组元数据格式
  vgcreate创建卷组
  vgdisplay显示卷组信息
  vgexport从系统中取消注册卷组
  vgextend将物理卷添加到卷组
  vgimport使用system注册导出的卷组
  vgimportclone从克隆的PV导入VG
  vgmerge合并卷组
  vgmknodes在/ dev中为卷组设备创建特殊文件
  vgreduce从卷组中删除物理卷
  vgremove删除卷组
  vgrename重命名卷组
  vgs显示有关卷组的信息
  vgscan搜索所有卷组
  vgsplit将物理卷移动到新的或现有的卷组中
  version显示软件和驱动程序版本信息
