# Usage: python3 client.py <server-name> <port>

from socket import *
import sys
import threading

#TCP socket
cli_socket = socket(AF_INET, SOCK_STREAM)   
server_name = ''
server_port = 0
client_is_connected = False

# Function to check if a string is alphanumeric
def is_alphanumeric(string: str):
    return string.isalnum()

# send a message to the server then wait to receive the response
def handle_send(message:str):
    try:
        cli_socket.sendto(message.encode(),(server_name, server_port))
    except:
        return

def handle_user_input(username):
    try:
        while client_is_connected:
            userCommand = input("")
            if (userCommand):
                # Send user command along with user message
                handle_send(userCommand + ' ' + username)
    except KeyboardInterrupt:
        cli_socket.close()
        sys.exit(1)

def handle_broadcasts():
    global client_is_connected
    while client_is_connected:
        try:
            message = cli_socket.recv(1024).decode()
            print(message)
            # Close client after quit message is processed
            if message.__contains__("quitting"):
                client_is_connected = False
                cli_socket.close()
                sys.exit(1)
        except:
            break

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

    try:
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
        global client_is_connected
        client_is_connected = True
        threading.Thread(target=handle_broadcasts).start()
        #Send the JOIN request
        handle_send(join_command)
        print("Connected to server!")
        username = join_args[1]
        #Process the server's response
        if client_is_connected:
            threading.Thread(target=handle_user_input, args=(username,)).start()

        return 0
    except:
        cli_socket.close()
        return 0


if __name__ == "__main__":
    main()