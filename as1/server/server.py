from socket import *
import sys
import random
import os
from pathlib import Path

if len(sys.argv) < 3:
    print("Client requires 2 arguments:\n1:<req_code>\n2:<file_to_send>")
    exit()

filepath = Path(('./' + sys.argv[2]))
if not filepath.is_file():
    print("file does not exist")
    exit()

req_code = sys.argv[1] #To verify with req_code sent by client
file_to_send = sys.argv[2] #.txt file

with open(file_to_send, 'r') as f:
    textlist = f.readlines()
text = ''
for i in textlist:
    text = text + i

#udp tcp Server set up
udpserverPort = 52500
udpserverSocket = socket(AF_INET, SOCK_DGRAM)
udpserverSocket.bind(('', udpserverPort))
print("SERVER_PORT = ", udpserverPort)
print("The udp server is ready to receive")

while True:
    message, clientAddress = udpserverSocket.recvfrom(2048)
    message = message.decode().split(" ")
    tcpserverSocket = socket(AF_INET,SOCK_STREAM)
    if message[1] == req_code:
        if message[0] == 'PORT':
            reply = "1"
            udpserverSocket.sendto(reply.encode(), clientAddress)
            r_port = int(message[2])
            tcpserverSocket.connect((clientAddress[0], r_port))
            tcpserverSocket.send(text.encode())
            tcpserverSocket.close()
        elif message[0] == 'PSV':
            r_port = random.randint(1025, 65535) #generate random port number
            tcpserverSocket.bind(('', r_port))
            reply = str(r_port)
            udpserverSocket.sendto(reply.encode(), clientAddress)
            tcpserverSocket.listen(1)
            connectionSocket, addr = tcpserverSocket.accept()
            connectionSocket.send(text.encode())
            connectionSocket.close()
    else:
        udpserverSocket.sendto("0".encode(), clientAddress)
        print("invalid req_code provided by client")