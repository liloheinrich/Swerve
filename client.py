# the pi is meant to be the server, the laptop the client
# Level 1: https://raspberrypi.stackexchange.com/questions/13425/server-and-client-between-pc-and-raspberry-pi
# Level 2: https://notenoughtech.com/raspberry-pi/rpi-socket-protocol/
# Level 3: http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php

import socket

HOST = '10.27.91.11' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
    command = raw_input('Enter your command: ')
    s.send(command)
    reply = s.recv(1024)
    if reply == 'Terminate':
        break
    print(reply)
