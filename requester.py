import socket
import struct 

def printReceiptInformation(header, data):
    print("time received: ")
    print("sender's IP address: ", sender_address[0], " sender's port: ", sender_address[1])
    print("packet type: ", header[0].decode('ascii'))
    print("sequence number: ", header[1])
    print("payload length: ", header[2])
    print("first 4 bytes of the payload: ", data[:4].decode("utf-8"))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 1) parse command line args and get requester port number and file to request name

# 2) read tracker.txt and retrieve sender name and port number and other details

udp_host = socket.gethostname()
udp_port = 12345

sock.bind((udp_host, udp_port))

while True:
    print("Waiting for client...")

    packet_with_header, sender_address = sock.recvfrom(1024)
    header = struct.unpack("!cII", packet_with_header[:9])
    data = packet_with_header[9:]

    printReceiptInformation(header, data)

    
    
