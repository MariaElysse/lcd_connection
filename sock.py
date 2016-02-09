#!/usr/bin/env python3
##
# Sender application for the lcd_daemon program
# messages typed in here are shown on the screen

import socket

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("raspberrypi.local", 8080))

sock.send(b"KAPPA KEEPO")
sock.close()
while True:
  sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    msg = input(">")
  except KeyboardInterrupt:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
  sock.connect(("raspberrypi.local", 8080))
  sock.send(bytes(msg,'utf-8'))
  sock.shutdown(socket.SHUT_RDWR)
  sock.close()
