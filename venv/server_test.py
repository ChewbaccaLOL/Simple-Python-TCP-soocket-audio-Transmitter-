# from socket import *
#
# serverPort = 5005
# bufferSize = 1024
#
# serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.bind(('', serverPort))
# print('The server is ready to recieve')
#
# while True:
#     message, clientAddress = serverSocket.recvfrom(1024)
#     print("Message received from client: ", message)
#     serverSocket.sendto(message, clientAddress)

import socket
import pyaudio
import threading
import os
os.system('cls')

# Socket
host = socket.gethostbyname(socket.gethostname())
# host = "127.0.0.1"
port = 8080
buffer = 2048
clients = []

# Audio
audio = pyaudio.PyAudio()
chunk = int(1024 * 4)


def client_listener():
    while True:
        buffer = 2048
        data, address = host_socket.recvfrom(buffer)
        if address not in clients:
            print(f'New client: {address[0]}:{address[1]}')
            clients.append(address)
            print(clients)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host_socket:
    try:
        host_socket.bind((host, port))
        print(f'Server hosted at {host}:{port}\n')

        print('Starting listener thread...')
        listener_thread = threading.Thread(target=client_listener)
        listener_thread.daemon = True
        listener_thread.start()
        print('Listener thread started!')

        print('Initiating microphone...')
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=chunk)

        print('Recording!')
        while True:
            voice_data = stream.read(chunk, exception_on_overflow=False)
            for client in clients:
                host_socket.sendto(voice_data, client)
    except socket.error as error:
        print(str(error))
        stream.close()
        host_socket.close()
    except KeyboardInterrupt:
        stream.close()
        host_socket.close()
        print('Key pressed!')
    finally:
        stream.close()
        host_socket.close()