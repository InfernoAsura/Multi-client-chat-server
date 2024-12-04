# In this file, the server first creates a general chatroom and binds itself to the host and port. Then, it listens for 
# connections and once found, creates a handshake connection with it. Then it creates a thread for each client (connection)
# and enters the client handler function, where it waits for the username to write his/her username and then it creates another 
# thread for listening to that client's messages. In the listen_for_messages function, it listens for the message sent by 
# client and acts accordingly. The chatroom class is responsible for managing different chatrooms. It is used to create 
# a chatroom and then add or remove client from that chatroom. Create_chatroom function is used to create a chatroom, 
# join_chatroom is used to join and leave_chatroom is used to leave the chatroom. The message is send to client using
# send_message_to_client function.
# The host is 0.0.0.0 which allows it to establish connection with any other device which is connected to the same network
# and same port. The listener limit is 5 which means only 5 people can join the server at a single time.


import socket
import threading

HOST = '0.0.0.0'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []
chatrooms = {}

class Chatroom:
    def __init__(self, name):
        self.name = name
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

def create_chatroom(name):
    if name in chatrooms:
        return False
    else:
        chatroom = Chatroom(name)
        chatrooms[name] = chatroom
        return True

def join_chatroom(client, room_name):
    if room_name in chatrooms:
        chatroom = chatrooms[room_name]
        chatroom.add_client(client)
        return True
    else:
        return False

def leave_chatroom(client, room_name):
    if room_name in chatrooms:
        chatroom = chatrooms[room_name]
        chatroom.remove_client(client)
        return True
    else:
        return False

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_messages_to_all(message, room_name):
    if room_name in chatrooms:
        chatroom = chatrooms[room_name]
        for client in chatroom.clients:
            send_message_to_client(client, message)

def listen_for_messages(client, username,address, room_name):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            if message.startswith("CREATE_ROOM"):
                trash, name = message.split("~")
                if create_chatroom(name) == False:
                    send_message_to_client(client, "ERROR~" + "Chatroom already exists")
                else:
                    leave_chatroom(client, room_name)
                    send_messages_to_all("SERVER~" + f"{username} left the chatroom {room_name}", room_name)
                    room_name = name
                    join_chatroom(client, room_name)
                    prompt_message = "SERVER~" + f"{username} created the chatroom {room_name}"
                    send_messages_to_all(prompt_message, room_name)
            elif message.startswith("JOIN_ROOM"):
                trash, name = message.split("~")
                if join_chatroom(client, name) ==False:
                    send_message_to_client(client, "ERROR~" + "Chatroom does not exist")
                else:
                    leave_chatroom(client, room_name)
                    send_messages_to_all("SERVER~" + f"{username} left the chatroom {room_name}", room_name)
                    room_name = name
                    prompt_message = "SERVER~" + f"{username} joined the chatroom {room_name}"
                    send_messages_to_all(prompt_message, room_name)
            elif message.startswith("FILE"):
                file_data = message[4:].encode()
                receive_file(username, file_data, room_name)
            elif message.startswith("exit"):
                active_clients.remove((username, client))
                leave_chatroom(client, room_name)
                print(f"Successfully disconnected to client {address[0]},{address[1]}")
                send_messages_to_all("SERVER~" + f"{username} left the server",room_name)
                client.sendall("exit".encode())
                client.close()
                break
            else:
                final_msg = username + '~' + message
                send_messages_to_all(final_msg, room_name)
        else:
            print(f"The message sent from client {username} is empty")

def receive_file(username, file_data, roomname):
    file_name = f"FILE_{username}.txt"
    fn = b"FILE" + file_data  
    message = f"SERVER~ {username} uploaded a file: {file_name}"
    send_messages_to_all(message, roomname)
    if roomname in chatrooms:
        chatroom = chatrooms[roomname]
        for client in chatroom.clients:
            client.sendall(fn)

def client_handler(client, address):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message, "general")
            break
        else:
            print("Client username is empty")
    
    join_chatroom(client, "general")
    threading.Thread(target=listen_for_messages, args=(client, username,address, "general", )).start()

def main():
    create_chatroom("general")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client, address, )).start()

if __name__ == '__main__':
    main()
