import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_host = socket.gethostname()
udp_port = 12345

data = "Hello World! My name is Charmaine."
packet = data.encode()
print("UDP target IP: ", udp_host)
print("UDP target port: ", udp_port)

sock.sendto(packet, (udp_host, udp_port))