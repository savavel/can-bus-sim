"""
 Python3 SSL server for connecting
 vehicle CAN Bus and Instrument Cluster

Created by: savavel
Last Edited: 10 May, 2018
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import socket
import time
import _thread
import json
import datetime
import ssl
import can

# Configure CAN bus parameters
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0'
can.rc['bitrate'] = 1000000

# Define can interface
bus = can.interface.Bus()

# Private and public key files
# for SSL auth
KEYFILE = '/home/pi/CanBusSim/privkey.pem'

CERTFILE = '/home/pi/CanBusSim/pubkey.pem'

# Set the hostname, portname
# and buffer size for the server
ic_host = '0.0.0.0'
ic_port = 8082
ic_buf = 1024


# CAN Bus Simulator server initialisation
ic_address = (ic_host, ic_port)
ic_socket = socket.socket(AF_INET, SOCK_STREAM)
ic_socket.bind(ic_address)
ic_socket.listen(1)
ic_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Specify SSL socket
ic_socket_ssl = ssl.wrap_socket(ic_socket, keyfile=KEYFILE,
                        certfile=CERTFILE, server_side=True)

"""
 This is not used anywhere
 Potentially allow receiving of messages from
 the Instrument Cluster Head Unit
"""
def ic_receiver(can_socket, can_address):
    while True:
        bin_data = can_socket.recv(ic_buf)
        data_utf8 = bin_data.decode("utf8").rstrip()
        if "disconnect" in data_utf8 or "" == data_utf8:
            print("disconnect")
            break
        data = data_utf8#json.loads(data_utf8)
        print(data)
        if "speed" in data:
            print('Speed')
            can_socket.send(json.dumps({"ackgnowledged": "speed"}).encode('utf-8'))
    can_socket.close()
    return

# Relay CAN Bus messages to the Instrument Cluster
# through an SSL socket
def can_sender(can_socket, bus):
    while True:
        message = bus.recv()
        arr = []
        for byte in message.data:
            arr.append(str(int(byte)))
        can_socket.send(json.dumps({"id": message.arbitration_id, "data": arr}).encode('utf-8'))

# Start the CAN bus server
# and relay the CAN messages to the instrument cluster
def can_server():
    while True:
        try:
            # accept ssl socket connections
            (can_socket, can_address) = ic_socket_ssl.accept()
            print('Got connection', can_socket, can_address)

            # potentially allow receiving messages from the Instrument Cluster head unit
            #thread_ic_receiver = _thread.start_new_thread(ic_receiver, (can_socket, can_address))

            # create CAN bus listener thread
            thread_can_sender = _thread.start_new_thread(can_sender, (can_socket, bus))
        except socket.error as e:
            print('Error: {0}'.format(e))

# Create the server thread
thread_can_server = _thread.start_new_thread(can_server, ())


# Keep application running 
while True:
    time.sleep(100)
