# Usage: python3 client.py <server-name> <port>

from socket import *
import sys

# "JOIN" command to join the chatroom
def send_join_request(server_name, server_port, username):
    print("join")

# "LIST" command to list all the users in the chatroom
def send_list_request(server_name, server_port):
    print("list")   

# "MESG" command to send a message to a specific user
def send_message_request(server_name, server_port):
    print("message")

# "BCST" command to broadcast a message to all the users in the chatroom
def send_broadcast_request(server_name, server_port):
    print("broadcast")

# "QUIT" command to quit the chatroom
def send_quit_request(server_name, server_port):
    print("quit")


def main():
    if (len(sys.argv) != 3):
        print("Usage: python client.py <server-name> <port>")
        sys.exit(1)
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    # TCP socket
    cli_socket = socket(AF_INET, SOCK_STREAM)
    cli_socket.connect((server_name, server_port))

    is_client_connected = True
    while is_client_connected:
        userCommand = input("")
        # TODO: handle other inputs for each command
        if userCommand == "JOIN":
            username = input("Enter your username: ")
            send_join_request(server_name, server_port, username)
        elif userCommand == "LIST":
            send_list_request(server_name, server_port)
        elif userCommand == "MESG":
            send_message_request(server_name, server_port)
        elif userCommand == "BCST":
            send_broadcast_request(server_name, server_port)
        elif userCommand == "QUIT":
            send_quit_request(server_name, server_port)
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()