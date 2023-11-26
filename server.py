import socket
import threading
import sys

# Global dictionary to hold client connections (username: socket)
clients = {}

client_is_connected = True
# Function to initialize the server socket
def initialize_server(port):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the server address and port
    server_socket.bind(('', port))
    # Enable the server to accept connections, with a backlog of 10 clients
    server_socket.listen(10)
    return server_socket


# Function to handle each client connection
def client_handler(client_socket, cli_address):
    username = ''
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Split the message into command and arguments
            message_split = message.split()
            command = message_split[0]
            args = message_split[1:-1]
            username = message_split[-1]
            # Handle JOIN command
            if command == "JOIN":
                # Check if username already exists or if client limit is reached
                if username in clients:
                    client_socket.send("JOIN Error:Username taken".encode())
                    break
                
                if len(clients) >= 10:
                    client_socket.send("JOIN Error:Too Many Users".encode())
                    break

                # Report back to the client they've successfully been added
                # client_socket.send("JOIN Success:Connected to server!".encode())

                # Add the client to the clients dictionary
                clients[username] = client_socket
                print("Connected with",cli_address)
                print(f"{username} Joined the Chatroom")

                # Broadcast join message to other clients
                broadcast(f"{username} joined!")
                continue

            # Handle LIST command
            elif command == "LIST":
                # Send a list of all connected clients to the requester
                client_list = ",".join(clients.keys())
                client_socket.send(f"{client_list}".encode())
                continue

            # Handle MESG command
            elif command == "MESG":
                # Make sure the correct number of args has been passed
                if len(args) < 2:
                    client_socket.send(f"MESG Error: No Message".encode())
                    break

                # parse user and message
                target_user, user_message = args[0], " ".join(args[1:])
                print(user_message)
                print(" ".join(args[1:]))

                # Check if the target user exists and send them the message
                if target_user in clients:
                    clients[target_user].send(f"{username}: {user_message}".encode())
                    client_socket.send("".encode())
                    continue

            # Handle BCST command
            elif command == "BCST":
                broadcast_message = " ".join(args)
                # Broadcast the message to all clients except the sender
                client_socket.send(f"{username} is sending a broadcast".encode())
                broadcast(f"{username}: {broadcast_message}")
                continue

            # Handle QUIT command
            elif command == "QUIT":
                if username:
                    client_socket.send(f"{username} is quitting the server".encode())
                    del clients[username]
                    broadcast(f"{username} left")
                continue

            # Handle unknown commands
            else:
                client_socket.send("Unknown Message".encode())
                continue

        except Exception as e:
            print(f"Error: {e}")
            continue

# Broadcast message to all clients
def broadcast(message):
    for username, client_socket in clients.items():
        client_socket.send(message.encode())

# Main function to start the server
def main():
    if(len(sys.argv) != 2):
        print("usage: python3 server.py <svr_port>")
        return
    port = int(sys.argv[1])

    server_socket = initialize_server(port)
    print("The Chat Server Started")

    # Accept new connections indefinitely
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            # Start a new thread to handle each client
            threading.Thread(target=client_handler, args=(client_socket, client_address)).start()
    except KeyboardInterrupt:
        server_socket.close()
        return 1
    

# Check if the script is the main program and execute it
if __name__ == "__main__":
    main()