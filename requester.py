import sys
from enum import Enum
import socket
import struct 

#Global variables
udp_port = 12345

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
# TODO: check packet type and print diff information if it is END packet
def print_receipt_information(header, data):
    print("time received: ")
    print("sender's IP address: ", sender_address[0], " sender's port: ", sender_address[1])
    print("packet type: ", header[0].decode('ascii'))
    print("sequence number: ", header[1])
    print("payload length: ", header[2])
    print("first 4 bytes of the payload: ", data[:4].decode("utf-8"))

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
    #              sender_port: 12345
    #          }
    # }
    tracker_table =  {}

    for file_line in file_lines:
        words_in_line = file_line.split()
        curr_file_name = words_in_line[0]
        id = words_in_line[1]
        sender_host_name = words_in_line[2]
        sender_port = words_in_line[3]

        if curr_file_name not in tracker_table:
            tracker_table[curr_file_name] = {}
        if id not in tracker_table[curr_file_name]:
            tracker_table[curr_file_name][id] = {}

        tracker_table[curr_file_name][id]["sender_host_name"] = sender_host_name 
        tracker_table[curr_file_name][id]["sender_port"] = sender_port

    print(tracker_table)

read_and_parse_tracker_file("tracker.txt")

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_host = socket.gethostname()
sock.bind((udp_host, udp_port))

while True:
    print("Waiting for sender...")

    packet_with_header, sender_address = sock.recvfrom(1024)
    header = struct.unpack("!cII", packet_with_header[:9])
    data = packet_with_header[9:]

    print_receipt_information(header, data)