# Loss checker

This module helps to check udp client/server packet loss. Can be run as client or server. Client send random string to server, waits for answer and when packet will receive, compare sended string with received and count time difference (ping). If packet is loss, answer will never be received and timeout will occur.

Module can be installed on multiple servers and checks on one client.

## Prerequisites

	- Python3.5 or newer

## Installion
$ python3 -m pip install loss_checker<br /><br />
**OR**<br /><br />
$ python3 -m pip install git+https://github.com/jok4r/loss_checker.git

## Usage / Eng

### Run as client

$ python3 -m loss_checker

### Run as server

$ python3 -m loss_checker --server


### Run server as a service

\**Can be run only on Linux*

$ python3 -m loss_checker --server --install

If you want to answer the question automatically (that the module will be installed as a service), add argument **-y**:

$ python3 -m loss_checker --server --install -y

And it will be installed and run as a service. You can check status, start and stop service with following commands:

$ service loss_checker status

$ service loss_checker start

$ service loss_checker stop

### Enabling and disabling service

$ systemctl enable loss_checker

$ systemctl disable loss_checker

### Uninstall service

$ python3 -m loss_checker --server --uninstall

You can add **-y** option to skip confirmation question:

$ python3 -m loss_checker --server --uninstall -y
