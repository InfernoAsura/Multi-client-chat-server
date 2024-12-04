# Multi-client-chat-server
Features: 
1. Chatting platform :- Multiple users can connect to the server from different devices and chat with each other. Currently, the limit of users is 5. Also the user had to add the ipv4 address of the network which the server and the user will use to connect.
2. File transferring :- Files can be transferred between users. The current size limit of files which can be transferred is 2KB but it can be changed. We have used csv and text files for transferring.
3. Chatrooms :- Users initially joins the "general" chatroom. Then, the user can create his/her own chatroom or maybe join somebody else's chatroom. The user needs to have the name of the chatroom to join or create a chatroom. Every chatroom has a unique name.

## How to run the code:
1. Run the server.py file.
2. Run the client.py file.
3. A window(messenger client) will pop up.
4. Enter the username and click on the join button to connect to the server. 
5. Now, type in the message textbox and click on the send button to send the message. 
6. To transfer a file, click the file icon, near the send button, and a pop-up of file explorer will appear. Choose the file that needs to be transferred and open it. The file will appear in the same folder in which the client.py file exists in txt format.
7. To create a chatroom, write the chatroom name, and click on the create. If the chatroom name is already taken, then an error message will occur, otherwise the chatroom will be created and you will leave the current chatroom and enter into the new chatroom. 
8. To join a chatroom, write the chatroom name which you want to join and click on the join button. If no such chatroom exists, then an error message will appear. Otherwise, you will join the chatroom.
9. The messages in an individual chatroom can only be read by the people present in that chatroom. 

## Note
Make sure that in the client.py file, you put the ipv4 address of the wifi(network) the server is running on in host.
