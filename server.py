# Level 1: https://raspberrypi.stackexchange.com/questions/13425/server-and-client-between-pc-and-raspberry-pi
# Level 2: https://notenoughtech.com/raspberry-pi/rpi-socket-protocol/
# Level 3: http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php

# hostname -I
# hostname -i

import socket

s = socket.socket()
host = socket.gethostname()
# host = '' #ip of raspberry pi
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print ('Got connection from',addr)
  c.send('Thank you for connecting')
  c.close()