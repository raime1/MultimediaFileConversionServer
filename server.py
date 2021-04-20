import socket 
import threading
import tqdm
import uuid
import os
import shutil

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 4096
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        receive_file(conn)
        connected = False
        '''
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            '''

    conn.close()
        
def receive_file(conn):
    filesize = conn.recv(HEADER).decode(FORMAT)
    filesize = int(filesize)

    rd_name = uuid.uuid1().hex
    os.makedirs(rd_name)

    progress = tqdm.tqdm(range(filesize), f"Receiving copy.txt", unit="B", unit_scale=True, unit_divisor=1024)
    with open(f"{rd_name}/{rd_name}.{input_ext}", "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = conn.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
        print("File transfer done...")
        f.close()
    
    #shutil.rmtree(f"./{rd_name}")
    #print("Folder was deleted")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def main():
    print("[STARTING] Server is starting...")
    start()

main()