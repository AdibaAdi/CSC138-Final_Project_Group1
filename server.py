import sys
import socket
import threading

# Global dictionary to hold client connections (username: socket)
clients = {}

client_is_connected = True
# Function to initialize the server socket
def initialize_server():
    if len(sys.argv) != 2:
        print("usage: python3 server.py <svr_port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set the SO_REUSEADDR option on the socket to reuse the socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind(('', port))
    server_socket.listen(10)
    return server_socket

# checks if a string consists of only letters and numbers
def is_alphanumeric(string: str):
    for c in string:
        if not ((c.upper() >= 'A' and c.upper() < 'Z') or (c >= '0' and c <= '9')):
            return False
    return True

# Function to handle each client connection
def client_handler(client_socket, client_address):
    username = None
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"Connected with {client_address}")

            # Split the message into command and arguments
            command, *args = message.split()

            # Handle JOIN command
            if command == "JOIN":
                # Make sure the appropriate number of arguments were provided
                if len(args) != 1 or not is_alphanumeric(args[0]):
                    client_socket.send("JOIN Error:Bad Username".encode())
                    break

                username = args[0]
                # Check if username already exists or if client limit is reached
                if username in clients:
                    client_socket.send("JOIN Error:Username taken".encode())
                    break
                
                if len(clients) >= 10:
                    client_socket.send("JOIN Error:Too Many Users".encode())
                    break
                
                # Add the client to the clients dictionary
                clients[username] = client_socket


                # Broadcast join message to other clients
                broadcast(f"{username} Joined the Chatroom!", username)

                # Report back to the client they've successfully been added
                client_socket.send("JOIN Success:Connected to server!".encode())

            # Handle LIST command
            elif command == "LIST":
                # Send a list of all connected clients to the requester
                client_list = "\n".join(clients.keys())
                client_socket.send(f"LIST Success:{client_list}".encode())

            # Handle MESG command
            elif command == "MESG":
                # Make sure the correct number of args has been passed
                if len(args) < 2:
                    client_socket.send(f"MESG Error: No Message".encode())
                    continue

                # parse user and message 
                target_user, user_message = args[0], " ".join(args[1:])

                # Check if the target user exists and send them the message
                if target_user in clients:
                    clients[target_user].send(f"{username} (private): {user_message}".encode())
                    client_socket.send(f"MESG Success: Message sent.")
                    continue
                else:
                    client_socket.send(f"MESG Error: User {target_user} not found".encode())
                    continue

            # Handle BCST command
            elif command == "BCST":
                broadcast_message = " ".join(args)
                # Broadcast the message to all clients except the sender
                broadcast(f"{username}: {broadcast_message}", username)
                client_socket.send(f"BCST Success: Message Broadcast".encode())
            

            # Handle QUIT command
            elif command == "QUIT":
                break

            # Handle unknown commands
            else:
                client_socket.send("Unknown command".encode())

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the client from the list and close the connection
    if username:
        client_socket.close()
        del clients[username]
        # Broadcast a message informing others of the client's departure
        broadcast(f"{username} Left the Chatroom!", username)

# Function to broadcast a message to all clients
def broadcast(message, sender=None):
    message_to_send = message if sender is None else f"{sender}: {message}"
    for username, client_socket in clients.items():
        if username != sender:
            try:
                client_socket.send(message_to_send.encode())
            except Exception as e:
                print(f"Broadcast to {username} failed: {e}")


# Main function to start the server
def main():
    server_socket = initialize_server()
    print(f"Server started on port {sys.argv[1]}")
    
    # Accept new connections indefinitely
    while True:
        client_socket, client_address = server_socket.accept()

        # Print the connected client's address - This is the correct location
        print(f"Connected with {client_address}")

        # Start a new thread to handle each client
        threading.Thread(target=client_handler, args=(client_socket, client_address)).start()
# Check if the script is the main program and execute it
if __name__ == "__main__":
    main()
