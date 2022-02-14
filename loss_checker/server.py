import socket
from loss_checker.config import cfg


class Server:
    def __init__(self):
        pass

    def server_c(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((cfg['server_ip'], cfg['server_port']))
        while True:
            data, address = sock.recvfrom(1024)
            if data:
                print('received %s from %s' % (data.decode(), address))
                sock.sendto(data, address)
