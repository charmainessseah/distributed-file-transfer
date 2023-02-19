from collections import defaultdict
from enum import Enum
import socket
import struct 

# printing information for each packet that arrives
# TODO: check packet type and print diff information if it is END packet
def print_receipt_information(header, data):
    print("time received: ")
    print("sender's IP address: ", sender_address[0], " sender's port: ", sender_address[1])
    print("packet type: ", header[0].decode('ascii'))
    print("sequence number: ", header[1])
    print("payload length: ", header[2])
    print("first 4 bytes of the payload: ", data[:4].decode("utf-8"))

# reads a text file and returns a list of strings
# each element represent each line in the text file
def read_and_parse_tracker_file(file_name):
    file = open(file_name, "r")
    file_lines = file.readlines()
    print(file_lines)

    # below is the nested dictionary format created
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
udp_port = 12345
sock.bind((udp_host, udp_port))


while True:
    print("Waiting for sender...")

    packet_with_header, sender_address = sock.recvfrom(1024)
    header = struct.unpack("!cII", packet_with_header[:9])
    data = packet_with_header[9:]

    print_receipt_information(header, data)