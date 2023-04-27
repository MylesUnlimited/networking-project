import socket

my_address = '127.0.0.1'
port = 13000

peers = {"peer1": ('127.0.0.1', 59755)}

files = {("test.png", 25): "peer1"}


def peer_join(address):
    name = "peer" + str(len(peers) + 1)
    peers[name] = address
    print((address[1]))

    portnum = (address[1]).to_bytes(8, byteorder='big')

    server_socket.sendto(portnum + b"peer joined", (address[0], address[1]))

    print(f"{name} has joined")
    print(peers)


def get_file_info(data: bytes) -> (str, int):
    return data[8:].decode(), int.from_bytes(data[:8], byteorder='big')


def get_peer(val):
    for key, value in peers.items():
        if val == value:
            return key

    return "key doesn't exist"


def upload_file(filename, filesize, address):
    name = get_peer(address)
    files[(filename, filesize)] = name
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

            if message_type == b"R":
                server_socket.sendto(b"need filename", (client_address))
                fileN, client_address = server_socket.recvfrom(1024)
                found = False
                j = 0
                for i in files:
                    if (list(files.keys())[j][0]) == fileN.decode():
                        server_socket.sendto(b"found", (client_address))
                        fileRecord = str(list(files.items())[j])
                        server_socket.sendto(fileRecord.encode(), (client_address))
                        fileInfo = list(files.keys())[j]
                        peerAddress = str(peers[files[fileInfo]])
                        server_socket.sendto(peerAddress.encode(), (client_address))

                        found = True
                        break
                    j += 1
                if found == False:
                    server_socket.sendto(fileN + b" not found", (client_address))

            if message == b"D":
                server_socket.sendto(b"need filename", (client_address))
                namefile, client_address = server_socket.recvfrom(1024)
                found = False
                a = 0
                for i in files:
                    if (list(files.keys())[a][0]) == namefile.decode():
                        server_socket.sendto(b"found", (client_address))
                        files.pop(list(files.keys())[a])
                        found = True
                        print(files)
                        break
                    a += 1
                if found == False:
                    server_socket.sendto(namefile + b" not found", (client_address))

                # print(fileN.decode())

            if message_type == b"J":
                peer_join(client_address)

            if message_type == b"U":
                server_socket.sendto(b"go ahead", (client_address))
                message, client_address = server_socket.recvfrom(1024)
                fname, fsize = get_file_info(message)
                upload_file(fname, fsize, client_address)

            # send client address back to client

            # ize = int.from_bytes(size, byteorder='big')
            # message, client_address = server_socket.recvfrom(size)
            # response = ''.join(list(map(lambda ch: '' if ch in 'aeiou' else ch, message)))
    except KeyboardInterrupt as ki:
        print("Shutting down...")
    finally:

        server_socket.close()

