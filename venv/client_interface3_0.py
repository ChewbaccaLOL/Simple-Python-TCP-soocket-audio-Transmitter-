
import threading
import socket
import pyaudio
import os
import tkinter as tk



def on_closing():
    stream.close()
    client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
    client_socket.close()
    root.destroy()

def disconnect_btn(b):
    stream.close()
    client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
    client_socket.close()
    b.destroy()


def listen_audio():
    # Socket
    # host = "127.0.0.1"
    # host = socket.gethostbyname(socket.gethostname())

    # port = 8080

    os.system('cls')

    # Audio
    audio = pyaudio.PyAudio()
    globals()['audio']=audio
    chunk = int(1024 * 4)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        globals()['client_socket']=client_socket
        try:

            client_socket.sendto('Hi!'.encode('utf-8'), (host, port))

            stream = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                output=True,
                                frames_per_buffer=chunk)
            globals()['stream'] = stream
            connect_btn = tk.Button(text="Disconnect", background="#555", foreground="#ccc",
                                    activebackground="#567",
                                    padx="15", pady="6", font="15", command=lambda: disconnect_btn(connect_btn))
            connect_btn.place(x=50, y=190, height=30, width=270, bordermode=tk.OUTSIDE)
            while True:
                voice_data = client_socket.recvfrom(chunk * 2)
                print('received chunk')
                print(voice_data)
                stream.write(voice_data[0])
        except socket.error as error:
            print(str(error))
            
            stream.close()
            client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
            client_socket.close()
        except KeyboardInterrupt:
            stream.close()
            client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
            client_socket.close()
            print('Key pressed!')
        

        finally:
            stream.close()
            client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
            client_socket.close()


def lst_cont():
    prcss_thread = threading.Thread(target=listen_audio)
    prcss_thread.start()


def main():
    root = tk.Tk()
    globals()['root'] = root
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
                            padx="15", pady="6", font="15", command=lambda: lst_cont())
    connect_btn.place(x=50, y=100, height=70, width=270, bordermode=tk.OUTSIDE)
    root.resizable(width=False, height=False)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.config(bg='#888')
    root.mainloop()


if __name__ == "__main__":
    main()
# if stream.is_active():
#     stream.close()
# if client_socket:
#     client_socket.sendto('Bye!'.encode('utf-8'), (host, port))
#     client_socket.close()