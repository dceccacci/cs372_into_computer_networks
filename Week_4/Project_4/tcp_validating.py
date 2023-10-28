import socket

def validating_tcp_packet(fileNameAddress, fileNameData):
    """ Validate if the TCP packet arrived correctly

        Args:
            fileNameAddress(String): Name of the file that has the IP address
            fileNameData(String): Name of the file that has the TCP data

        Return:
            True: If the Checksums are equal
            False: If the Checksums are NOT equal
    """

    # Get data from files
    dataFromFileAddress = get_data_from_file(fileNameAddress, "r")
    tcpData = get_data_from_file(fileNameData, "rb")

    # Create IP peusdo Header
    tcpLength = file_length_in_bytes(tcpData)
    pseudoHeader = create_pseudo_header(dataFromFileAddress, tcpLength)

    # Get Orginal TCP checksum
    tcpOrginalCkSum = int.from_bytes(tcpData[16:18], "big")

    # Create a TCP Header with a Zero Checksum
    tcpHeaderZeroCkSum = tcpData[:16] + b'\x00\x00' + tcpData[18:]

    # Make TCP header an even number of bytes
    if len(tcpHeaderZeroCkSum) % 2 == 1:
        tcpHeaderZeroCkSum += b'\x00'
    
    # Calculate Checksum
    checkSum = check_sum(pseudoHeader, tcpHeaderZeroCkSum)

    # Compair Calculated Checksum to Orginal Checksum
    if tcpOrginalCkSum == checkSum:
        return True
    else:
        return False


# ----- Below: Get Data out of a file ----------

def get_data_from_file(fileName, readType):
    """ Opens a file and returns its data

        Args:
            fileName(String): Name of the file to open
            readType(String): The type of data in the file

        Return:
            Data: Data from opened file.
    """
    # Open file and return its data
    with open(fileName, readType) as fp:
        fileData = fp.read()
    return fileData


# ----- Below Is Code to Create the Pseudo Header -----------

def get_byte_strings(fileData):
    """ Extract and Convert a String IPv4 Addresses from a file into Source and Destination
        Byte Strings then return them.

        Args:
            fileData(String): String Data from Address File
        
        Return:
            byte string: Source IP in a byte string
            byte string: Destination IP in a byte string

    """
    bothIPStrings = get_ip_strings_from_file(fileData)
    sourceBytes = ip_to_byte_string(bothIPStrings[0])
    destinationBytes = ip_to_byte_string(bothIPStrings[1])
    return sourceBytes, destinationBytes


def get_ip_strings_from_file(fileData):
    """ Seperate raw string data into IPv4: source and destination

        Args:
            fileData(String): Raw String Data from File

        Return:
            String List: A list of source and destination IP Strings
    """
    fileRemoveNewLine = fileData.split("\n")[0]
    fileSplitIPs = fileRemoveNewLine.split(" ")
    return fileSplitIPs


def ip_to_byte_string(ipString):
    """ Convert a IPv4 String into a byte string and return it

        Args:
            ipString(String): The IPv4 in String form

        Return:
            byte string: The Byte String of the 
    """
    byteString = b''
    ipValues = ipString.split(".")
    for value in ipValues:
        valueInByte = int(value).to_bytes(1,"big")
        byteString += valueInByte
    return byteString


def create_pseudo_header(dataFromFileAddress, tcpLength):
    """Creates a Pesudo IP Header

    Args:
        dataFromFileAddress (String): String data containing IP Addresses
        tcpLength (Bytes): The length of the TCP packet in Bytes

    Returns:
        Bytes: The Pseudo IP header in byte form
    """
    sourceIP, destIP = get_byte_strings(dataFromFileAddress)
    zero = b'\x00'
    protocol = b'\x06'
    pseudoHeader = b'' + sourceIP + destIP + zero + protocol + tcpLength
    return pseudoHeader


def file_length_in_bytes(fileData):
    """ Returns the length in bytes, of the TCP packet

    Args:
        fileData (Bytes): Raw data of the TCP packet

    Returns:
        Byte string: The length of the file as a byte string
    """
    return len(fileData).to_bytes(2,"big")


# ----- Below: TCP Header CheckSum ----------

def check_sum(pseudoHeader, tcpHeaderZeroCkSum):
    """Calculates the Check Sum of a TCP packet

    Args:
        pseudoHeader (byte string): A pseudo IP header
        tcpHeaderZeroCkSum (byte string): A TCP header with a zero check sum

    Returns:
        int: The calculated checksum of the TCP packet.
    """
    data = pseudoHeader + tcpHeaderZeroCkSum
    offset = 0
    total = 0
    while offset < len(data):
        word = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2
        total += word
        total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff 


# ------ Running and checking all files -----------
""" 
    Runs through each file and verifies if the calculated checksum is the same as
    the orginal checksum in the TCP packet.
"""
for i in range(10):
    addressFileName = "tcp_addrs_{}.txt".format(i)
    dataFileName = "tcp_data_{}.dat".format(i)
    result = validating_tcp_packet(addressFileName, dataFileName)
    if result:
        print("Files #{}: PASS".format(i))
    else:
        print("Files #{}: FAIL".format(i))