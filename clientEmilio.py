"""
Sencillo chat de terminal multiplataforma pensado para redes locales.
Escrito en Python 3.6.4
"""

import sys
import time
import socket
import threading

# Variable de salida.
exit = False

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

ip = sys.argv[1]

try:
    port = int(sys.argv[2])
except(ValueError):
    helpmsg("Error: El puerto debe ser un valor numérico entero.")

if port < 0 or port > 65535:
    helpmsg("Error: Puerto fuera del rango válido [0-65535].")

# Pide el nombre de usuario.
valid = False
while not valid:
    user = input("Nombre: ")
    if len(user) > 0 and len(user) <= 20:
        valid = True

# Función de salida.
def stopandquit():
    exit = True
    server.close()
    sys.exit()

# Hilo de escucha del servidor.
def serverthread():
    while not exit:
        try:
            msg = server.recv(2048).decode("utf-8")
            if msg == "!q":
                print(time.strftime("%H:%M:%S")+" - El servidor se ha desconectado -")
                stopandquit()
            else:
                print(msg)
        except:
            break

# Crea el socket TCP servidor e intenta conectar con el mismo.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))

# Empieza el hilo de escucha del servidor.
threading.Thread(target=serverthread).start()

# Ayuda al inicio.
print("!q : salir")

# Bucle principal. Espera entrada y envía mensajes al servidor.
while not exit:
    try:
        msg = input()
        if msg == "!q":
            server.send(msg.encode("utf-8"))
            exit = True
        else:
            server.send(("["+user+"]: "+msg).encode("utf-8"))
    except: #(KeyboardInterrupt, SystemExit):
        stopandquit()

stopandquit()
