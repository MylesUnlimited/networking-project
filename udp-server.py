import socket
import random as rand
import pandas as pd

my_address = '192.168.1.155'
port = 13000
f = open("test.txt","r+")
t = f.read()
if ("Peer_Name,Peer_Address\n") not in t:
    f.write("Peer_Name,Peer_Address\n")
    f.close()
else:
    f.close()
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((my_address, port))
    print(f"Server is ready on {my_address}:{port}")
    try:
        while True:
            f = open("test.txt","a")
            message, client_address = server_socket.recvfrom(1024)
            message_type = message[:1]
            peer_name = message[1:].decode()
            #ize = int.from_bytes(size, byteorder='big')
            print(f'message type = {message_type} and peer = {peer_name}')
            # message, client_address = server_socket.recvfrom(size)
            #response = ''.join(list(map(lambda ch: '' if ch in 'aeiou' else ch, message)))
            response = peer_name
            f.write(peer_name+','+str(client_address)+'\n')
            f.close()
            server_socket.sendto(response.encode(), client_address)
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        server_socket.close()
