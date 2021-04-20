import socket
import os
import tqdm

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send_file(filepath):
    # Send filesize in bytes if the desired file
    filesize = os.path.getsize(filepath)
    print(filesize)
    encoded_size = f"{}".encode(FORMAT)
    client.send(encoded_size)
    # Send file to server
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(filepath, "rb") as f:
        bytes_read = f.read(BUFFER_SIZE)
        while bytes_read: 
            client.sendall(bytes_read)
            progress.update(len(bytes_read))
            bytes_read = f.read(BUFFER_SIZE)
        client.close()
        
def can_convert(og_ext, to_ext):
    if og_ext == to_ext:
        print("The conversion extension is the same as the one in the specified file. No conversion to be made")
        return False
    #exts = None
    #if og_ext in video_exts:
    #    exts = video_exts
    #elif og_ext in audio_exts:
    #    exts = audio_exts
    #else:
    if og_ext not in video_exts and og_ext not in audio_exts:
        print(f"The file extension {og_ext} of the input file is not supported")
        return False
    
    if to_ext not in video_exts and to_ext not in audio_exts:
        print(f"The file extension {to_ext} of the output file is not supported")
        return False
    
    #if to_ext not in exts:
    #    print(f"Conversion from {og_ext} to {to_ext} is not supported!!!")
    #    return False
    return (True)
"""
def send_file_quick(filepath):
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(filepath, "rb") as f:
        client.sendfile(f, 0)
"""

filename = "sources.txt"


send_file(filename)

#send(DISCONNECT_MESSAGE)