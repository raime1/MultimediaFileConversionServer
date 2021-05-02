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
        
def receive_file(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    #Receiving initial info about the file
    info = conn.recv(BUFFER_SIZE).decode(FORMAT)
    input_ext, output_ext, filesize = info.split(SEPARATOR)
    #Generate a random name for the temporal files
    rd_name = uuid.uuid1().hex
    os.makedirs(rd_name)

    input_file = f"{rd_name}/{rd_name}{input_ext}"
    output_file = f"{rd_name}/{rd_name}{output_ext}"
    filesize = int(filesize)
    print(f"[CONN with {addr}]Receiving file of {filesize} bytes.")
    #Receive the data of the file
    with open(input_file, "wb") as f:
        received_data = 0
        while received_data < filesize:
            bytes_read = conn.recv(BUFFER_SIZE)
            # write to the file the bytes we just received
            f.write(bytes_read)
            received_data += len(bytes_read)
        f.close()
    print(f"[CONN with {addr}]File transfer done, init conversion.")
    try:
        #Exe file conversion
        ffmpeg.input(input_file).output(output_file).run(capture_stdout= False,capture_stderr=True, overwrite_output=True)
        print(f"[CONN with {addr}]Conversion done, init file transfer.")
        #Get info of converted file and send it to client
        filesize = os.path.getsize(output_file)
        conn.send(f"True{SEPARATOR}{filesize}".encode(FORMAT))
        #Send file in chunk of buffer size
        with open(output_file, "rb") as f:
            bytes_read = f.read(BUFFER_SIZE)
            while bytes_read: 
                conn.sendall(bytes_read)
                bytes_read = f.read(BUFFER_SIZE)
            f.close()
    except Exception as e:
        print(f"[CONN with {addr}]Error in the conversion process.")
        conn.send(f"False{SEPARATOR}Error in the conversion process".encode(FORMAT))
    finally:   
        #Close connection to client and remove temporal files
        conn.close()
        shutil.rmtree(f"./{rd_name}")
        print(f"[CONN with {addr}]Folder was deleted and conn closed.")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=receive_file, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def main():
    print("[STARTING] Server is starting...")
    start()

main()