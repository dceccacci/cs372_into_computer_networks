# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    """ 
        A server that accepts connections and prints the data 
        sent by the clients.

    """
    # A set to keep track of all the socket connections
    socketSet = set()

    # Create and add the listening socket
    listenSocket = listen_socket(port)
    socketSet.add(listenSocket)

    while True:
        # Get the list of sockets that are ready to recv or accept from
        readyToRead, _, _ = select.select(socketSet, {}, {})

        for readySocket in readyToRead:
            # New connection coming in
            if readySocket is listenSocket:
                newConnection = readySocket.accept()
                socketSet.add(newConnection[0])
                print_connection(newConnection)
            else:
                recvData = readySocket.recv(4096)

                # Client has said that they are done transmitting
                if len(recvData) == 0:
                    print_disconnection(readySocket)
                    socketSet.remove(readySocket)
                else:
                    print_data(recvData, readySocket)


def print_connection(socket):
    # Prints the connection message when a client connects
    print(f'{socket[0].getpeername()}: connected')


def print_disconnection(socket):
    # Prints the disconnect message when a client disconnects
    print(f'{socket.getpeername()}: disconnected')


def print_data(data, socket):
    # Prints the message data sent by the client
    dataLength = len(data)
    print(f'{socket.getpeername()} {dataLength} bytes: {data}')


def listen_socket(port):
    # Creates and returns a listener socket
    s = socket.socket()
    s.bind(('', port))
    s.listen()

    print("waiting for connections")
    return s

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
