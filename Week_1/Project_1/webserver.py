import socket
import sys

def main():
    # Creates a webserver that sends a simple reply of "Hello"

    # NOTE Selecting a host has not been implemented yet.

    # Checks to see if a host was NOT given and only a port was
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])

    # Checks to see if a host was given and a port was given
    elif len(sys.argv) > 2 and sys.argv[2].isdigit():
            port = int(sys.argv[2])
    
    # Default, if no port was given
    else:
        port = 28333
    
    # Creates a socket on desired port to start listening on
    sockLis = sock_lisen(port)

    # Start accepting requests on that listening socket
    accept_request(sockLis)


def sock_lisen(port):
    """Passed a port number to create a socket that will listen for incoming connections.

    Args:
        port (int): What port the socket will be bound to.

    Returns:
        Socket: A socket that will listen for incoming connections.
    """

    # Create server socket
    sock = socket.socket()
    # Bind socket to default localhost and to the passed port
    sock.bind(("", port))
    sock.listen()

    # Inform user on which URL to go to to make requests.
    print("Now listening at URL: localhost:{}".format(port))
    return sock


def accept_request(lisSock):
    """Accepts requests on the server socket and calls function send_res() to make response.
        Note: loops forever

    Args:
        lisSock (Socket): The socket that the server is currently listening on
    """

    # Server will run until it is manually shutdown
    while True:
        newConn = lisSock.accept()
        newSocket = newConn[0] # index [0] is the new socket
        
        # Send of request for response
        send_res(newSocket)
        
        # Done with new socket, close it down
        newSocket.close()

def send_res(sock):
    """Sends a response to a request

    Args:
        sock (Socket): The Socket to receive and respond to
    """
    # Get the first request
    d = sock.recv(4096)

    # The default response to all requests
    res = f"HTTP/1.1 200\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnect: close\r\n\r\nHello!".encode("ISO-8859-1")
    
    # Send response
    sock.sendall(res)

    # If there is more to the request, send another response.
    while not d.decode("ISO-8859-1")[-4:] == "\r\n\r\n":
        d = sock.recv(4096)
        sock.sendall(res)
    

# Start the program
main()

