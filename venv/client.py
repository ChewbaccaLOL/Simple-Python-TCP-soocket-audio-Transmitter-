# from socket import *
# 
# serverIP = "127.0.0.1"
# serverPort = 5005
# bufferSize = 1024
# message = b"Hello, World!"
# 
# print("UDP server IP address: ",serverIP)
# print("UDP server port number: ", serverPort)
# print("Message to be sent to server:", message)
# 
# clientSocket = socket(AF_INET, SOCK_DGRAM)
# clientSocket.sendto(message, (serverIP, serverPort))
# recvMessage, serverAddress = clientSocket.recvfrom(bufferSize)
# print("Message received from server: ", recvMessage)
# clientSocket.close()

import socket
import pyaudio
import os

# Socket
# host = "127.0.0.1"

host = socket.gethostbyname(socket.gethostname())

port = 8080

os.system('cls')

# Audio
audio = pyaudio.PyAudio()
chunk = int(1024 * 4)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    try:

        client_socket.sendto(' '.encode('utf-8'), (host, port))

        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            output=True,
                            frames_per_buffer=chunk)

        while True:
            voice_data = client_socket.recvfrom(chunk*2)
            print('received chunk')
            print(voice_data)
            stream.write(voice_data[0])
    except socket.error as error:
        print(str(error))
        stream.close()
        client_socket.close()
    except KeyboardInterrupt:
        stream.close()
        client_socket.close()
        print('Key pressed!')

    finally:
        stream.close()
        client_socket.close()