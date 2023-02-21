import sys
from enum import Enum
import socket
import struct 

class Packet_Type(Enum):
    request = 'R'
    data = 'D'
    end = 'E'

#Checking the command line arguments
def check_sys_arg():
    if(len(sys.argv) != 5):
        print('Please enter the correct number of arguments')
    if(str(sys.argv[1]) != '-p' | str(sys.argv[3]) != '-o'):
        print('Please enter arguments in correct format')
    if(int(sys.argv[2]) <= 2049 | int(sys.argv[2]) >= 65536):
        print('Please enter the correct requester port number')
    global udp_port
    udp_port = sys.argv[2]

# printing information for each packet that arrives
def print_receipt_information(header, data):
    packet_type = header[0].decode('ascii')
    if (packet_type == 'D'):
        print('DATA Packet')
    elif (packet_type == 'E'):
        print('END Packet')

    print('send time: ')
    print('requester addr: ')
    print('sequence num: ', header[1])
    print('length: ', header[2])
    print('payload: ', data.decode("utf-8"))

# reads and parses tracker.txt into a nested dictionary
# details of nested dictionary are outlined below
def read_and_parse_tracker_file(file_name):
    try:
        file = open(file_name, "r")
    except:
        print('Please enter the correct file name!')
    
    file_lines = file.readlines()
    print(file_lines)

    # below is the structure of the nested dictionary
    # filename: {
    #          id: {
    #              sender_host_name: "some_host_name",
    #              sender_port_number: 12345
    #          }
    # }
    tracker_dict =  {}

    for file_line in file_lines:
        words_in_line = file_line.split()
        curr_file_name = words_in_line[0]
        id = int(words_in_line[1])
        sender_host_name = words_in_line[2]
        sender_port_number = words_in_line[3]

        if curr_file_name not in tracker_dict:
            tracker_dict[curr_file_name] = {}
        if id not in tracker_dict[curr_file_name]:
            tracker_dict[curr_file_name][id] = {}

        tracker_dict[curr_file_name][id]['sender_host_name'] = sender_host_name
        tracker_dict[curr_file_name][id]['sender_port_number'] = int(sender_port_number)

    print(tracker_dict)
    return tracker_dict

# send request packed with file name to the sender
def send_request_packet_to_sender(tracker_dict, file_name, id):
    data = file_name
    file_id_dict = tracker_dict[file_name]
    
    sender_host_name = file_id_dict[id]['sender_host_name']
    sender_port_number = file_id_dict[id]['sender_port_number']

    print(data, sender_host_name, sender_port_number)

#Global variables
udp_port = 12345

tracker_dict = read_and_parse_tracker_file('tracker.txt')

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_host = socket.gethostname()
sock.bind((udp_host, udp_port))

# request the senders for packets

# file_name = 'hello.txt'
# file_id_dict = tracker_dict[file_name]
# number_of_chunks_to_request = len(file_id_dict)

# for id in range(0, number_of_chunks_to_request):
#     send_request_packet_to_sender(tracker_dict, file_name, id + 1)

sender_host_name = socket.gethostname() # change this
sender_port_number = 12344 # change this

data = 'split.txt'.encode() # change this to the file name from input

# assemble udp header
packet_type = (Packet_Type.request.value).encode('ascii')
sequence_number = 1112
data_length = len(data)
udp_header = struct.pack('!cII', packet_type, sequence_number, data_length)

packet_with_header = udp_header + data

print('sending request to sender...')
sock.sendto(packet_with_header, (sender_host_name, sender_port_number))

# wait for requested packets from sender while the END packet has not been sent
while True:
    print('Waiting for the sender to send requested data back...')

    packet_with_header, sender_address = sock.recvfrom(1024)
    header = struct.unpack("!cII", packet_with_header[:9])
    data = packet_with_header[9:]

    print_receipt_information(header, data)

    packet_type = header[0].decode('ascii')
    if (packet_type == 'E'):
        break