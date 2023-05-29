~~~shell
pip3 install channels

[root@test1 ops]# ls
app  manage.py  media  ops  static  templates
[root@test1 ops]# ls app/
admin.py  apps.py  consumers.py  __init__.py  migrations  models.py  __pycache__  routing.py  tests.py  views.py
~~~

### vim settings.py
~~~shell
import os
INSTALLED_APPS = [
...
    'app',
    'channels',
]

ASGI_APPLICATION = 'app.routing.application'
CHANNEL_LAYERS= {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
            }
        }

'DIRS': [os.path.join(BASE_DIR,'templates')],
~~~
### [root@test1 ops]# cat app/consumers.py 
~~~shell
from channels.generic.websocket import WebsocketConsumer
import os,asyncio,threading,json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
class ChatConsumer(WebsocketConsumer):
  def websocket_connect(self, message):
            self.accept()
            self.send("ws 服务器端 连接成功 ！！")
  def thread(self,args):
      while True:
              asyncio.sleep(2)
              self.send(f" {args}JUST TEST ")
  def websocket_receive(self, message):
            """客户端发送数据过来  自动触发"""
            mess = json.loads(message)

            threading.Thread(target=self.thread,args=(mess,)).start()
  async def websocket_disconnect(self,message):
            print("ws 服务器端 断开连接 ！！")
~~~
### [root@test1 ops]# cat app/routing.py 
~~~shell
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from app import consumers

application = ProtocolTypeRouter({
        'websocket':URLRouter([
                    # websocket相关的路由
                            path('wsws/',consumers.ChatConsumer.as_asgi())
                                ])
        })

~~~
### [root@test1 ops]# cat ops/urls.py 
~~~shell
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ws),
]
~~~
### [root@test1 ops]# cat app/views.py
~~~shell
def ws(request):
    return render(request,'ws.html')


~~~
~~~txt

[root@test1 django-opsweb]# cat ops/asgi.py 
"""
ASGI config for ops project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os,django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ops.settings')
django.setup()
application = get_default_application()


~~~
## 启动命令 daphne支持websocket
## daphne  -b 0.0.0.0 -p 8888 ops.asgi:application 
### [root@test1 ops]# cat templates/ws.html 
~~~shell
<!DOCTYPE html >
<html>
	<head>
		    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		        <title>测试demo</title>
			    <!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
			        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css"
						                 integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
				    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	</head>
	<body>

		<div class="container">
			    <div style="height: 30px"></div>
			        <button type="button" id="execute_script" class="btn btn-success">查看日志</button>

				    <h4>日志内容:</h4>
				        <div style="height: 600px;overflow: auto;" id="content_logs">
						        <div id="messagecontainer" style="font-size: 16px;background-color: black;color: white">
								        </div>
									    </div>
		</div>
	</body>
	<script type="text/javascript">
		    // 点击按钮
		    $('#execute_script').click(function () {
			            // 新建websocket连接
			            const chatSocket = new WebSocket(
					                'ws://'
					                + window.location.host
					                + '/wsws/'
					            );

			            // 连接建立成功事件
			            chatSocket.onopen = function () {
					                console.log('WebSocket open');
					                //发送字符: laying_eggs到服务端
					                chatSocket.send(JSON.stringify({
								                'message': 'laying_eggs'
								            }));
					                console.log("发送完字符串laying_eggs");
					            };
			            // 接收消息事件
			            chatSocket.onmessage = function (e) {
					                {#if (e.data.length > 0) {#}
								            //打印服务端返回的数据
								            console.log('message: ' + e.data);
								            // 转换为字符串，防止卡死testestt
								            $('#messagecontainer').append(String(e.data) + '<br/>');
								            //滚动条自动到最底部
								            $("#content_logs").scrollTop($("#content_logs")[0].scrollHeight);
								            {# }#}
					            };
			            // 关闭连接事件
			            chatSocket.onclose = function (e) {
					                console.log("connection closed (" + e.code + ")");
					                chatSocket.send(JSON.stringify({
								                'message': 'close'
								            }));
					            }
			        });
	</script>
</html>
~~~
