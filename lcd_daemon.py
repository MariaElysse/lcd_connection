import lcd_connection.lcd_connection
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8080))
sock.listen(5)

lcd = lcd_connection.lcd_connection.LCDConnection("/dev/ttyAMA0")

while True:
    try:
        (clientsocket, address) = sock.accept()
        received = clientsocket.recv(2048)
        lcd.write(received)
    except KeyboardInterrupt:
        print("Exiting")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()