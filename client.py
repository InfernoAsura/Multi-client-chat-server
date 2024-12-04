# The tkinter library is used to create the GUI for the chatbox. The host is the current network on which the server
# is running. First, the client connect with the server using the join button, which ultimately calls the connect
# function. Then it creates a thread to listen for any message that the server sends and react accordingly. using the 
# send_file function, we can send files and using the join and create chatroom functions, we can join and create
# chatrooms.



import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

HOST = '172.31.36.136'
PORT = 1234

DARK_GREY = '#1E1E1E'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message == 'exit':
        client.sendall(message.encode())
        exit(0)
    elif message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "rb") as file:
            file_data = file.read()
        client.sendall(b"FILE" + file_data)


def create_chatroom():
    room_name = message_textbox.get()
    client.sendall(f"CREATE_ROOM~{room_name}".encode())
    message_textbox.delete(0, len(room_name))

def join_chatroom():
    room_name = message_textbox.get()
    client.sendall(f"JOIN_ROOM~{room_name}".encode())
    message_textbox.delete(0, len(room_name))

root = tk.Tk()
root.geometry("650x600")
root.title("Messenger Client")
root.resizable(False, False)

root.pack_propagate(0)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=650, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=650, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=650, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE,insertbackground="white" , width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE,insertbackground="white" , width=25)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)


file_button = tk.Button(bottom_frame, text="📂", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_file)
file_button.pack(side=tk.LEFT, padx=10)

create_button = tk.Button(bottom_frame, text="Create", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=create_chatroom)
create_button.pack(side=tk.LEFT, padx=10)

join_button = tk.Button(bottom_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=join_chatroom)
join_button.pack(side=tk.LEFT, padx=10)


message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_messages_from_server(client):
    pq = 0
    while True:
        message = client.recv(2048).decode('utf-8')
        if message.startswith("ERROR"):
            trash, mess = message.split("~")
            messagebox.showerror("Error", mess)
        elif message.startswith("FILE"):
            file_name = f"file_{pq}.txt"
            pq += 1
            with open(file_name, "wb") as file:
                file.write(message[4:].encode())
        elif message == "exit":
            client.close()
            exit(0)
        elif message:
            username, content = message.split("~")
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
