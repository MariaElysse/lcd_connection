#!/usr/bin/env python3
import lcd_connection.lcd_connection
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8080))
sock.listen(5)

lcd = lcd_connection.lcd_connection.LCDConnection("/dev/ttyAMA0")
lcd.clear()
while True:
    try:
        lcd.clear()
        (clientsocket, address) = sock.accept()
        received = clientsocket.recv(4096)
        print(received)
        lcd.write(received.decode('ascii'))
        clientsocket.close()

    except (KeyboardInterrupt, OSError):
        print("Exiting")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()      
        exit(0)
