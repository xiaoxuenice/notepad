~~~txt
## docker部署consul集群

### 1.在每台服务器上创建挂载的目录和文件 (注意修改集群IP）

mkdir -p /usr/local/consul/{config,consul-data,logs}
chown 100:1000 /usr/local/consul/logs/
cat > /usr/local/consul/config/consul.json <<EOF
{
"datacenter":"prod",
"primary_datacenter":"prod",
"start_join":["192.168.73.128","192.168.73.129"],
"retry_join":["192.168.73.128","192.168.73.129"],
"connect":{"enabled":true },

"enable_debug": false,
"rejoin_after_leave": true,

"retry_interval": "10s",
"encrypt":"9ByOop4YqKLlytN1J64MYUS9vh+vIBpyaqJtCyQLx/U=",
"enable_debug": false,

"log_file":"/opt/apps/logs/",
"log_level":"info",

"log_rotate_bytes":100000000,
"log_rotate_duration":"24h",
"log_rotate_max_files":10,
"enable_script_checks":false,
"enable_local_script_checks":true,
"disable_remote_exec":true
}
EOF
cat > /usr/local/consul/config/local.json << EOF
{"connect": {"enabled": true}}
EOF

### 2.在每台服务器上启动容器

localip=`route |grep defa|awk '{print $NF}'|xargs -I {}  ifconfig {}|grep "inet "|awk '{print $2}'`
docker run -d --net=host --name consul --restart always \
-v /usr/local/consul/consul-data:/consul/data \
-v /usr/local/consul/config:/consul/config \
-v /usr/local/consul/logs:/opt/apps/logs \
consul  consul agent -server \
-bind=$localip \
-bootstrap-expect 2 \
-client 0.0.0.0 \
-data-dir /consul/data \
-config-dir /consul/config \
-ui

### 3.查看投票状态，查询集群状态

docker exec -t consul consul operator raft list-peers
docker exec consul consul info

### 4.http://localhost:8500
~~~


~~~txt
### consul 单机部署
docker run -d -p 8500:8500 -h node1 --name node1  consul agent -server -bootstrap-expect=1  -node=node1 -client 0.0.0.0 -ui
### 集群成员
requests.get("http://192.168.73.128:8500/v1/catalog/nodes").text


### 注册服务
data={
  "id": "test1",
  "name": "prometheus",
  "address": "192.168.73.128",
  "port": 99,
  "meta": {
    "dev": "test"
  },
  "tags": [
    "prometheus"
  ],
  "EnableTagOverride": false,
  "checks": [
    {
      "http": "http://192.168.73.128:99/",
      "interval": "5s"
    }
  ]
}

requests.put("http://192.168.73.128:8500/v1/agent/service/register",data=json.dumps(data)).status_code

注释：ID 指定实例的唯一ID名称；
Name 指定服务名，可以多个实例共用服务名；
Tags 指定服务的标签列表，这些标签可用于过滤服务，并通过API进行公开；
Address 指定服务的实例地址；
Port 指定实例的端口号；
Meta 指定服务的元数据，格式为key:value，此处用于保存我们的标签信息；
EnableTagOverride 此处禁用服务标签的反熵功能；
Check 服务的检查列表，Consul会根据配置信息定时发起检查，确定服务是否正常；

### 删除服务 apiurl + ID
requests.put("http://192.168.73.128:8500/v1/agent/service/deregister/test1").status_code

### 查询所有服务组
json.loads(requests.get("http://192.168.73.128:8500/v1/catalog/services").text)

### 查询服务组详情 apiurl + Name
json.loads(requests.get("http://192.168.73.128:8500/v1/catalog/service/prometheus").text)

### 查询组服务健康检查通过|失败的服务
json.loads(requests.get("http://192.168.73.128:8500/v1/health/state/passing").text)
json.loads(requests.get("http://192.168.73.128:8500/v1/health/state/critical").text)



###  kv 写入
requests.put("http://192.168.73.128:8500/v1/kv/prometheus/host",data='{"test1":"192.168.73.128","test2":"192.168.73.129"}').text

###  kv 查询
_vaule=json.loads(requests.get("http://192.168.73.128:8500/v1/kv/prometheus/host").text)[0]['Value']
json.loads(base64.b64decode(_vaule).decode())

###  kv 删除
requests.delete("http://192.168.73.128:8500/v1/kv/prometheus/host").text
~~~

