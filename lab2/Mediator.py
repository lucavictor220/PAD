import socket
import struct


def receive_message_unicast(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((ip, port))

    while True:
        print("waiting for message from nodes")
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("received message:", data.decode('utf-8'))

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
        receive_message_unicast("127.0.0.1", 5005)
    except socket.timeout:
        print("Time out...")


def receive_tcp_message(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    connection, addr = sock.accept()
    print('Connection address: {0} {1}', ip, port)
    while True:
        data = connection.recv(1024)
        if not data: break
        print("received data:".format(data.decode('utf-8')))
        connection.send(data)  # echo
        break
    sock.close()


def send_tcp_message(ip, port):
    message = "My data from node"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.timeout(0.5)
    try:
        sock.connect((ip, port))
    except sock.timeout:
        print("Can\'t connect... Exit")
    sock.send(message)
    sock.close()

send_multicast_message("Hello world, work hard and don\'t give up", '224.3.29.71', 10000)