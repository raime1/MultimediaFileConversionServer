import socket 
import threading
import uuid
import os
import shutil
import ffmpeg

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 4096
DISCONNECT_MESSAGE = "!DISCONNECT"
SEPARATOR = "<SEPARATOR>"

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
    info = conn.recv(BUFFER_SIZE).decode(FORMAT)
    input_ext, output_ext, filesize = info.split(SEPARATOR)
    
    rd_name = uuid.uuid1().hex
    os.makedirs(rd_name)

    input_file = f"{rd_name}/{rd_name}{input_ext}"
    output_file = f"{rd_name}/{rd_name}{output_ext}"
    filesize = int(filesize)
    print(f"Receiving file...{filesize}")
    #progress = tqdm.tqdm(range(filesize), f"Receiving {input_ext}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(input_file, "wb") as f:
        received_data = 0
        while received_data < filesize:
            # read 1024 bytes from the socket (receive)
            print("Receiving data...")
            bytes_read = conn.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                print("Data received...")
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            received_data += len(bytes_read)
            print(received_data)
            #progress.update(len(bytes_read))
        print("File transfer done...")
        f.close()
    print("FILE TRANSFER DONE...")
    try:
        print(input_file)
        print(output_file)
        ffmpeg.input(input_file).output(output_file).run(capture_stdout= False,capture_stderr=True, overwrite_output=True)
        print("Conversion done...")
        #out, err = ffmpeg.input(input_file).output('pipe:', format = 'mp4').run(capture_stdout= True, capture_stderr=True))
        
        filesize = os.path.getsize(output_file)
        conn.send(f"True{SEPARATOR}{filesize}".encode(FORMAT))
        print(f"True{SEPARATOR}{filesize}")
        with open(output_file, "rb") as f:
            bytes_read = f.read(BUFFER_SIZE)
            while bytes_read: 
                conn.sendall(bytes_read)
                bytes_read = f.read(BUFFER_SIZE)
            f.close()
        conn.close()
    except Exception as e:
        print(f"Error in the conversion process: {e.stderr}")
        conn.send(f"False{SEPARATOR}{e.stderr}".encode(FORMAT))
        print("False{SEPARATOR}{e.stderr}")
        conn.close()
    finally:   
        shutil.rmtree(f"./{rd_name}")
        print("Folder was deleted")


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