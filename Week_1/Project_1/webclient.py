import socket
import sys


def main():
    # Web client that makes requests on prints responses.

    # Check to see if a host was given, if not use default: "example.com"
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        # Check to see if the user used "www."; if so, strip it off
        if sys.argv[1].startswith("www."):
            host = sys.argv[1].lstrip("www.")
        else:
            host = sys.argv[1]
    else:
        host = "example.com"

    # Checks to see if a host was NOT given and only a port was
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    # Checks to see if a host was given and a port was given
    elif len(sys.argv) > 2 and sys.argv[2].isdigit():
        port = int(sys.argv[2])
    
    # Default, if no port was given
    else:
        port = 80
    
    # Create and connect to a socket
    sock = connect(host, port)

    # Send a request to the host
    sendAll(sock, host)

    # Receive and print response from host
    receive(sock)

    # Done with the socket, close it
    sock.close()


def connect(host, port):
    """Create a socket to make connection with

    Args:
        host (String): Host to connect to
        port (Int): The port number

    Returns:
        Sock: The socket that is now used for the connection
    """
    
    # Create socket
    sock = socket.socket()
    # Connect to the host and port
    sock.connect((host, port))
    # Return the connected socket
    return sock


def sendAll(sock, host):
    """Make a request to the passed socket

    Args:
        sock (Socket): The Socket that you are using for the connection
        host (String): The host that you are making the request to
    """
    # Create request
    req = f"GET / HTTP/1.1\r\nHost: www.{host}\r\nConnection: close\r\n\r\n".encode("ISO-8859-1")
    # Send request
    sock.sendall(req)


def receive(sock):
    """Get the responses on the socket and print them out

    Args:
        sock (Socket): The socket with the responses
    """
    # Get the first response and print it
    d = sock.recv(4096)
    print(d.decode("ISO-8859-1"))

    # If there more to receive, get and print them
    while len(d) > 0:
        d = sock.recv(4096)
        print(d.decode("ISO-8859-1"))

# Start the program
main()