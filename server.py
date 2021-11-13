#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol
import glob
import os
import shutil


IP = "0.0.0.0"
PHOTO_PATH = r"C:\server_screen.jpg" # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """

    cmd_words = cmd.split()
    is_valid = protocol.check_cmd(cmd)
    if is_valid:
        command = cmd_words[0]
        params = cmd_words[1:]
        return is_valid, command, params
    else:
        return is_valid, "ERROR", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = 'ERROR'
    try:
        if command == "DIR":
            response = glob.glob(params)
        elif command == "DELETE":
            os.remove(params)
            response = "OK"
        elif command == "COPY":
            shutil.copy(params[0], params[1])
            response = "OK"
    except Exception as ex:
        response = "ERROR! " + str(ex)

    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:

                # (6)

                # prepare a response using "handle_client_request"

                # add length field using "create_msg"

                # send to client

                if command == 'SEND_FILE':
                    # Send the data itself to the client

                    # (9)
                
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            #send to client

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
