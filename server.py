# Level 1: https://raspberrypi.stackexchange.com/questions/13425/server-and-client-between-pc-and-raspberry-pi
# Level 2: https://notenoughtech.com/raspberry-pi/rpi-socket-protocol/
# Level 3: http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php

# hostname -I
# hostname -i

import socket

# HOST = '' # Server IP or Hostname
# HOST = socket.gethostname()
# HOST = '127.0.1.1'
HOST = '10.27.91.11'
print("HOST = ", HOST)
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#managing error exception
try:
  s.bind((HOST, PORT))
except socket.error:
  print('Bind failed')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')

# awaiting for message
while True:
  data = conn.recv(1024)
  print('I sent a message back in response to: ' + data) 
  reply = ''

  # process your message
  if data == 'Hello':
    reply = 'Hi, back!'
  elif (data == 'This is important'):
    reply = 'OK, I have done the important thing you have asked me!'
  #and so on and on until...
  elif data == 'quit':
    conn.send('Terminating')
    break
  else:
    reply = 'Unknown command'

  # Sending reply
  conn.send(reply)
  
conn.close() # Close connections