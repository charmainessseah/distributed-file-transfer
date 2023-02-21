import sys
from enum import Enum
import socket
import struct

class Packet_Type(Enum):
    request = 'R'
    data = 'D'
    end = 'E'

# variables sent as command line arguments, initializing with dummy values
requester_port_number = 12345
sender_port_number = 12344
sequence_number = 0
data_length = 0
rate = 0

def check_input(arg):
    index = -1
    for i in range(0, len(sys.argv)):
        if(str(sys.argv[i]) == arg):
            return i
    return index

def check_sys_args():

    global requester_port_number, sequence_number, data_length, rate
    
    if(len(sys.argv) != 11):
        print('Please enter correct number of arguments!')
        exit()

    p_index = check_input('-p')
    
    if(p_index != -1 and p_index != 10):
        if((not sys.argv[p_index + 1].isdigit()) or int(sys.argv[p_index + 1]) <= 2049 or int(sys.argv[p_index + 1]) >= 65536):
            print('Please enter sender port number integer value in range (2049, 65536)')
            exit()
        else:
            sender_port_number = int(sys.argv[p_index + 1])
    else:
        print('Please enter sender port number in correct format')
        exit()
    
    g_index = check_input('-g')
    if(g_index != -1 and g_index != 10):
        if((not sys.argv[g_index + 1].isdigit()) or int(sys.argv[g_index + 1]) <= 2049 or int(sys.argv[g_index + 1]) >= 65536):
            print('Please enter requester port number integer value in range (2049, 65536)')
            exit()
        else:
            requester_port_number = int(sys.argv[g_index + 1])
    else:
        print('Please enter arguments in correct format')
        exit()

    r_index = check_input('-r')
    if(r_index != -1 and r_index != 10):
         if not sys.argv[r_index + 1].isdigit():
            print('Please enter integer value for the rate')
            exit()
         else:
            rate = int(sys.argv[g_index + 1])
    else:
        print('Please enter correct arguments in correct format')
        exit()
    
    l_index = check_input('-l')
    if(l_index != -1 and l_index != 10):
         if not sys.argv[r_index + 1].isdigit():
            print('Please enter integer value for the rate')
            exit()
         else:
            data_length = int(sys.argv[r_index + 1])
    else:
        print('Please enter correct arguments in correct format')
        exit()

    q_index = check_input('-q')
    if(q_index != -1 and q_index != 10):
         if not sys.argv[q_index + 1].isdigit():
            print('Please enter integer value for the rate')
            exit()
         else:
            sequence_number = int(sys.argv[q_index + 1])
    else:
        print('Please enter correct arguments in correct format')
        exit()

# print packet information before each packet is sent to the requester
def print_packet_information(requester_host_name, sequence_number, data, packet_type):
    if (packet_type == 'D'):
        print('DATA Packet')
    elif (packet_type == 'E'):
        print('END Packet')

    print('send time: ')
    print('requester addr: ', requester_host_name)
    print('Sequence num: ', sequence_number)
    print('length: ', len(data))
    print('payload: ', data.decode('utf-8'))
    print()

def read_file(file_name):
    try:
        with open(file_name, 'r') as reader:
            data = reader.read()
            return data
    except:
        print('Please enter the correct file name!')

check_sys_args()
print('sender port number: ', sender_port_number)
print('requester port number: ', requester_port_number)

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_host = socket.gethostname()
sock.bind((udp_host, sender_port_number))

# wait for request packet
print('waiting for requester to send the filename it wants to retrieve...')
packet_with_header, sender_address = sock.recvfrom(1024)
header = struct.unpack("!cII", packet_with_header[:9])
file_name = packet_with_header[9:]

print('request packet data sent a file name which is: ', file_name.decode('utf-8'))

requester_host_name = socket.gethostname()

# read the file data
print('reading file...')
data = read_file(file_name).encode()
print(data)

# assemble udp header
packet_type = (Packet_Type.data.value).encode('ascii')
sequence_number = 1112
data_length = len(data) 
header = struct.pack('!cII', packet_type, sequence_number, data_length)

packet_with_header = header + data

print('-----------------------------------------------------------------------------')
print('sender', sequence_number, "'s print information:")

# send data
sock.sendto(packet_with_header, (requester_host_name, requester_port_number))
print_packet_information(requester_host_name, sequence_number, data, packet_type.decode())

# send END packet after all data has been sent
data = ''.encode()
packet_type = (Packet_Type.end.value).encode('ascii')
sequence_number = 1112
data_length = 0 
header = struct.pack('!cII', packet_type, sequence_number, data_length)

packet_with_header = header + data
sock.sendto(packet_with_header, (requester_host_name, requester_port_number))
print_packet_information(requester_host_name, sequence_number, data, packet_type.decode())

print('-----------------------------------------------------------------------------')