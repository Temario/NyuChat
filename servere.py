"""
Sencillo chat de terminal multiplataforma pensado para redes locales.
Escrito en Python 3.6.4
"""

import sys
import time
import socket
import threading

# Mensaje de ayuda cuando no se proporcionan dos argumentos.
def helpmsg(str):
    print(str)
    sys.exit()

if len(sys.argv) != 3:
    helpmsg("Ayuda: "+sys.argv[0]+" IP puerto")

# Valida los parámetros y los pasa a variables.
try:
    socket.inet_pton(socket.AF_INET, sys.argv[1])
except(OSError):
    helpmsg("Error: dirección IP inválida.")

ip = str(sys.argv[1])

try:
    port = int(sys.argv[2])
except(ValueError):
    helpmsg("Error: El puerto debe ser un valor numérico entero.")

if port < 0 or port > 65535:
    helpmsg("Error: Puerto fuera del rango válido [0-65535].")

# Crea el socket TCP servidor y establece los parámetros.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Escucha del socket servidor en la IP y el puerto.
try:
    server.bind((ip, port))
except(OSError):
    helpmsg("Error: Puerto ya en uso.")
except(socket.gaierror):
    helpmsg("Error: No se ha podido crear el socket en "+ip+":"+port+".")

server.listen(100) # Hasta 100 clientes simultáneos. Editar si es necesario.

# Array de sockets de clientes y variable de salida.
clients = []
exit = False

# Función de eliminación de cliente del array.
def remove(conn):
    if conn in clients:
        clients.remove(conn)

# Función de envío de mensajes a todos los clientes.
def broadcast(msg, conn):
    for c in clients:
        #if c != conn: # Descomentar para no enviar los mensajes de vuelta al emisor.
        try:
            c.send(msg.encode("utf-8"))
        except:
            c.close()
            remove(c)
            
def fichero(texto):
    ano=time.strftime("%y-%m-%d")
    reg=open(ano+"-log.txt","a")
    reg.write(' - '+texto+'\n')
    reg.close()

# Hilos de clientes.
def clientthread(conn, addr):
    conn.send((time.strftime("%H:%M:%S")+" - Conectado a ["+ip+"] -").encode("utf-8"))
    while not exit:
        try:
            msg = conn.recv(2048).decode("utf-8")
            if msg == "!q":
                msg_send = " - ["+addr[0]+"] se ha desconectado -"
            else:
                msg_send = " ["+addr[0]+"] "+msg
            msg_send = time.strftime("%H:%M:%S")+msg_send
            print(msg_send)
            fichero(msg_send)
            broadcast(msg_send, conn)
        except:
            remove(conn)
            break

# Hilo del servidor.
def serverthread():
    while not exit:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            msg_send = time.strftime("%H:%M:%S")+" - ["+addr[0]+"] se ha conectado -"
            print(msg_send)
            fichero(msg_send)
            threading.Thread(target=clientthread, args=(conn, addr)).start()
        except:
            break

# Empieza el hilo servidor.
threading.Thread(target=serverthread).start()

# Ayuda al inicio.
msg_send = time.strftime("%H:%M:%S")+" Servidor Iniciado"
print("Servidor en escucha, !q : salir")
fichero(msg_send)

# Bucle principal. Espera entrada y envía mensajes del servidor.
while not exit:
    try:
        msg = input()
        if msg == "!q":
            msg_send = time.strftime("%H:%M:%S")+" - Servidor cerrado"
            fichero(msg_send)
            broadcast("!q", None)
            exit = True
            for c in clients:
                c.close()
                clients.remove(c)
            server.close()
        elif msg.split(" ")[0] == "ban":
            for c in clients:
                recogerip = str(c.getpeername()).split("'")[1]
                if recogerip == msg.split(" ")[1]:
                    c.send((time.strftime("%H:%M:%S ")+" Has sido baneado del servidor. ").encode("utf-8"))
                    c.close()
                    remove(c)
                    msg_send = time.strftime("%H:%M:%S ")+ recogerip + " fue baneado"
                    print(msg_send)
                    fichero(msg_send)
                    broadcast(msg_send.encode("utf-8"), None)
        else:
            msg_send =time.strftime("%H:%M:%S")+" [Servidor]: "+msg
            fichero(msg_send)
            broadcast(msg_send, None)
    except: #(KeyboardInterrupt, SystemExit):
        exit = True
        msg_send = time.strftime("%H:%M:%S")+"Servidor cerrado por excepcion"
        fichero(msg_send)
        server.close()
        sys.exit()