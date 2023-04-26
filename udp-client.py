import socket
import random as r
#import os
import os.path as path
import sys


server_address = '192.168.1.152'
port = 13000
BUFFER_SIZE = 1024
X = (r.randint(1,10000))

name = "peer"+ str(X)

def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')
'''
def send_file( address: (str, int),filename: str):
    file_size = get_file_size(filename)
    size = (file_size).to_bytes(8, byteorder='big')
    name = filename.encode()



    try:
        message = size + name
        client_socket.sendto(message, address)
        reply = client_socket.recv(BUFFER_SIZE)
        if reply != b'go ahead':
            raise Exception('Bad server response - was not go ahead!')

        # open the file to be transferred
        with open(filename, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            is_done = False
            while not is_done:
                chunk = file.read(BUFFER_SIZE)
                if len(chunk) > 0:
                    client_socket.send(chunk)
                elif len(chunk) == 0:
                    is_done = True

    except OSError as e:
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        client_socket.close()

def receive_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data

    file_name += '.temp'
    # please do not change the above line!
    with open(file_name, 'wb') as file:
        retrieved_size = 0
        try:
            while retrieved_size < file_size:
                chunk = conn_socket.recv(BUFFER_SIZE)
                retrieved_size += len(chunk)
                file.write(chunk)

        except OSError as oe:
            print(oe)
            os.remove(file_name)
'''
def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size

def request_file():
    udp_client_socket.sendto(b"R", (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)
    if response == b"go ahead":
        filename = input("Filename: ")
        udp_client_socket.sendto(bytes(filename.encode()), (server_address, port))
        response,address = udp_client_socket.recvfrom(1024)
        tcpport, tcpip = get_file_info(response)
        print(f'{tcpport}, {tcpip} has the file')


def upload_file():
    udp_client_socket.sendto(b"U", (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)
    if response == b"go ahead":
        filename = input("Filename: ")
        size = (get_file_size(filename)).to_bytes(8, byteorder='big')
        udp_client_socket.sendto(size + bytes(filename.encode()), (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"uploaded":
            print("working")
            return

def join_Network(name):

    udp_client_socket.sendto(b"J" + name.encode(), (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)

    if response[8:] == b"peer joined":
        print("Peer Joined")
        return int.from_bytes(response[:8],byteorder='big')


if __name__ == "__main__":
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()

    try:
        while True:
            message = input("Message Type: ")
            message_type = bytes(message.encode())
            '''
            reply = tcp_client_socket.recv(BUFFER_SIZE)

            if reply == b"request":
                tcp_client_socket.send(b"ready")
            '''

            if message == "J":
                tcp_port = join_Network(name)
                print(tcp_port)
                server_socket.bind((socket.gethostbyname(hostname), tcp_port))

            if message == "U":
                upload_file()

            if message == "R":
                request_file()

            #print(f'Response from {address[0],address[1]} is "{response.decode()}"')
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        udp_client_socket.close()
        tcp_client_socket.close()
        server_socket.close()