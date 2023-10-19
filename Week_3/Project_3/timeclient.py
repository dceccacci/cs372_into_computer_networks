import socket
import time

def main():
    """
    Sets the host and port to allow a web socket to connect to the Atomic Clock
    """
    host = "time.nist.gov"
    port = 37
    create_socket(host, port)

def create_socket(host, port):
    """
    Creates a socket that connects to the host and port arguments.

    Args:
        host (String): The name of the host website to connect to
        port (Int): The Port number of the website to connect to

    """
    sock = socket.socket()
    sock.connect((host, port))
    get_time(sock)

def get_time(sock):
    """
    Gets the current time being sent by the website

    Args:
        sock (Socket): The socket that is connected to the website.
    """
    bitTime = sock.recv(4096)
    time = int.from_bytes(bitTime)
    print_time(time)

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

def print_time(atomicTime):
    """
    Prints the Atomic Clock time in seconds, and Prints the current time on the system
    since 1900

    Args:
        atomicTime(int): The time in seconds of the atomic clock
    """
    print("NIST time  : {}".format(atomicTime))
    print("System time: {}".format(system_seconds_since_1900()))

main()
