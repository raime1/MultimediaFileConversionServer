import socket
import os
import tqdm
import argparse

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

video_exts = [".avi", ".gif", ".mov", ".mp4", ".rawvideo", ".webm"]
audio_exts = [".aac",".ac3", ".flac", ".mp3", ".wav"]



def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send_file(input_file, output_file):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    # Send filesize in bytes if the desired file
    filesize = os.path.getsize(input_file)
    input_name, input_ext = os.path.splitext(input_file)
    output_name,  output_ext = os.path.splitext(output_file)

    if not can_convert(input_ext, output_ext):
        return
    
    encoded_info = f"{input_ext}{SEPARATOR}{output_ext}{SEPARATOR}{filesize}".encode(FORMAT)
    client.send(encoded_info)
    # Send file to server
    progress = tqdm.tqdm(range(filesize), f"Sending {input_file}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(input_file, "rb") as f:
        bytes_read = f.read(BUFFER_SIZE)
        while bytes_read: 
            client.sendall(bytes_read)
            progress.update(len(bytes_read))
            bytes_read = f.read(BUFFER_SIZE)
        f.close()
    
    print("Waiting for convertion...")
    response = client.recv(BUFFER_SIZE).decode(FORMAT)
    print(response)
    success, info = response.split(SEPARATOR)
    success = bool(success)
    if success:
        filesize = int(info)
        progressR = tqdm.tqdm(range(filesize), f"Receiving {output_file}", unit = "B", unit_scale = True, unit_divisor = 1024)
        with open(output_file, "wb") as f:
            received_data = 0
            while received_data < filesize:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                received_data += len(bytes_read)
                progressR.update(len(bytes_read))
            print("File transfer done...")
            f.close()
    else:
        print("Error ocurred in the conversion")

    if not client._closed:
        client.close()
    


    
        
def can_convert(og_ext, to_ext):
    if og_ext == to_ext:
        print("The conversion extension is the same as the one in the specified file. No conversion to be made")
        return False

    if og_ext not in video_exts and og_ext not in audio_exts:
        print(f"The file extension {og_ext} of the input file is not supported")
        return False
    
    if to_ext not in video_exts and to_ext not in audio_exts:
        print(f"The file extension {to_ext} of the output file is not supported")
        return False

    return (True)
"""
def send_file_quick(filepath):
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit = "B", unit_scale = True, unit_divisor = 1024)
    with open(filepath, "rb") as f:
        client.sendfile(f, 0)
"""

filename = "test2.webm"

parser = argparse.ArgumentParser()
parser.add_argument("ip_server", help="IP Address of the server that is going to permform the multimedia file conversion")
parser.add_argument("input_file", help="File that tou want to convert")
parser.add_argument("output_file", help="Two posible options:"
                    +"\ \n- path/of/file.extension: File to save the result and the extension to conver the original file"
                    +"\ \n- .extension: extension to convert the file, the new file will be in the same directory and have the same name of the original file")
args = parser.parse_args()

SERVER = args.ip_server
ADDR = (SERVER, PORT)

send_file(args.input_file, args.output_file)
