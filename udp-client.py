import socket
import random as r
import os.path as path
import sys


server_address = '192.168.1.152'
port = 13000
X = (r.randint(1,10000))

name = "peer"+ str(X)

'''
def send_file( address: (str, int),filename: str):
    # get the file size in bytes
    # TODO: section 2 step 2
    file_size = get_file_size(filename)
    # convert file_size to an 8-byte byte string using big endian
    # TODO: section 2 step 3
    size = (file_size).to_bytes(8, byteorder='big')
    name = filename.encode()

    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # TODO: section 2 step 5
        client_socket.connect((IP,PORT))
        # send the file size in the first 8-bytes followed by the bytes
        # for the file name to server at (IP, PORT)
        # TODO: section 2 step 6
        message = size + name
        # TODO: section 2 step 7
        client_socket.sendto(message, (IP, PORT))
        reply = client_socket.recv(BUFFER_SIZE)
        if reply != b'go ahead':
            raise Exception('Bad server response - was not go ahead!')

        # open the file to be transferred
        with open(file_name, 'rb') as file:
            # read the file in chunks and send each chunk to the server
            is_done = False
            while not is_done:
                chunk = file.read(BUFFER_SIZE)
                if len(chunk) > 0:
                    client_socket.send(chunk)
                elif len(chunk) == 0:
                    is_done = True

                # TODO: section 2 step 8a
                # TODO: section 2 step 8b
    except OSError as e:
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        client_socket.close()


#def request_file(filename, address):



def upload_file(conn_socket: socket, file_name: str, file_size: int):
    # create a new file to store the received data
    file_name = 'ad-Image'
    open('ImageWasModified', 'w')
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


'''

def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size

def request_file(filename):
    file = bytes(filename.encode())
    udp_client_socket.sendto(file,(server_address,port))

    response,address = udp_client_socket.recvfrom(1024)

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

            if message == "J":
                tcp_port = join_Network(name)
                print(tcp_port)
                server_socket.bind((socket.gethostbyname(hostname), tcp_port))

            if message == "U":
                upload_file()

            '''
            if response == b"request":
                client_socket.send(b"go ahead")
                file, address = client_socket.recvfrom(1024)
                send_file( file,address)
            '''

            #print(f'Response from {address[0],address[1]} is "{response.decode()}"')
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        udp_client_socket.close()
        tcp_client_socket.close()
        server_socket.close()