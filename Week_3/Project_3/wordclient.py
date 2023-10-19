import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    global packet_buffer

    while True:

        # Start checking to see if the full packet is in the buffer
        if len(packet_buffer) >= WORD_LEN_SIZE:
            packetLength = int.from_bytes(packet_buffer[:2], "big")

            # Full Packet in buffer, Extract and Return
            if len(packet_buffer) >= (packetLength + 2):
                fullPacket = packet_buffer[:packetLength + 2]
                packet_buffer = packet_buffer[packetLength + 2:]
                return fullPacket

        # Get new Data from Socket
        newData = s.recv(4096)

        # No new Data recieved, Return None
        if len(newData) == 0:
            return None
        
        # There was new data, Add it to the buffer
        packet_buffer += newData


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    wordBytes = word_packet[2:]
    wordDecoded = wordBytes.decode("ISO-8859-1")
    return wordDecoded

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
