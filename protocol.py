#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    data_words = data.split()
    if data_words[0] in ['TAKE_SCREENSHOT', 'SEND_PHOTO', 'EXIT']:
        if len(data_words) == 1:
            return True
    elif data_words[0] in ['DIR', 'DELETE', 'EXECUTE']:
        # if the cmd is "DIR C:\New folder" data_words = 2
        if len(data_words) >= 2:
            return True
    elif data_words[0] in ['COPY']:
        if len(data_words) == 3:
            return True

    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    length = str(len(data))
    zfill_length = str(length.zfill(LENGTH_FIELD_SIZE))
    return zfill_length + data


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    try:
        length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
        message = my_socket.recv(int(length)).decode()
        return True, message

    except Exception as ex1:
        return False, "get_msg Error"
