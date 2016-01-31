import socket

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8080))

sock.send(b"KAPPA KEEPO")
sock.close()
while True:
  sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(("127.0.0.1", 8080))

  msg = input(">")
  sock.send(bytes(msg,'utf-8'))
  sock.close()
