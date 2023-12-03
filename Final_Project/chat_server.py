#--------------------------------#
# Example usage:                 #
# python chat_server.py 3490     #
#--------------------------------#

import sys
import socket
import select
import json



# Packet Size
PACKET_LEN_SIZE = 2
# A set to keep track of all the socket connections
socketSet = set()
# Buffer for Byte data sent by Clients
recvBuffer = {}
# Client Aliases
clientAlias = {}
    

def run_server(port):
    
    # Create and add the listening socket
    listenSocket = listen_socket(port)
    add_to_socket_set(listenSocket)

    while True:
        # Get the list of sockets that are ready to recv or accept from
        readyToRead, _, _ = select.select(get_socket_set(), {}, {})

        for readySocket in readyToRead:
            # New connection coming in
            if readySocket is listenSocket:
                newConnection = readySocket.accept()
                # Add socket to the set and create a buffer
                add_to_socket_set(newConnection[0])
                add_connection_to_recv_buffer(newConnection[0])
            else:
                try:
                    data = get_data(readySocket)
                except:
                    # Client has transmitted that they are disconnecting
                    transmit_disconnect(readySocket, listenSocket)
                    remove_from_socket_set(readySocket)
                    remove_from_recv_buffer(readySocket)
                    remove_from_client_alias(readySocket)
                    break
                    
                # Get packet buffer
                packetBuffer = get_buffer_from_recv_buffer(readySocket)
                # Process the received packet
                decodedPayload = process_recv(data, packetBuffer)
                payloadType = get_payload_type(decodedPayload)
                
                # Process the Payload
                if payloadType == "hello":
                    # Add the alias
                    alias = decodedPayload["nick"]
                    add_alias(readySocket, alias)
                    transmit_connected(readySocket, listenSocket)
                elif payloadType == "chat":
                    # Send out the chat to all clients
                    transmit_message(readySocket, listenSocket, decodedPayload)
                else:
                    # Invalid Payload Type
                    pass
                


def listen_socket(port):
    # Creates and returns a listener socket
    s = socket.socket()
    s.bind(('', port))
    s.listen()

    return s



# --- Functions to Get / Add / Remove from  variables ---
def get_socket_set():
    return socketSet

def add_to_socket_set(socket):
    socketSet = get_socket_set()
    socketSet.add(socket)
    
def remove_from_socket_set(socket):
    socketSet = get_socket_set()
    socketSet.remove(socket)
    pass

def recv_buffer():
    return recvBuffer

def get_buffer_from_recv_buffer(socket):
    buffer = recv_buffer()
    return buffer[socket]
    
def add_connection_to_recv_buffer(connection):
    recvBuffer = recv_buffer()
    recvBuffer[connection] = b''

def remove_from_recv_buffer(socket):
    recvBuffer = recv_buffer()
    recvBuffer.pop(socket)

def client_alias():
    return clientAlias

def add_alias(socket, alias):
    allAliases = client_alias()
    allAliases[socket] = alias

def get_alias(socket):
    allAliases = client_alias()
    return allAliases[socket]

def remove_from_client_alias(socket):
    clientAlias = client_alias()
    clientAlias.pop(socket)

def expected_packet_length():
    return PACKET_LEN_SIZE
# --- End of functions to Get / Add / Remove from  variables ---




# ---- Functions to process Recv Packet -------------

def get_data(socket):
    return socket.recv(4096)


def process_recv(newData, buffer):
    
    # Add data to the current buffer
    buffer += newData
    
    expectedLength = expected_packet_length()
    
    # Check to see if buffer has at least the packet length
    if len(buffer) >= expectedLength:
        packetLength = int.from_bytes(buffer[:expectedLength], "big")

        # Check if the buffer has a full payload packet
        if len(buffer) >= (packetLength + expectedLength):
            # Extract and Decode Payload
            decodedPayload = extract_payload(buffer, expectedLength, packetLength)
            return decodedPayload


def extract_payload(buffer, expectedLength, packetLength):
    # Get payload after length bytes
    payloadBytes = buffer[expectedLength:]
    # Decode those bytes into Python native data
    payloadDecoded = payloadBytes.decode("ISO-8859-1")
    print(f"\n Type: {type(payloadDecoded)} \n")
    print(f"\n message: {payloadDecoded} \n")
    payloadDecoded = json.loads(payloadDecoded)
    print(f"\n Type: {type(payloadDecoded)} \n")

    # Remove the packet from buffer
    buffer = buffer[(expectedLength + packetLength):]

    return payloadDecoded
# ---- End of Functions to process Recv Packet -------------



# ---- Functions to process Payload -----
def get_payload_type(payload):
    return payload.get("type")


def transmit_disconnect(leavingSocket, listenSocket):
    # Create the leave message
    alias = get_alias(leavingSocket)
    message = {"type": "leave", "nick": alias}
    
    # Send message off to be transmitted
    transmit_to_clients(listenSocket, message)
            
            
def transmit_connected(connectingSocket, listenSocket):
    # Get the socket set
    socketSet = get_socket_set()
    
    # Create the connecting message
    alias = get_alias(connectingSocket)
    message = {"type": "join", "nick": alias}
    
    # Send message off to be transmitted
    transmit_to_clients(listenSocket, message)


def transmit_message(TransmittingSocket, listenSocket, payload):

    # Create the chat message
    alias = get_alias(TransmittingSocket)
    payloadMessage = payload.get("message")
    message = {"type": "chat", "nick": alias, "message": payloadMessage}
    
    # Send message off to be transmitted
    transmit_to_clients(listenSocket, message)


def transmit_to_clients(listenSocket, message):
    # Get the socket set
    socketSet = get_socket_set()
    
    # Message Into Json File and Encode
    jsonMessage = jsonMessage = json.dumps(message)
    encodedMessage = jsonMessage.encode()
    # Get Size of Message and Encode
    messageSize = len(encodedMessage)
    encodedMessageSize = messageSize.to_bytes(PACKET_LEN_SIZE , byteorder='big')
    # Combine
    fullPacket = encodedMessageSize + encodedMessage
    
    # Send Packet
    for socket in socketSet:
        if socket is not listenSocket:
            print(f'To: {socket.getpeername()} Packet: {fullPacket}')
            try: 
                print('send successful')
                socket.sendall(fullPacket)
            except:
                # Socket already Disconnected
                continue

# ---- End of Functions to process Payload -----
    
    
    
    
    

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1
    
    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
