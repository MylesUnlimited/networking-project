import socket
import random as r
import os
import os.path as path
import sys
import threading


server_address = '192.168.1.152'
port = 13000
BUFFER_SIZE = 1024
X = (r.randint(1,10000))

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)




pname = "peer"+ str(X)

def join_Network(name):
    udp_client_socket.sendto(b"J" + name.encode(), (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)

    if response[8:] == b"peer joined":
        print("Peer Joined")
        return int.from_bytes(response[:8], byteorder='big')



tcp_port = join_Network(pname)
tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
server_socket.bind(((socket.gethostbyname(hostname), tcp_port+1)))

print(socket.gethostbyname(hostname), tcp_port,"1")

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
'''
'''
def receive_file(address,file_name: str, file_size: int):

    tcp_client_socket.connect(address)
    tcp_client_socket.send(b"hello")
    reply = tcp_client_socket.recv(BUFFER_SIZE)
    if reply == b"ready":
        file_name += '.temp'

        with open(file_name, 'wb') as file:
            retrieved_size = 0
            try:
                while retrieved_size < file_size:
                    chunk = tcp_client_socket.recv(BUFFER_SIZE)
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

def tcp_client():

    try:
        while True:

            print(tcp_port)

            print("Started")

            server_socket.listen(1)

            conn,addr = server_socket.accept()

            conn.sendall(b'Ready')
            data = conn.recv(1024)
            if data == b"Cool":
                print("Awesome")



    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        tcp_client_socket.close()
        server_socket.close()

def udp_client():

    def request_file():
        udp_client_socket.sendto(b"R", (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"go ahead":
            filename = input("Filename: ")
            udp_client_socket.sendto(bytes(filename.encode()), (server_address, port))
            response, address = udp_client_socket.recvfrom(1024)
            tcp_ip, t_port = get_file_info(response)
            print(tcp_ip,t_port)
            tcp_client_socket.connect((tcp_ip,t_port+1))
            response = tcp_client_socket.recv(1024)
            if response == b"Ready":
                tcp_client_socket.send(b"Cool")

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


    try:
        while True:
            message = input("Message Type: ")

            if message == "U":
                upload_file()

            elif message == "R":
                request_file()

    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        udp_client_socket.close()

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=udp_client)
        t2 = threading.Thread(target=tcp_client)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    except KeyboardInterrupt as ki:
        print("Shutting down...")


