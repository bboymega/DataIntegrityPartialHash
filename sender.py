import random
from partialhash import partialhash
import socket
import pickle
import datetime
from md5hashcalc import md5hashcalc
import argparse
#from partialdataIO import
parser = argparse.ArgumentParser(description='Sender of Data Integrity Verification with Dynamic Partial Hash Algorithm.')
parser.add_argument('file', type=str)
parser.add_argument('host', type=str)
args = parser.parse_args()
file = open(args.file, "rb")
data = bytearray(file.read())
file.close()
data_size = len(data)
n = random.randint(3 + int(data_size / 10485760),  5 + int(data_size / 10485760))  #Average block size for large files: 10MB
max_partial_size = int(data_size / n * 2)
#partial_label = partialhash.generatepartiallabel(n, max_partial_size, data_size)
#partial_data = partialhash.generatepartialdata(data, partial_label)
#instruction_tag = partialhash.generateinstructiontag(n)
#partial_hash = partialhash.generatepartialhash(instruction_tag, partial_data)
#final_hash = partialhash.generatefinalhash(partial_hash)
print("Calculating Hash value of", file.name)
partial_param = partialhash.generatefinalhashquick(n, data, max_partial_size, data_size)

partial_label = pickle.loads(partial_param[0])
instruction_tag = pickle.loads(partial_param[1])
partial_hash = pickle.loads(partial_param[2])
final_hash = partial_param[3].decode("utf-8")

#print("Partial Label:", partial_label)
#print("Instruction Tag:", instruction_tag)
print("Calculated Final Hash:", final_hash)
#partialdataIO.savepartialdata('/Volumes/RAMDISK', partial_data, instruction_tag)

host = args.host
port = 15000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
try:
    data_send = []
    data_send.append(data)
    data_send.append(file.name.encode("utf-8"))
    data_send.append(pickle.dumps(partial_label))
    data_send.append(pickle.dumps(instruction_tag))
    data_send.append(final_hash.encode("utf-8"))
    serialized_data = pickle.dumps(data_send)
    data_size = len(serialized_data)
    client_socket.sendall(data_size.to_bytes(20, byteorder='big'))
    client_socket.sendall(serialized_data)
    size_bytes = client_socket.recv(20)
    data_size = int.from_bytes(size_bytes, byteorder='big')
    tmp_data = b""
    while len(tmp_data) < data_size:
        chunk = client_socket.recv(10485760)
        if not chunk:
            break
        tmp_data += chunk
    received_data = pickle.loads(tmp_data)
    integrity_stat = int.from_bytes(received_data[0], byteorder='big')
    final_hash_received = received_data[1].decode("utf-8")
    print("Received Final Hash From Peer:", final_hash_received)
    if (integrity_stat == 1):
        print("Data integrity has been verified.")
    else:
        print("Data integrity cannot be verified. It might have been modified by a third party.")
finally:
    client_socket.close()