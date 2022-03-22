from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.ssh import SSH
from django.http.request import QueryDict
# from django.utils.six import StringIO
from LogTool_v3.settings import TMP_DIR
import os
import json
import base64


class WebSSH(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
        status 为 1 时, message 为具体的错误信息
    """

    def connect(self):
        """
        打开 websocket 连接, 通过前端传入的参数尝试连接 ssh 主机
         :return:
        """
        # self.host_id = self.scope['url_route']['kwargs'].get('host_id')
        # self.simple_user = self.scope["session"]["session_simple_nick_name"]
        self.accept()
        # query_string = self.scope.get('query_string')
        # ssh_args = QueryDict(query_string=query_string, encoding='utf-8')

    def sshConnect(self,ssh_args):
        width = ssh_args.get('width')
        height = ssh_args.get('height')
        width = int(width)
        height = int(height)

        auth = ssh_args.get('auth')
        # ssh_key_name = ssh_args.get('ssh_key')
        ssh_key_name=""
        passwd = ssh_args.get('password')

        host = ssh_args.get('host')
        port = ssh_args.get('port')
        port = int(port)
        user = ssh_args.get('user')
        docker_name = ssh_args.get('docker_name')

        # if passwd:
        #     passwd = base64.b64decode(passwd).decode('utf-8')
        # else:
        #     passwd = None

        self.ssh = SSH(websocker=self, message=self.message)

        ssh_connect_dict = {
            'host': host,
            'user': user,
            'password': passwd,
            'port': port,
            'timeout': 30,
            'pty_width': width,
            'pty_height': height,
            'docker_name': docker_name
        }

        # 不需要
        if auth == 'key':
            ssh_key_file = os.path.join(TMP_DIR, ssh_key_name)
            with open(ssh_key_file, 'r') as f:
                ssh_key = f.read()

            from six import StringIO
            string_io = StringIO()
            string_io.write(ssh_key)
            string_io.flush()
            string_io.seek(0)
            ssh_connect_dict['ssh_key'] = string_io

            os.remove(ssh_key_file)

        self.ssh.connect(**ssh_connect_dict)

    def disconnect(self, close_code):
        try:
            self.ssh.close()
        except:
            pass

    # def websocket_receive(self, message):
    #     # 浏览器基于websocket向后端发送数据，自动触发接收消息
    #     print('接收到消息', message)
    #     # self.send(text_data='收到了')


#等待用户输入，输入一个字符websocket收到后就启动两个进程，一个是发送字符到前端，一个是发送字符到ssh
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        from django_webssh import models
        # 要判断前端传来的是主页的消息，还是ssh中的命令消息，不一样的类型处理方式不一样
        if data.get('type')=="web":
            print('接收到消息，点击的type是：', data.get('type'))
            # 如果点击的是登录，就先插入数据库，然后和点击选项一样，查数据并链接ssh
            if len(data)>2:
                models.Serverinfo.objects.create(name=data.get('name'),host=data.get('host'),port=data.get('port'),user=data.get('user'),pwd=data.get('pwd'),docker_name=data.get('docker_name'))
            info=models.Serverinfo.objects.get(name=data.get('name'))
            ssh_args={"width":264,"height":23,"auth":"pwd","host":info.host,"user":info.user,"password":info.pwd,"port":info.port,"docker_name":info.docker_name}
            self.sshConnect(ssh_args)
            print("ssh链接的信息："+str(ssh_args))
        else:
            status = data['status']
            if status == 0:
                data = data['data']
                self.ssh.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.ssh.resize_pty(cols=cols, rows=rows)
