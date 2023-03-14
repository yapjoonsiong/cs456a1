from socket import *
import sys
import random

if len(sys.argv) < 6:
    print("Client requires 5 arguments:\n1:<server_address>\n2: <n_port> (Should match n_port of server)\n3: <mode> (A [Active] or P [Passive]\n4: <req_code> (Should match req_code of server)\n5: <file_received> (must be a text file: format: XYZ.txt)")
    exit()

#udp tcp client setup
server_address = sys.argv[1]

if (int(sys.argv[2]) < 1025) or (int(sys.argv[2]) > 65535):
    print("n_port out of range. please enter integer from set [1025, 65535] matching server n_port")
    exit()
n_port = int(sys.argv[2]) #udp Server port 52500

if sys.argv[3] != 'P' and sys.argv[3] != 'A':
    print("Mode can only be 'A' or 'P'")
    exit()
mode = sys.argv[3] #P or A for passive or active

req_code = sys.argv[4] #Must be same as server

if not sys.argv[5][-4:] == '.txt':
    print("file name must be a txt file with file extension .txt")
    exit()
file_received = sys.argv[5] #tzt file with .txt extension

udpclientSocket = socket(AF_INET, SOCK_DGRAM)
tcpclientSocket = socket(AF_INET, SOCK_STREAM)

#message to send
if mode == 'A':
    r_port = random.randint(1025, 65535) #generate random port number
    msg = f"PORT {req_code} {r_port}"
elif mode == 'P':
    msg = f"PSV {req_code}"

#message and reply
udpclientSocket.sendto(msg.encode(), (server_address, n_port))
reply, serverAddress = udpclientSocket.recvfrom(2048)
reply = reply.decode()
udpclientSocket.close()

if reply == '0':
    print("req_code is invalid")
    exit()

if mode == 'A':
    tcpclientSocket.bind(('', r_port))
    tcpclientSocket.listen(1)
    connectionSocket, addr = tcpclientSocket.accept()
    text_received = connectionSocket.recv(1024)
    connectionSocket.close()
elif mode == 'P':
    r_port = int(reply)
    tcpclientSocket.connect((server_address,r_port))
    text_received = tcpclientSocket.recv(1024)
    tcpclientSocket.close()

text = text_received.decode()

#write file to txt
with open (file_received, 'w') as f:
    f.write(text)

