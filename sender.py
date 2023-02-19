import argparse
from enum import Enum
import socket
import struct

class Packet_Type(Enum):
    request = 'R'
    data = 'D'
    end = 'E'

# print packet information before each packet is sent to the requester
def print_packet_information(requester_host_name, sequence_number, data_length, data):
    print("time packet is sent: ")
    print("IP address of requester: ", requester_host_name)
    print("sequence number: ", sequence_number)
    print("first 4 bytes of the payload: ", data[:4].decode("utf-8"))

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

requester_host_name = socket.gethostname()
requester_port_number = 12345

data = "Hello World! My name is Charmaine.".encode()

# assemble udp header
packet_type = (Packet_Type.data.value).encode('ascii')
sequence_number = 1112
data_length = len(data) 
udp_header = struct.pack("!cII", packet_type, sequence_number, data_length)

packet_with_header = udp_header + data

print_packet_information(requester_host_name, sequence_number, data_length, data)

sock.sendto(packet_with_header, (requester_host_name, requester_port_number))