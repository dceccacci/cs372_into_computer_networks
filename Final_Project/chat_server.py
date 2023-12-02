# Example usage:
#
# python chat_server.py 3490
import sys
import socket
import select
import json

class ChatServer:

    def __init__(self):
        # Packet Size
        self.PACKET_LEN_SIZE = 2
        # A set to keep track of all the socket connections
        self.socketSet = set()
        # Buffer for Byte data sent by Clients
        self.recvBuffer = {}
        # Client Aliases
        self.clientAlias = {}
        

    def run(self, port):
        
        # Create and add the listening socket
        listenSocket = self.listen_socket(port)
        self.add_to_socket_set(listenSocket)

        while True:
            # Get the list of sockets that are ready to recv or accept from
            readyToRead, _, _ = select.select(self.get_socket_set(), {}, {})

            for readySocket in readyToRead:
                # New connection coming in
                if readySocket is listenSocket:
                    newConnection = readySocket.accept()
                    # Add socket to the set and create a buffer
                    self.add_to_socket_set(newConnection[0])
                    self.add_connection_to_recv_buffer(newConnection[0])
                else:
                    data = get_data(self, socket)
                    if len(data) == 0:
                        # Client has transmitted that they are disconnecting
                        self.transmit_disconnect(readySocket, listenSocket)
                        self.remove_from_socket_set(readySocket, listenSocket)
                        self.remove_from_recv_buffer(readySocket, listenSocket)
                        self.remove_from_client_alias(readySocket, listenSocket)
                        
                    # Get packet buffer
                    packetBuffer = self.get_buffer_from_recv_buffer(readySocket)
                    # Process the received packet
                    decodedPayload = self.process_recv(readySocket, data, packetBuffer)
                    payloadType = self.get_payload_type(decodedPayload)
                    
                    # Process the Payload
                    if payloadType == "hello":
                        # Add the alias
                        alias = decodedPayload["nick"]
                        self.add_alias(readySocket, alias)
                        self.transmit_connected(readySocket, listenSocket)
                    elif payloadType == "chat":
                        # Send out the chat to all clients
                        self.transmit_message(readySocket, listenSocket, decodedPayload)
                    else:
                        # Invalid Payload Type
                        pass


    def listen_socket(self, port):
        # Creates and returns a listener socket
        s = socket.socket()
        s.bind(('', port))
        s.listen()

        return s



    # --- Functions to Get / Add / Remove from self variables ---
    def get_socket_set(self):
        return self.socketSet
    
    def add_to_socket_set(self, socket):
        socketSet = self.get_socket_set()
        socketSet.add(socket)
        
    def remove_from_socket_set(self, socket):
        socketSet = self.get_socket_set()
        socketSet.remove(socket)
        pass
    
    def recv_buffer(self):
        return self.recvBuffer
    
    def get_buffer_from_recv_buffer(self, socket):
        buffer = recv_buffer()
        return self.buffer[socket]
        
    def add_connection_to_recv_buffer(self, connection):
        recvBuffer = self.recv_buffer
        recvBuffer[connection] = b''
    
    def remove_from_recv_buffer(self, socket):
        recvBuffer = self.recv_buffer()
        recvBuffer.pop(socket)
    
    def client_alias(self):
        return self.clientAlias
    
    def add_alias(self, socket, alias):
        allAliases = self.client_alias()
        allAliases[socket] = alias
    
    def get_alias(self, socket):
        allAliases = self.client_alias()
        return allAliases[socket]
    
    def remove_from_client_alias(self, socket):
        clientAlias = self.client_alias()
        clientAlias.pop(socket)
    
    def expected_packet_length():
        return self.PACKET_LEN_SIZE
    # --- End of functions to Get / Add / Remove from self variables ---
    
    
    
    
    # ---- Functions to process Recv Packet -------------
    
    def get_data(self, socket):
        return socket.recv(4096)
    
    
    def process_recv(self, newData, buffer):
        
        # Add data to the current buffer
        buffer += recvData
        
        expectedLength = self.expected_packet_length()
        
        # Check to see if buffer has at least the packet length
        if len(buffer) >= expectedLength:
            packetLength = int.from_bytes(buffer[:expectedLength], "big")

            # Check if the buffer has a full payload packet
            if len(buffer) >= (packetLength + expectedLength):
                # Extract and Decode Payload
                DecodedPayload = self.extract_payload(buffer, expectedLength, packetLength)
                return DecodedPayload
    
    
    def extract_payload(self, buffer, expectedLength, packetLength):
        # Get payload after length bytes
        payloadBytes = buffer[expectedLength:]
        # Decode those bytes
        payloadDecoded = payloadBytes.decode("ISO-8859-1")
        # Remove the packet from buffer
        buffer = buffer[(expectedLength + packetLength):]
        return payloadDecoded
    # ---- End of Functions to process Recv Packet -------------



    # ---- Functions to process Payload -----
    def get_payload_type(self, payload):
        return payload["type"]
    
    def transmit_disconnect(self, leavingSocket, listenSocket):
        # Get the socket set
        socketSet = self.get_socket_set()
        
        # Create the leave message
        alias = self.get_alias(leavingSocket)
        message = {"type": "leave", "nick": alias}
        jsonMessage = json.dumps(message)
        encodedMessage = jsonMessage.encode()
        
        for socket in socketSet:
            if socket is not listenSocket and socket is not leavingSocket:
                socket.sendall(encodedMessage)
                
                
    
    def transmit_connected(self, socket, listenSocket):
        # Get the socket set
        socketSet = self.get_socket_set()
        
        # Create the leave message
        alias = self.get_alias(leavingSocket)
        message = {"type": "join", "nick": alias}
        jsonMessage = json.dumps(message)
        encodedMessage = jsonMessage.encode()
        
        for socket in socketSet:
            if socket is not listenSocket and socket is not leavingSocket:
                socket.sendall(encodedMessage)
    
    
    def transmit_message(self, socket, listenSocket, message):
        # Get the socket set
        socketSet = self.get_socket_set()
        
        # Create the leave message
        alias = self.get_alias(leavingSocket)
        message = {"type": "chat", "nick": alias, "message": message}
        jsonMessage = json.dumps(message)
        encodedMessage = jsonMessage.encode()
        
        for socket in socketSet:
            if socket is not listenSocket and socket is not leavingSocket:
                socket.sendall(encodedMessage)
    

    # ---- End of Functions to process Payload -----
    
    
    
    
    

#--------------------------------#
# Starts running the server #
#--------------------------------#

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    server = ChatServer()
    server.run(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
