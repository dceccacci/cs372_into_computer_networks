# Example usage:
#
# python chat_client.py alice localhost 3490
# python chat_client.py bob localhost 3490
# python chat_client.py chris localhost 3490
#
# The first argument is a prefix that the server will print to make it
# easier to tell the different clients apart. You can put anything
# there.
import sys
import socket
import json
import threading
from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: select_client.py prefix host port", file=sys.stderr)

def main(argv):
    """
        Create a chat UI that allows the user to chat with other users through
        a chat server. Is able to both send and receive messages at the same time.
    """
    try:
        nick = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    # Make the client socket and connect
    serverSocket = socket.socket()
    serverSocket.connect((host, port))
    
    # Send connect message to server
    joinMessage = {"type": "hello", "nick": nick}
    send_message(serverSocket, joinMessage)

    # Start Chat Windows    
    init_windows()

    # Create a thread that handles incomming messages from the server.
    t1 = threading.Thread(target=runner, args=([serverSocket]), daemon=True)
    t1.start()

    while True:
        try:
            messageInput = read_command(nick + "> ")
        except:
            break
        
        # Special Character Used, Action Needed
        if messageInput[:1] == "/":
            parseAction(messageInput)
        
        # Prepare the message to send
        messageToSend = {"type": "chat", "message": messageInput}
        
        # Send message to server
        send_message(serverSocket, messageToSend)

    end_windows()

def parseAction(input):
    """
        Check to see if the user is trying to preform a special action.
    """
    if input[:2] == "/p":
        sys.exit()

def send_message(server, message):
    """
        Takes a string message, and converts it into bytes and send to the server.
    """
    # Encode Message
    jsonMessage = json.dumps(message)
    encodedMessage = jsonMessage.encode()
    # Get and Encode length
    messageSize = len(encodedMessage)
    encodedMessageSize = messageSize.to_bytes(2, byteorder='big')
    # Combine
    fullPacket = encodedMessageSize + encodedMessage
    
    server.send(fullPacket)

packet_buffer = b''

def runner(serverSocket):
    """
        Prints incomming messages from the server to the chats UI window.
    """
    
    global packet_buffer
    
    
    while True:
        # Get a message from the server
        message_packet = get_next_message_packet(packet_buffer, serverSocket)

        if message_packet is None:
            break

        # Get the messages type, and its nickname
        messageDecoded = extract_message(message_packet)
        messageType = messageDecoded.get("type")
        messageNick = messageDecoded.get("nick")
        
        # Create a message depending on its type
        if messageType == "join":
            toChatWindow = f"*** {messageNick} has joined the chat"
        elif messageType == "leave":
            toChatWindow = f"*** {messageNick} has left the chat"
        elif messageType == "chat":
            message = messageDecoded.get("message")
            toChatWindow = f"{messageNick}: {message}"

        # Send the message to the chat winow
        print_message(toChatWindow)
        



def get_next_message_packet(packet_buffer, serverSocket):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    while True:
            # Start checking to see if the full packet is in the buffer
            if len(packet_buffer) >= 2:
                packetLength = int.from_bytes(packet_buffer[:2], "big")
                
                # Full Packet in buffer, Extract and Return
                if len(packet_buffer) >= (packetLength + 2):
                    fullPacket = packet_buffer[:packetLength + 2]
                    packet_buffer = packet_buffer[packetLength + 2:]
                    return fullPacket
            
            # Get new Data from Socket
            newData = serverSocket.recv(4096)
            
            # No new Data recieved, Return None
            if len(newData) == 0:
                return None
            
            packet_buffer += newData

def extract_message(packet):
    """
    Extract the message from a message packet.

    packet: a message packet consisting of the encoded message length
    followed by the UTF-8 message.

    Returns the message decoded as Python native Data.
    """

    messageBytes = packet[2:]
    messageDecoded = messageBytes.decode("ISO-8859-1")
    message = json.loads(messageDecoded)
    
    return message

if __name__ == "__main__":
    sys.exit(main(sys.argv))
