import sys
import argparse
from enum import Enum
import socket
import struct

class Packet_Type(Enum):
    request = 'R'
    data = 'D'
    end = 'E'

#variables sent as command line arguments, initializing with dummy values
requester_port_number = 12345
sender_port_number = 12344
sequence_number = 0
data_length = 0
rate = 0


def check_sys_args():
    if(len(sys.argv) != 11):
        print('Please enter correct number of arguments!')
    if(str(sys.argv[1]) != '-p' | str(sys.argv[3]) != '-g' | str(sys.argv[5]) != '-r' | str(sys.argv[7]) != '-q' | str(sys.argv[9]) != '-l'):
        print('Please enter arguments! in correct format')
    if(int(sys.argv[2]) <= 2049 | int(sys.argv[2]) >= 65536):
        print('Please enter the correct sender port number')
    if(int(sys.argv[4]) <= 2049 | int(sys.argv[4]) >= 65536):
        print('Please enter the correct requester port number')
    global requester_port_number, sequence_number, data_length, rate
    requester_port_number = int(sys.argv[4])
    sequence_number = sys.argv[8]
    data_length = sys.argv[10]
    rate = sys.argv[6] 

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