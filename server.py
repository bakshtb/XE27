#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol
import glob
import os
import shutil
import subprocess
import pyautogui

IP = "0.0.0.0"
PHOTO_PATH = r"C:\server_screen.jpg"  # The path + filename where the screenshot at the server should be saved


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
        if command in ['DIR', 'DELETE', 'EXECUTE']:
            # if the param is "C:\New folder" then the split will return two  params because the space
            params = [' '.join(params)]
            if not os.path.exists(params[0]):
                return False, "ERROR", []
            if command == 'DIR':
                params[0] += "\*.*"
        if command in ['COPY']:
            if not os.path.isfile(params[0]) or os.path.isfile(params[1]):
                return False, "ERROR", []
        return True, command, params
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
            response = '\n'.join(glob.glob(params[0]))
        elif command == "DELETE":
            os.remove(params[0])
            response = "OK"
        elif command == "COPY":
            shutil.copy(params[0], params[1])
            response = "OK"
        elif command == "EXECUTE":
            subprocess.call(params[0])
            response = "OK"
        elif command == "TAKE_SCREENSHOT":
            image = pyautogui.screenshot()
            image.save(PHOTO_PATH)
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
                print("received: Command=", command, "Params=", params)
                if command != 'SEND_PHOTO':
                    res = handle_client_request(command, params)
                    res = protocol.create_msg(res)
                    client_socket.send(res.encode())
                else:
                    # first, sending the picture size.
                    pic_size = str(os.path.getsize(PHOTO_PATH))
                    pic_size = protocol.create_msg(pic_size)
                    client_socket.send(pic_size.encode())
                    # second, sending the picture.
                    with open(PHOTO_PATH, 'rb') as pic:
                        pic_bytes = pic.read()
                        client_socket.send(pic_bytes)

                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                res = protocol.create_msg(response)
                client_socket.send(res.encode())
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            res = protocol.create_msg(response)
            client_socket.send(res.encode())

            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
