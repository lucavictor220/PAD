import socket
import struct

def send_unicast_message(message, ip, port):
    print("UDP target IP:", ip)
    print("UDP target port:", port)
    print("message:", message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message.encode('utf-8'), (ip, port))


def send_multicast_message(message, multicast_group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.5)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:
        print("Send message: {}".format(message))
        address = (multicast_group, port)
        sent = sock.sendto(message.encode('utf-8'), address)
        print("Message send!")
    except socket.timeout:
        print("Time out...")


send_multicast_message("Hello world, work hard and don\'t give up", '224.3.29.71', 10000)