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
chunk = int(1024 * 4) # setting chunk to 4K

# client listener accepts messages for strating translation to a new device
def client_listener():
    while True:
        
        buffer = 2048 # buffer for message
        data, address = host_socket.recvfrom(buffer)
        if address not in clients and data == 'Hi!'.encode('utf-8'): # if message is Hi! and client isn't connected, we're connecting it
            print(f'New client: {address[0]}:{address[1]}') # adding new client and showing IP/port
            clients.append(address)
            print('Active clients: ',clients) # showing all active cients
        elif  data == 'Bye!'.encode('utf-8'): # if message is Bye!, disconnecting the client
            print(f'This client has quitted: {address[0]}:{address[1]}') # displaying disconnected client
            
            clients.remove(address)
            print('Active clients: ',clients)




with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as host_socket:
    try:
        host_socket.bind((host, port)) # starting socket
        print(f'Server hosted at {host}:{port}\n')

        print('Starting listener thread...')
        listener_thread = threading.Thread(target=client_listener) # starting a thread for client listener
        listener_thread.daemon = True # starting daemon thread, to shut it as shutting the server and also it is a background process
        listener_thread.start()
        print('Listener thread started!')

        print('Initiating microphone...')
        # starting audio listener
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=chunk)

        print('Recording!')
        while True:
            voice_data = stream.read(chunk, exception_on_overflow=False) # reading audio from microphone
            for client in clients: # sending audiio chunk to all clients
                # print(client)
                host_socket.sendto(voice_data, client)
    # handling exceptions
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