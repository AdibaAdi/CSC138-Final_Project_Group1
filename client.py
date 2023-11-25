# Usage: python3 client.py <server-name> <port>

from socket import *
import sys

#TCP socket
cli_socket = socket(AF_INET, SOCK_STREAM)   
server_name = ''
server_port = 0
client_is_connected = False

# send a message to the server then wait to receive the response
def send_and_receive(message:str):
    try:
        cli_socket.sendto(message.encode(),(server_name, server_port))
        return cli_socket.recv(1024).decode()
    except:
        return ''

# checks if a string consists of only letters and numbers
def is_alphanumeric(string: str):
    for c in string:
        if not ((c.upper() >= 'A' and c.upper() < 'Z') or (c >= '0' and c <= '9')):
            return False
    return True

# process response messages from the server
def process_server_response(message):
    pass

def main():
    if (len(sys.argv) != 3):
        print("Usage: python client.py <server-name> <port>")
        sys.exit(1)
    server_name = sys.argv[1]
    server_port = int(sys.argv[2])

    #Try to connect and make sure the connection worked
    try:
        cli_socket.connect((server_name, server_port))
    except:
        print("Connection failed!")
        sys.exit(1)

    #TODO: retool this with new paradigm
    #Prompt user to send JOIN command with their user name
    join_command_is_valid = False
    while not join_command_is_valid:
        join_command = input("Enter JOIN followed by your username: ")
        join_args = join_command.split()

        # if the user's input is invalid in any way, continue to prompt for valid input
        if len(join_args) != 2: continue
        if len(join_args[1]) < 1: continue
        if not is_alphanumeric(join_args[1]): continue
        if join_args[0] != "JOIN": continue
        
        join_command_is_valid = True
    
    #Send the JOIN request
    server_response = send_and_receive(join_command)

    
    while client_is_connected:
        userCommand = input(":")
        process_server_response(send_and_receive(userCommand))

    cli_socket.close()
    return 0


if __name__ == "__main__":
    main()