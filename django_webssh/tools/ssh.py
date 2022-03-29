import paramiko
from threading import Thread
from django_webssh.tools.tools import get_key_obj
import socket
import json

class SSH:
    def __init__(self, websocker, message):
        self.websocker = websocker
        self.message = message
        self.ssh_client = paramiko.SSHClient()

    def connect(self, host, user, password=None, ssh_key=None, port=22, timeout=30,
                term='xterm', pty_width=40, pty_height=24,docker_name=None):
        try:
            # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if ssh_key:
                key = get_key_obj(paramiko.RSAKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.DSSKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.ECDSAKey, pkey_obj=ssh_key, password=password) or \
                      get_key_obj(paramiko.Ed25519Key, pkey_obj=ssh_key, password=password)

                self.ssh_client.connect(username=user, hostname=host, port=port, pkey=key, timeout=timeout)
            else:
                self.ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)

            transport = self.ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()

            for i in range(3):
                recv = self.channel.recv(1024).decode('utf-8')
                self.message['status'] = 0
                self.message['message'] = recv
                message = json.dumps(self.message)
                self.websocker.send(message)
                if i==0:
                    dockerId=self.get_dockerId(docker_name)
                    command="docker logs -f --tail 100 "+dockerId
                    self.django_to_ssh(command)
        except socket.timeout:
            self.message['status'] = 1
            self.message['message'] = 'ssh 连接超时'
            message = json.dumps(self.message)
            self.websocker.send(message)
            self.close()
        except:
            self.close()

    # 获取dockerId
    def get_dockerId(self, logname):
        result = self.exec_command('docker ps')
        new = result.split('\n')
        containerId = '不知道'
        for i in new:
            print(i)
            if logname in i:
                containerId = i.split('   ')[0]
        print('容器id是： ' + containerId)
        return containerId

    def exec_command(self,command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        result = stdout.read().decode("utf-8")
        return result

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    #一个是发送字符到ssh
    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
        except:
            self.close()


    #一个是发送字符到前端展示出来
    def websocket_to_django(self):
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                if not len(data):
                    return
                self.message['status'] = 0
                self.message['message'] = data
                message = json.dumps(self.message)
                self.websocker.send(message)
        except:
            self.close()

    def close(self):
        self.message['status'] = 1
        self.message['message'] = '关闭连接'
        message = json.dumps(self.message)
        self.websocker.send(message)
        self.channel.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.django_to_ssh, args=(data,)).start()
        Thread(target=self.websocket_to_django).start()
