import socket
import select
import sys
import threading
import time

if len(sys.argv) != 4:
	print("Ayuda: Argumentos erroneos")
	exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = str(sys.argv[1])
port = int(sys.argv[2])
user = str(sys.argv[3])
server.connect((ip, port))
exit = False

print("!q : salir")

def serverthread():
	while not exit:
		try:
			msg = server.recv(2048)
			print(msg.decode("utf-8"))
		except:
			break

threading.Thread(target=serverthread).start()

def stopandquit():
	exit = True
	server.close()
	sys.exit()
print(user)
while not exit:
	try:
		msg = input()
		if msg == "!q":
			exit = True
		msg2= '['+time.strftime("%H:%M:%S")+']'+user+': '+msg
		server.send(msg2.encode("utf-8"))
		print('['+time.strftime("%H:%M:%S")+']My: '+msg)
	except(KeyboardInterrupt, SystemExit):
		stopandquit()

stopandquit()
