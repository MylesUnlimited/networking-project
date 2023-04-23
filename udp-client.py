import socket
import random as r


server_address = '192.168.1.155'
port = 13000
X = (r.randint(1,10000))
name = "peer"+ str(X)

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        while True:
            message = input("What's your message: ")
            message_type = b'R'
            client_socket.sendto(message_type + name.encode(), (server_address, port))
            response, address = client_socket.recvfrom(1024)
            print(f'Response from {address[0],address[1]} is "{response.decode()}"')
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        client_socket.close()
