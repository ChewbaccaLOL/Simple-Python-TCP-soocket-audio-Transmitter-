
import threading
import socket
import pyaudio
import os
import tkinter as tk


# disconnect function
def dscn():
    try:
        stream.close()
    except:
        pass
    try:
        client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
        client_socket.close()
    except:
        pass


# hancle closing windoow
def on_closing():
    dscn()
    root.destroy()


# handle the button
def disconnect_btn(b):
    dscn()
    b.destroy()

# handling sound recieve
def listen_audio():
    # Socket
    # host = "127.0.0.1"
    # host = socket.gethostbyname(socket.gethostname())

    # port = 8080

    os.system('cls')

    # Audio
    audio = pyaudio.PyAudio()  # pyaudio that can interpret chunks of bits of sound and play them
    globals()['audio']=audio
    chunk = int(1024 * 4) # Setting chunk to 4k bits

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        globals()['client_socket']=client_socket # setting the socket and setting it in globals to close it on disconnection
        try: # trying to listen

            client_socket.sendto('Hi!'.encode('utf-8'), (host, port)) # when connecting, giving a short message to connect to server

            # start to play audio from server
            stream = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                output=True,
                                frames_per_buffer=chunk)
            globals()['stream'] = stream #setting stream to globals to close it on exit
            # handling the disconnection button
            connect_btn = tk.Button(text="Disconnect", background="#555", foreground="#ccc",
                                    activebackground="#567",
                                    padx="15", pady="6", font="15", command=lambda: disconnect_btn(connect_btn))
            connect_btn.place(x=50, y=190, height=30, width=270, bordermode=tk.OUTSIDE)
            # recieving chunks of audio and passing it to audio stream
            while True:
                voice_data = client_socket.recvfrom(chunk * 2)
                print('received chunk')
                print(voice_data)
                if stream.is_active():
                    stream.write(voice_data[0])
        # handling exceptions
        except socket.error as error:
            print(str(error))

            dscn()
        except KeyboardInterrupt:
            dscn()
            print('Key pressed!')
        

        finally:
            dscn()

# running a separate thread for listening audio function
def lst_cont():
    prcss_thread = threading.Thread(target=listen_audio)
    prcss_thread.start()


def main():
    root = tk.Tk()
    globals()['root'] = root # setting root to globals, to accept it any time (for handling closing and stuff)
    # properties of window
    root.title("Audio translation listener")
    root.geometry("400x250-300-200")

    # IP selection
    IPlabel = tk.Label(text="Enter IP:", bg='#888')
    IPlabel.config(font=("Arial_helvetica 12"))
    IPlabel.place(x=50, y=50)

    IP_var = tk.StringVar()
    IP_var.set('192.168.1.105')

    IP_var_box = tk.Entry(textvariable=IP_var, font=("Arial_helvetica 12"), bg="#AAA")
    IP_var_box.place(x=120, y=50, width=108)

    # Port selection
    PortLabel = tk.Label(text="Port:", bg='#888')
    PortLabel.config(font=("Arial_helvetica 12"))
    PortLabel.place(x=240, y=50)

    Port_Var = tk.IntVar()
    Port_Var.set(8080)

    Port_Var_box = tk.Entry(textvariable=Port_Var, font=("Arial_helvetica 12"), bg="#AAA")
    Port_Var_box.place(x=280, y=50, width=40)

    # connection button
    globals()['host'] = IP_var.get()
    globals()['port'] = Port_Var.get()
    connect_btn = tk.Button(text="Connect to the audio channel", background="#555", foreground="#ccc",
                            activebackground="#567",
                            padx="15", pady="6", font="15", command=lambda: lst_cont()) # lambda calls listener
    connect_btn.place(x=50, y=100, height=70, width=270, bordermode=tk.OUTSIDE)
    root.resizable(width=False, height=False)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.config(bg='#888')
    root.mainloop()


if __name__ == "__main__":
    main()
