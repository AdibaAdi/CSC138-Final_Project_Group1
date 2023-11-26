# Usage: python3 client.py <server-name> <port>

from socket import *
import sys

# Function to check if a string is alphanumeric
def is_alphanumeric(string: str):
    return string.isalnum()

def main():
    # Initialize TCP socket
    cli_socket = socket(AF_INET, SOCK_STREAM)
    cli_socket.settimeout(10)

    # Check for correct usage
    if len(sys.argv) != 3:
        print("Usage: python client.py <server-name> <port>")
        sys.exit(1)

    server_name = sys.argv[1]
    server_port = int(sys.argv[2])

    # Try to connect to the server
    try:
        cli_socket.connect((server_name, server_port))
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # Prompt user to send JOIN command with their username
    while True:
        join_command = input("Enter JOIN followed by your username: ")
        join_args = join_command.split()

        # Validate the user's input
        if len(join_args) == 2 and len(join_args[1]) > 0 and is_alphanumeric(join_args[1]) and join_args[0].upper() == "JOIN":
            break
        print("Invalid command format. Please enter JOIN followed by your username.")

    # Send the JOIN request and receive server response
    server_response = send_and_receive(cli_socket, join_command)
    print(server_response)

    # Main loop to process user commands
    while True:
        user_command = input("Enter command: ")
        server_response = send_and_receive(cli_socket, user_command)
        if not process_server_response(cli_socket, server_response):
            break

    cli_socket.close()

# Send a message to the server and wait to receive the response
def send_and_receive(cli_socket, message: str):
    try:
        cli_socket.send(message.encode())  # Use send for TCP socket
        return cli_socket.recv(1024).decode()
    except (BrokenPipeError, ConnectionResetError):
        print("Server has closed the connection.")
        return None
    except Exception as e:
        print(f"Error in communication: {e}")
        return None

# Process response messages from the server
def process_server_response(cli_socket, message):
    if message is None:
        print("Connection lost.")
        return False

    print("Server:", message)
    if message.startswith("JOIN Success"):
        return True
    elif "Error" in message or message.startswith("QUIT"):
        return False

    # Adding additional response processing as needed
    return True

if __name__ == "__main__":
    main()
