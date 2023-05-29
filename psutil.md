~~~txt
import psutil,time
from collections import Counter
print("--------------------------------------    基本信息 ----------------------------------")
print("系统上次启动时间:  "+str(time.strftime("%Y-%m-%d %H:%M:%W",time.localtime(psutil.boot_time()))))
print("cpu核数:   "+str(psutil.cpu_count()))
print("cpu利率:  "+str(psutil.cpu_percent(interval=5))+"%")
print("内存大小:  "+ str(int(psutil.virtual_memory().total / 1000000))+"M")
print("内存利率:  "+str(int(psutil.virtual_memory().used / psutil.virtual_memory().total *100))+"%")
for i in psutil.disk_partitions():
    print(f"{i.device} 挂载到 {i.mountpoint} 磁盘大小: " + str(round(psutil.disk_usage(i.mountpoint).total / 1000000000,3))+"G" )
    print(f"{i.device} 挂载到 {i.mountpoint} 磁盘剩余: " + str(round(psutil.disk_usage(i.mountpoint).free / 1000000000,3))+"G")
print("--------------------------------------    网卡流量 ----------------------------------")
for i in psutil.net_io_counters(pernic=True):
            print("发送流量:"  + str(int(psutil.net_io_counters(pernic=True)[i].bytes_sent / 1000000))+"M\t" + "  接收流量:" + str(int(psutil.net_io_counters(pernic=True)[i].bytes_recv / 1000000)) + "M\t网卡" + str(i))
print("--------------------------------------    连接数量 ----------------------------------")
ip=[]
for i in psutil.net_connections():
    if i.laddr.ip not in  '::1 0.0.0.0 ::127.0.0.1' and i.status == "ESTABLISHED":
       ip.append(i.raddr.ip)
for i in Counter(ip).most_common()[:20]:    #显示前20个
    print("IP连接数:  " + str(i[1])+ "\t\t"+str(i[0]))
print("--------------------------------------    活跃进程 ----------------------------------")
for i in psutil.process_iter():
    if i.status() == "running":
            print("PID: "+str(i.pid) + "  \t进程: "+str(i.name()) + "\t参数: " + str(i.cmdline()))
~~~
