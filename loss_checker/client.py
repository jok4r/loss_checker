import socket
from loss_checker.config import cfg
from threading import Thread
import time
import datetime
import oe_common


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
            ping = self.get_ping(server_address, data.decode())
            print('%s ping: %s ms' % (server_address[0], round(ping.total_seconds() * 1000, 2)))

        except socket.timeout:
            print('%s: timeout' % server_address[0])
        finally:
            self.del_from_sent(server_address, message)
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

