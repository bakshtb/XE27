#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol

IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = r"C:\client_screen.jpg"  # The path + filename where the copy of the screenshot at the client should be saved


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    valid_msg, res = protocol.get_msg(my_socket)
    #  If server's response is valid, print it
    if valid_msg:
        if cmd != 'SEND_PHOTO':
            print("Server respond:", res)
        else:
            img_size = int(res)
            with open(SAVED_PHOTO_LOCATION, 'wb+') as pic:
                img_bytes = my_socket.recv(img_size)
                pic.write(img_bytes)
    else:
        print("Response not valid\n")


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet.encode())
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
