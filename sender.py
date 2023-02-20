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

#elif(str(sys.argv[1]) != '-p' | str(sys.argv[3]) != '-g' | str(sys.argv[5]) != '-r' | str(sys.argv[7]) != '-q' | str(sys.argv[9]) != '-l'):
#        print('Please enter arguments in correct format')
#    elif(int(sys.argv[2]) <= 2049 | int(sys.argv[2]) >= 65536):
#       print('Please enter the correct sender port number')
#   elif(int(sys.argv[4]) <= 2049 | int(sys.argv[4]) >= 65536):
#       print('Please enter the correct requester port number')

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
def print_packet_information(requester_host_name, sequence_number, data_length, data):
    print("time packet is sent: ")
    print("IP address of requester: ", requester_host_name)
    print("sequence number: ", sequence_number)
    print("first 4 bytes of the payload: ", data[:4].decode("utf-8"))


check_sys_args()

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