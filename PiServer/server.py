# echo-server.py

import socket
from tree import RGBXmasTree
from time import sleep

tree = RGBXmasTree()

HOST = ""  # Standard loopback interface address (localhost)
PORT = 65436  # Port to listen on (non-privileged ports are > 1023)

def updateTree(datastring):
	brokenstring = datastring.split(",")
	print(brokenstring)
	tree[int(brokenstring[0])].color = (float(brokenstring[1]),float(brokenstring[2]),float(brokenstring[3]))

def close():
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    tree.color = (0,0,0)
    print ("closed")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                close()
                break
            #conn.sendall(data)
            #print(data)
            updateTree(data)
