# Usage: python3 client.py <server-name> <port>

from socket import *
import sys

# "JOIN" command to join the chatroom
def send_join_request(cli_socket: socket, server_name, server_port, username):
    message = "JOIN " + username
    cli_socket.sendto(message.encode(), (server_name, server_port))

# "LIST" command to list all the users in the chatroom
def send_list_request(cli_socket: socket, server_name, server_port):
    cli_socket.sendto("LIST".encode(), (server_name, server_port))

# "MESG" command to send a message to a specific user
def send_message_request(cli_socket: socket, server_name, server_port, message_target, message_contents):
    
    
    cli_socket.sendto("MESG".encode(), (server_name, server_port))

# "BCST" command to broadcast a message to all the users in the chatroom
def send_broadcast_request(cli_socket: socket, server_name, server_port):
    cli_socket.sendto("BCST".encode(), (server_name, server_port))

# "QUIT" command to quit the chatroom
def send_quit_request(cli_socket: socket, server_name, server_port):
    cli_socket.sendto("QUIT".encode(), (server_name, server_port))

# checks if a string consists of only letters and numbers
def is_alphanumeric(string: str):
    for c in string:
        if not ((c.upper() >= 'A' and c.upper() < 'Z') or (c >= '0' and c <= '9')):
            return False
    return True


def main():
    if (len(sys.argv) != 3):
        print("Usage: python client.py <server-name> <port>")
        sys.exit(1)
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    # TCP socket
    cli_socket = socket(AF_INET, SOCK_STREAM)

    #Try to connect and make sure the connection worked
    try:
        cli_socket.connect((server_name, server_port))
    except:
        print("Connection failed!")
        sys.exit(1)

    #Prompt user to send JOIN command with their user name
    join_command_is_valid = False
    while not join_command_is_valid:
        join_command = input("Enter JOIN followed by your username: ")
        join_args = join_command.split(' ')

        if len(join_args != 2): continue
        if len(join_args[1] < 1): continue
        if not is_alphanumeric(join_args[1]): continue
        if join_args[0] != "JOIN": continue
        
        join_command_is_valid = True

        # Not sure if this ^ is more legible than that v
        # join_command_is_valid = len(join_args) == 2 and len(join_args[1] > 0) and is_alphanumeric(join_args[1]) and join_args[0] == "JOIN"
    

    is_client_connected = True
    while is_client_connected:
        userCommand = input(":")
        commandArgs = userCommand.split(' ')

        # TODO: handle other inputs for each command
        if commandArgs[0] == "JOIN":
            username = input("Enter your username: ")
            send_join_request(cli_socket, server_name, server_port, username)
        elif userCommand == "LIST":
            send_list_request(cli_socket, server_name, server_port)
        elif userCommand == "MESG":
            send_message_request(cli_socket, server_name, server_port)
        elif userCommand == "BCST":
            send_broadcast_request(cli_socket, server_name, server_port)
        elif userCommand == "QUIT":
            send_quit_request(cli_socket, server_name, server_port)
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()