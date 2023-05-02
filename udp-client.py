import socket
import random as r
import os
import os.path as path
import sys
import threading
import time


server_address = "192.168.1.155"
port = 13000
BUFFER_SIZE = 1024
X = (r.randint(1,10000))

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pname = "peer"+ str(X)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

tcp_IP = get_ip()

def join_Network(name):
    udp_client_socket.sendto(b"J" + name.encode(), (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)
    if response == b"need TCP address":
        udp_client_socket.sendto(tcp_IP.encode(), (server_address, port))
    response, address = udp_client_socket.recvfrom(1024)
    if response[8:] == b"peer joined":
        print(pname + " Joined")
        return int.from_bytes(response[:8], byteorder='big')

tcp_port = join_Network(pname)

#print(socket.gethostbyname(hostname), tcp_port,"1")

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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((tcp_IP, tcp_port))
    server_socket.listen(1)



    try:
        while True:

            print((tcp_IP, tcp_port))
            print("Started")
            conn, addr = server_socket.accept()

            isDone = False
            while not isDone:
                data = conn.recv(1024)
                if data == b"Connected":
                    conn.send(b'Ready')
                    data = conn.recv(1024) #file name
                    fname = data.decode()
                    fsize = get_file_size(data.decode())
                    conn.send((fsize).to_bytes(8,byteorder='big')) #sending file size
                    data = conn.recv(1024) #go ahead
                    if data != b'go ahead':
                         raise Exception('Bad server response - was not go ahead!')

                        # open the file to be transferred
                    with open(fname, 'rb') as file:
                    # read the file in chunks and send each chunk to the server
                        is_finished = False
                        while not is_finished:
                            chunk = file.read(BUFFER_SIZE)
                            if len(chunk) > 0:
                                conn.send(chunk)
                            elif len(chunk) == 0:
                                conn.close()
                                isDone = True



    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:
        server_socket.close()


def udp_client():

    def download_file(conn_socket: socket, file_name: str, file_size: int):
        # create a new file to store the received data
        file_name += '.temp'
        # please do not change the above line!
        with open(file_name, 'wb') as file:
            retrieved_size = 0
            try:
                while retrieved_size < file_size:
                    # TODO: section 1 step 6a
                    chunk = conn_socket.recv(BUFFER_SIZE)
                    retrieved_size += len(chunk)
                    file.write(chunk)
                    # TODO: section 1 stop 6b
                    # TODO: section 1 stop 6c
            except OSError as oe:
                print(oe)
                os.remove(file_name)

    def request_file():
        udp_client_socket.sendto(b"R", (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"go ahead":
            filename = input("Filename: ")
            udp_client_socket.sendto(bytes(filename.encode()), (server_address, port))
            response, address = udp_client_socket.recvfrom(1024)
            tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            peer_ip, peer_port = get_file_info(response)
            print(peer_ip,peer_port)

            tcp_client_socket.connect((peer_ip,peer_port))
            tcp_client_socket.send(b"Connected")
            response = tcp_client_socket.recv(1024)
            if response == b"Ready":
                fname = filename.encode()
                tcp_client_socket.send(bytes(fname))
            response = tcp_client_socket.recv(1024) #file size
            fsize = int.from_bytes(response,byteorder='big')
            tcp_client_socket.send(b"go ahead")
            download_file(tcp_client_socket,filename,fsize)
            tcp_client_socket.shutdown(socket.SHUT_RDWR)
            tcp_client_socket.close()



    def upload_file():
        udp_client_socket.sendto(b"U", (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"need TCP address":
            udp_client_socket.sendto(tcp_IP.encode(), (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"go ahead":
            filename = input("Filename: ")
            size = (get_file_size(filename)).to_bytes(8, byteorder='big')
            udp_client_socket.sendto(size + bytes(filename.encode()), (server_address, port))
            response, address = udp_client_socket.recvfrom(1024)
            if response == b"uploaded":
                print("file uploaded")
                return

    def remove_file(filename):
        namefile = bytes(filename.encode())
        udp_client_socket.sendto(b"D", (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)
        if response == b"need filename":
            udp_client_socket.sendto(namefile, (server_address, port))

        response, address = udp_client_socket.recvfrom(1024)
        if response == b"deleted":
            print("file deleted")

        else:
            print(response.decode())

    def exit_network(peer):
        peer1 = bytes(peer.encode())
        udp_client_socket.sendto(b"E", (server_address, port))
        response, address = udp_client_socket.recvfrom(1024)

        if response == b"need peername":
            udp_client_socket.sendto(peer1, (server_address, port))

        response, address = udp_client_socket.recvfrom(1024)
        if response == b"peer deleted":
            print("peer deleted")

        else:
            print(response.decode())

    try:
        while True:
            message = input("Message Type: ")

            if message == "U":
                upload_file()

            elif message == "R":
                request_file()

            if message == "D":
                name = input("Input File Name: ")
                remove_file(name)

            if message == "E":
                peer = input("Input Peer Name: ")
                exit_network(peer)

    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        udp_client_socket.close()

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=tcp_client)
        t2 = threading.Thread(target=udp_client)

        t1.start()
        time.sleep(0.01)
        t2.start()

        t1.join()
        t2.join()

    except KeyboardInterrupt as ki:
        print("Shutting down...")


