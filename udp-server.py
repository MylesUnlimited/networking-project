import socket


my_address = '127.0.0.1'
port = 13000

peers = {"peer423":('127.0.0.1', 59755)}

files = {("test.png",25):"peer423"}


def peer_join(name, address, tAddress):
    peers[name] = tAddress
    print((address[1]))

    portnum = (address[1]).to_bytes(8, byteorder='big')

    server_socket.sendto(portnum+b"peer joined",(address[0],address[1]))

    print(f"{name} has joined")
    print(peers)

def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')

def get_peer(val):
    for key, value in peers.items():
        if val == value:
            return key
    return "key doesn't exist"

def get_value(keyname):
    for key, value in files.items():

        if keyname == key[0]:
            return value

    return "key doesn't exist"

def get_ip(peername):
    for key, value in peers.items():
        print((key))
        if peername == key:
            return value

    return "key doesn't exist"

def find_file(filename, address):
    ip, port = get_ip(get_value(filename))

    port = (port).to_bytes(8, byteorder='big')
    ip = ip.encode()
    server_socket.sendto(port+bytes(ip), (address))

def upload_file(filename, filesize, address, tAddress):
    name = get_peer(tAddress)
    files[(filename,filesize)] = name
    print(files)
    server_socket.sendto(b"uploaded", (address))

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
                server_socket.sendto(b"need TCP address", (client_address))
                t_Ip, client_address = server_socket.recvfrom(1024)
                tcp_Address = (t_Ip.decode(), client_address[1])
                peer_join(peer_name,client_address, tcp_Address)

            if message_type == b"U":
                server_socket.sendto(b"need TCP address", (client_address))
                t_Ip, client_address = server_socket.recvfrom(1024)
                tcp_Address = (t_Ip.decode(), client_address[1])
                server_socket.sendto(b"go ahead", (client_address))
                message, client_address = server_socket.recvfrom(1024)
                fname, fsize = get_file_info(message)
                upload_file(fname,fsize,client_address, tcp_Address)

            if message_type == b"R":
                server_socket.sendto(b"go ahead", (client_address))
                message, client_address = server_socket.recvfrom(1024)
                print(message.decode())
                find_file(message.decode(),client_address)

            if message == b"D":
                server_socket.sendto(b"need filename", (client_address))
                namefile, client_address = server_socket.recvfrom(1024)
                found = False
                a = 0
                for i in files:
                    if (list(files.keys())[a][0]) == namefile.decode():
                        server_socket.sendto(b"deleted", (client_address))
                        files.pop(list(files.keys())[a])
                        found = True
                        print(files)
                        break
                    a += 1
                if found == False:
                    server_socket.sendto(namefile + b" not found", (client_address))

            if message == b"E":
                server_socket.sendto(b"need peername", (client_address))
                peer1, client_address = server_socket.recvfrom(1024)
                found = False
                b = 0
                for i in peers:
                    if (list(peers.keys())[b]) == peer1.decode():
                        server_socket.sendto(b"peer deleted", (client_address))
                        peers.pop(list(peers.keys())[b])
                        found = True
                        print(peers)
                        break
                    b += 1
                if found == False:
                    server_socket.sendto(peer1 + b" not found", (client_address))

    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        server_socket.close()

