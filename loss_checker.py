import asyncio
import socket
import os
import sys
import ovcfg
import oe_common
import time
import datetime
from threading import Thread

sc = {
    'server_ip': '0.0.0.0',
    'ip_check_list': [],
    'server_port': 800,
}
# Auth types: password, keys, master_keys
cfg = ovcfg.Config(std_config=sc, file='loss_checker.json', cfg_dir_name='.', local=True).import_config()


class Server:
    def __init__(self):
        pass

    async def server(self):
        server = await asyncio.start_server(
            self.handle_echo,
            cfg['server_ip'],
            cfg['server_port'],

        )
        # asyncio.start_server()

    async def handle_echo(self, reader, writer):
        await self.Handle(reader, writer).handle()

    class Handle:
        def __init__(self, reader, writer):
            self.reader = None
            self.writer = None

        async def handle(self):
            data = await self.reader.read()
            message = data.decode()
            address = self.writer.get_extra_info('peername')
            print('Received from: %s : %s' % (address, message))
            self.writer.write(data)
            await self.writer.drain()
            self.writer.close()


def server_c():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((cfg['server_ip'], cfg['server_port']))
    while True:
        data, address = sock.recvfrom(1024)
        if data:
            print('received %s from %s' % (data.decode(), address))
            sock.sendto(data, address)


class Client:
    def __init__(self):
        self.sent_s = {}

    def client_c(self):
        i = 0
        while True:
            i += 1
            now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('%s check %s' % (now_date, i))
            for server in cfg['ip_check_list']:
                Thread(target=self.check_server, args=(server, )).start()
            time.sleep(5)

    def check_server(self, server):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        server_address = (server, cfg['server_port'])
        # print('server_address is:', server_address)
        message = oe_common.get_rnd_string(100)
        try:
            sent = sock.sendto(message.encode(), server_address)
            # print('sent', message)
            self.add_to_sent(server_address, message)
            data, address = sock.recvfrom(1024)
            # print('received %s from %s' % (data, address))
            ping = self.get_ping(server_address, message)
            print('%s ping: %s ms' % (server_address[0], round(ping.total_seconds() * 1000, 2)))

        except socket.timeout:
            print('%s: timeout' % server_address[0])
            self.del_from_sent(server_address, message)
        finally:
            sock.close()

    def add_to_sent(self, address, message):
        if address in self.sent_s:
            self.sent_s[address][message] = datetime.datetime.now()
        else:
            self.sent_s[address] = {message: datetime.datetime.now()}
        # print(self.sent_s)

    def del_from_sent(self, address, message):
        if address in self.sent_s:
            if message in self.sent_s[address]:
                del self.sent_s[address][message]

    def get_ping(self, address, message):
        if address in self.sent_s:
            if message in self.sent_s[address]:
                return datetime.datetime.now() - self.sent_s[address][message]
        raise RuntimeError('message not stored')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--client':
            Client().client_c()
        elif sys.argv[1] == '--server':
            server_c()
    else:
        Client().client_c()
