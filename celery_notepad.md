~~~shell
pip3 install celery==5.0.5
pip3 install redis=3.5.3

docker run -p 6379:6379 --restart always --name redis -d redis

[root@test celery]# tree
.
`-- project
    |-- config.py
    |-- __init__.py
    `-- tasks.py

[root@test celery]# cat project/config.py
BROKER_URL = 'redis://127.0.0.1:6379/1' # Broker配置，使用Redis作为消息中间件

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2' # BACKEND配置，这里使用redis

CELERY_RESULT_SERIALIZER = 'json' # 结果序列化方案

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间

CELERY_TIMEZONE='Asia/Shanghai'   # 时区配置

CELERY_IMPORTS = (     # 指定导入的任务模块,可以指定多个
    'project.tasks',
)


[root@test celery]# cat project/__init__.py
from celery import Celery
app = Celery('project')                                # 创建 Celery 实例
app.config_from_object('project.config')               # 加载配置模块


[root@test celery]# cat project/tasks.py
from project import app
import time
@app.task
def show_name(name):
    time.sleep(10)
    return name


In [4]: from project import tasks

In [5]: t = tasks.show_name.delay('yayaya')

In [6]: t.status

In [7]: from celery.result import AsyncResult

In [8]: AsyncResult(id=t.id).state

~~~
