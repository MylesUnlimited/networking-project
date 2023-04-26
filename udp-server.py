import socket
import random as rand
import pandas as pd

my_address = '192.168.1.152'
port = 13000

peers = {"peer423":('127.0.0.1', 59755)}

files = {("test.png",25):"peer423"}


def peer_join(name, address):
    peers[name] = address
    print((address[1]))

    portnum = (address[1]).to_bytes(8, byteorder='big')

    server_socket.sendto(portnum+b"peer joined",(address[0],address[1]))

    print(f"{name} has joined")
    print(peers)

def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')

def upload_file(name, filename, filesize):
    files[(filename,filesize)] = name

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((my_address, port))
    print(f"Server is ready on {my_address}:{port}")
    try:
        while True:
            message, client_address = server_socket.recvfrom(1024)
            message_type = message[:1]

            if message_type == b"J":
                peer_name = message[1:].decode()
                peer_join(peer_name,client_address)

            if message_type == b"U":


            #send client address back to client

            #ize = int.from_bytes(size, byteorder='big')
            # message, client_address = server_socket.recvfrom(size)
            #response = ''.join(list(map(lambda ch: '' if ch in 'aeiou' else ch, message)))
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        server_socket.close()

