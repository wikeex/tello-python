import socket
import asyncio
import functools


class Tello:
    def __init__(self, tello_ip):
        self.local_ip = ''

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self._bind_ip(self.local_ip, 8891, self.socket)

        self.tello_ip = tello_ip
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)

        self.response = None

    def _bind_ip(self, ip, port, s):
        """
        本地端口绑定方法，如果绑定失败则端口+1再递归执行。
        :param ip: tello ip
        :param port: 本地端口
        :param s: socket对象
        :return:
        """
        try:
            s.bind((self.local_ip, port))
            return port
        except OSError:
            # 绑定失败则表明该端口异常，递归
            return self._bind_ip(ip, port + 1, s)

    async def wait_response(self, command):
        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)

        self.response, ip = self.socket.recvfrom(1024)
        return self.response, ip

    def action_result(self, command, future):
        response = future.result()[0].decode('utf-8')
        ip = future.result()[1]
        print('%s, %s, %s' % (ip, command, response))
        if response == 'ok':
            ...
        elif 'error' in response:
            ...

    def send_command(self, command):
        """
        发送命令方法，原来想使用协程实现多线程一样的非阻塞效果，但是只实现了阻塞效果，
        后来想想阻塞也挺好的，能保证发送的命令和回复对应，就不该了。
        :param command:
        :return:
        """
        print('sending command: %s to %s' % (command, self.tello_ip))
        coroutine = self.wait_response(command)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(coroutine)
        task.add_done_callback(functools.partial(self.action_result, command))
        loop.run_until_complete(task)

