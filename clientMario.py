import socket
import select
import sys
import threading

if len(sys.argv) != 4:
	print("Ayuda: anda calla ya")
	exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = str(sys.argv[1])
port = int(sys.argv[2])
user = str(sys.argv[3])
server.connect((ip, port))
exit = False

"""user = ""
valid = False
while not valid:
	user = input("Nombre: ")
	if len(user) > 0 and len(user) < 20:
		valid = True"""

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

print('Nyu->')

while not exit:
	try:
		msg = input('<me>: ')
		if msg == "!q":
			exit = True
		msg2= user+'->'+msg
		server.send(msg2.encode("utf-8"))
		
	except(KeyboardInterrupt, SystemExit):
		stopandquit()

stopandquit()
