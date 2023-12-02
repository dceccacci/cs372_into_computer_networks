-- Client --

When a client first launches, the user will specifiy a nickname on the command line
along with the server information.

Then its very first packet it sends is a "hello" packet that also has the nickname in it.

After that, ever line the user types into the client gets sent to the server as a chat packet.

Client has a text user interface to help keep the output clean.

The clients output and input will be multithreaded.
    * The main sending thread will:
        * Send chat messages from the user to the server
        * Send chat messages from the user to the server
    * The receiving thread will:
        * Receive packets from the server
        * Display those results on-screen
(Note they do not share the same socket)

The client will be started by specifying the user's nickname, the server address, and the server port on the command line. These are all required arguments; there are no defaults.
```
python chat_client.py chris localhost 3490
```


-- Server --

When it gets a "hello" packet, it will take the nickname from the packet, and rebroadcast the connection event to all other clients.

Every chat packet (or connect or disconnect packet) that the client gets from the server is shown on the outputs.

* Packet handling
    * When looking at the data stream, make sure you have at least two bytes in your buffer so you can determine the JSON data length.

    * After that, see if the length (plus 2 for the 2-byte header) is in the buffer.



-- Packet Structure --

Communicates over TCP (stream) sokets using a defined packet structure.

A packet is a 16-bit big-endian number representing the payload length.

You can encode the JSON string to a UTF-8 bytes by calling .encode() on the string.


-- JSON Payloads --

Each packet starts with the two-byte length of the payload, followed by the payload.

The payload is a UTF-8 encoded string repr3esentigg a JSON object

Each payload is an Object, and has a field in it named "type" that represents the type of the payload. The remaining fields vary based on the type.


- Hello Payload - 

From client to server
{
    "type": "hello"
    "nick": "[user nickname]"
}


- Chat Payload -

from client to server
{
    "type": "chat"
    "message": "[message]"
}

from server to clients
{
    "type": "chat"
    "nick": "[sender nickname]"
    "message": "[message]"
}


- Join Payload -

from server to clients
{
    "type": "join"
    "nick": "[joiner's nickname]"
}


- Leave packet
{
    "type": "leave"
    "nick": "[leaver's nickname]"
}



===== Responsabilites =====

Server
    main() 
        Starts running the server on command line assigned Port
            run_server(port):

    run_server(port)
        Create needed passable Variables
            Creates sockets for the socket set
                socketSet = set()
            Creates listeningSocket
                listenSocket = listen_socket(port)
            Create a buffer Dictionary
                recvBuffer = {}
            Create a nickName Dictionary
                clientAlias = {}

        Sits and waits for the listening socket OR any other socket to be ready
            while True: readyToRead....
        If listening socket, New Sockets are added to the socketSet
            newConnection = readySocket.accept()
            socketSet.add(newConnection[0])
        Else, clients are sending data.
            Send socket off to a new function
                receive_data(readySocket)

    receive_data(socket, bufferDictionary)
        Check to see if there is a full packet in the buffer at socket key.
            if TRUE
                Extract packet, 
                



