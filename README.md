# Multimedia File Conversion Server and Client

**Instituto Tecnológico de Costa Rica**

**Curso de Redes**

**Tarea: Capa de redes**

Multimedia file conversion server and client app using **FFmpeg, python and sockets**. The server side can run locally on a LAN network, or either is ready to be dockerized. 

For more information on how to use client side use command -h/--help.

## Server side

The server client "server.py" is the one in charge to run continously as a server listening for new connections, receive the files and make the format conversion and then delete the input files and return the output file as the new format. Server side also verifies the format desored to make sure you are not changing the file to it's same format.

Execution command: python3 server.py

## Client side

The client file "client.py" receives multiple params, for it's main execution use the following order.
Call the script
  - server client IP address
  - input file with file extension
  - output file with file extension

The input fill will be uploaded to the server, then the server will send the output file to the client device when the convertion is done.

Execution command: python3 client.py serverIP inputFile outputFile

Example: python3 client.py 35.222.70.179 myVideo.mp4 myVideo.webm

That's for changing a video in mp4 to a webm format.

### Authors

By Danilo Chaves, Leonardo Lizano, Kevin Solano.
