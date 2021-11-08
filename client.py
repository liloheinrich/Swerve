# the pi is meant to be the server, the laptop the client
# Level 1: https://raspberrypi.stackexchange.com/questions/13425/server-and-client-between-pc-and-raspberry-pi
# Level 2: https://notenoughtech.com/raspberry-pi/rpi-socket-protocol/
# Level 3: http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php

import socket

s = socket.socket()
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # ???
# host = '' # ip of raspberry pi 

print (host)
port = 12345

s.connect((host, port))
print (s.recv(1024))
s.close