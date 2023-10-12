import socket
import sys
import os.path

def main():
    """
        Creates a webserver that listens for requests from clients,
        receives requests, finds the corresponding file and 
        responds with that file if found.

    """

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
    
    # Start process of listening for requests and send responses
    sock_lisen(port)


def sock_lisen(port):
    """Passed a port number to create a socket that will listen for incoming connections.

    Args:
        port (int): What port the socket will be bound to.
    """

    # Create server socket and start it listening
    sock = socket.socket()
    sock.bind(("", port)) # Using default localhost for IP
    sock.listen()

    # Inform user on which URL to go to to make requests.
    print("Now listening at URL: localhost:{}".format(port))
    accept_connections(sock)


def accept_connections(lisSock):
    """Accepts requests from the socket, then sends off requests to be handled.
        Note: loops forever

    Args:
        lisSock (Socket): The socket that the server is currently listening on
    """

    # NOTE Server will run until it is manually shutdown
    while True:

        # Accept a connection then send off request to be handled
        newConn = lisSock.accept()
        newSocket = newConn[0]
        handle_request(newSocket)

        # Done with new socket, close it down
        newSocket.close()

def handle_request(socket):
    """Gets the file name and data from other functions, then sends that data off to be made
        into a response.
            Note: Loops until all requests have been filled for the socket.

    Args:
        socket (Socket): The socket that is currently sending requests
    """

    # Get the fileName from request, then send it off to be put into a reponse
    fileName, rawRequest = get_request(socket)
    send_res(fileName, socket)
    
    # Checks to see if there were any more requests from current connected socket.
    if not rawRequest.decode("ISO-8859-1").find("\r\n\r\n"):
        handle_request(socket)


def get_request(connectedSocket):
    """Gets and Returns the file name from the request, as well as the raw request data.

    Args:
        connectedSocket (_type_): _description_

    Returns:
        String: The file name
        Request: Byte representation of the request from the socket
    """

    # Get the request from the socket
    rawRequest = connectedSocket.recv(4096)
    
    # Strips down the request for file name
    getRequest = rawRequest.decode("ISO-8859-1").split("\r\n")[0]
    rawFilePath = getRequest.split(" ")[1]
    fileName = os.path.split(rawFilePath)[1]

    return fileName, rawRequest


def send_res(fileName, sock):
    """Sends the requested file in a response
        If file not found, it will sends an error message.

    Args:
        fileName(String): The name of the file the is being requested
        sock (Socket): The Socket to respond on
    """
    # Gets the data for the file requested
    fileData = get_file(fileName)

    # Generate a response based on if the content was found or not
    if fileData:
        contentType = get_content_type(os.path.splitext(fileName)[1])
        contentLength = len(fileData.encode("ISO-8859-1"))
        response = f"HTTP/1.1 200\r\nContent-Type: {contentType}\r\nContent-Length: {contentLength}\r\nConnect: close\r\n\r\n{fileData}".encode("ISO-8859-1")
    else:
        response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnect: close\r\n\r\n404 not found".encode("ISO-8859-1")
    
    # Send response back
    sock.sendall(response)


def get_file(fileName):
    """Finds and returns the file by its name

    Args:
        fileName (String): The name of the file to find

    Returns:
        Data: The files data (None if file not found)
    """
    try:
        with open(fileName) as fp:
            data = fp.read()
            return data
    except:
        # File not found or other error
        return

def get_content_type(fileType):
    """Finds the content type based off of file type

    Args:
        fileType (String): The file type

    Returns:
        String: The content type
    """
    contentTypes = {".txt": "text/plain",
                    ".html:": "text/html"}
    
    return contentTypes.get(fileType)

# Start the program
main()

