import os.path
import sys
from loss_checker import Client
from loss_checker import Server
import shutil
import pathlib
import oe_common
import signal


def signal_handler(sig, frame):
    print("Pressed Ctrl+C, exiting...")
    os.kill(os.getpid(), signal.SIGTERM)


if len(sys.argv) > 1:
    if sys.argv[1] == '--client':
        Client().client_c()
    elif sys.argv[1] == '--server':
        if len(sys.argv) > 2:
            daemon_name = 'loss_checker'
            if sys.argv[2] == '--install':
                if os.name != 'posix':
                    raise RuntimeError("Unsupported OS")
                question = 'Script will be installed as a service, continue? [y/n]: '
                # sys.stdout.write(question)
                if len(sys.argv) > 3 and sys.argv[3] == '-y':
                    choice = 'y'
                else:
                    print(question, end='')
                    choice = input().lower()
                if choice == 'y':
                    print('Installing as a service')
                    shutil.copy(
                        os.path.join(
                            os.path.dirname(os.path.abspath(__file__)),
                            'cfg/%s.service' % daemon_name
                        ),
                        '/lib/systemd/system'
                    )
                    os.system('systemctl enable %s' % daemon_name)
                    os.system('systemctl start %s' % daemon_name)
                    os.system('systemctl daemon-reload')
                    os.system('systemctl status %s' % daemon_name)
                else:
                    print('Install canceled')
                sys.exit(0)
            elif sys.argv[2] == '--uninstall':
                if os.name != 'posix':
                    raise RuntimeError("Unsupported OS")
                question = 'Servce %s will be uninstalled, continue? [y/n]: '
                print(question, end='')
                choice = input().lower()
                if choice == 'y' or (len(sys.argv) > 3 and sys.argv[3] == '-y'):
                    os.system('systemctl disable %s' % daemon_name)
                    os.system('systemctl stop %s' % daemon_name)
                    os.system('systemctl daemon-reload')
                    oe_common.rm(os.path.join('/lib/systemd/system', '%s.service' % daemon_name))
                else:
                    print("Removing canceled")
                sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        Server().server_c()
else:
    signal.signal(signal.SIGINT, signal_handler)
    Client().client_c()
