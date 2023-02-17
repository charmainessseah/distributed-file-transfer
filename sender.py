import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_host = socket.gethostname()
udp_port = 12345

data = "Hello World! My name is Charmaine.".encode()
print("UDP target IP: ", udp_host)
print("UDP target port: ", udp_port)

# assemble udp header
packet_type = 'R'.encode('ascii')
sequence_number = 1112
data_length = len(data) 
udp_header = struct.pack("!cII", packet_type, sequence_number, data_length)

packet_with_header = udp_header + data

sock.sendto(packet_with_header, (udp_host, udp_port))