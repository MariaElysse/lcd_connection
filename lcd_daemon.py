#!/usr/bin/env python3
##
# Example usage of the LCD Connection module
# (by example I mean the initial intention)
# Messages can be sent using the companion sender app, sock.py

import lcd_connection.lcd_connection
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8080))
sock.listen(5)

lcd = lcd_connection.lcd_connection.LCDConnection("/dev/ttyAMA0")
lcd.clear()
while True:
    try:
        (clientsocket, address) = sock.accept()
        received = clientsocket.recv(4096)
        print(received)
        lcd.clear()
        lcd.write(received.decode('ascii'))
        clientsocket.close()

    except (KeyboardInterrupt, OSError):
        print("Exiting")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()      
        exit(0)
