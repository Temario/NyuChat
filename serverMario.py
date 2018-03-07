import socket
import sys
import threading

if len(sys.argv) != 3:
	print("Ayuda: "+sys.argv[0]+" IP puerto")
	exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip = str(sys.argv[1])
port = int(sys.argv[2])
server.bind((ip, port))
server.listen(100)
clients = []
exit = False

def clientthread(conn, addr):
	conn.send((" - Conectado a "+ip+" -").encode("utf-8"))
	while not exit:
		try:
			msg = conn.recv(2048).decode("utf-8")
			u=msg.split(': ')
			if u[1] == "!q":
				msg_send = " - "+u[0]+" se ha desconectado -"
			else:
				msg_send = msg
			print(msg_send)
			broadcast(msg_send, conn)
		except:
			remove(conn)
			break

def broadcast(msg, conn):
	for c in clients:
		if c != conn:
			try:
				c.send(msg.encode("utf-8"))
			except:
				c.close()
				remove(c)

def remove(conn):
	if conn in clients:
		clients.remove(conn)

def serverthread():
	while not exit:
		try:
			conn, addr = server.accept()
			clients.append(conn)
			print(" - "+addr[0]+" se ha conectado -")
			threading.Thread(target=clientthread, args=(conn, addr)).start()
		except:
			break

threading.Thread(target=serverthread).start()
print("Servidor en escucha, !q : salir")

while not exit:
	try:
		msg = input()
		if msg == "!q":
			exit = True
			server.close()
	except(KeyboardInterrupt, SystemExit):
		exit = True
		server.close()
		sys.exit()
