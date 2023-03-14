In server folder, first run ./server.sh <req_code> sent.txt
<req_code> can be any preferred string without spaces, and 'sent.txt' is a preloaded txt file to be sent

In client folder, run ./client.sh <server_address> <n_port> <mode> <req_code> <received.txt>
<server_address>, use localhost or 127.0.0.1
<n_port> must be an integer that matches that of server
<mode> can be either A or P for Active or Passive
<req_code> must match that of server
<received.txt> can be your preferred name but must have the suffix .txt

the received.txt will be saved to the client folder