from partialhash import partialhash
import socket
import pickle
import ntpath
from pathlib import Path
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 15000
server_socket.bind((host, port))
server_socket.listen(1)
import argparse
parser = argparse.ArgumentParser(description='Receiver of Data Integrity Verification with Dynamic Partial Hash Algorithm.')
parser.add_argument('path', type=str)
args = parser.parse_args()
file_path = args.path
while True:
    connection, client_address = server_socket.accept()
    try:
        print(f"Connection from",client_address[0]+":"+str(client_address[1]))
        size_bytes = connection.recv(20)
        if not size_bytes:
            break
        data_size = int.from_bytes(size_bytes, byteorder='big')
        tmp_data = b""
        print("\rReceiving data from client",client_address[0]+":"+str(client_address[1]),"(0%)",end='',flush=True)
        while len(tmp_data) < data_size:
            chunk = connection.recv(10485760)
            if not chunk:
                break
            tmp_data += chunk
            print("\rReceiving data from client",client_address[0]+":"+str(client_address[1]), "("+str(int(len(tmp_data)/data_size*100))+"%)",end='',flush=True)
        received_data = pickle.loads(tmp_data)
        data = received_data[0]
        print("\nReceived",len(received_data[0]),"bytes from client. Verifying integrity...")
        filename = received_data[1].decode("utf-8")
        partial_label = pickle.loads(received_data[2])
        instruction_tag = pickle.loads(received_data[3])
        final_hash = received_data[4].decode("utf-8")
        n = len(partial_label)

        print("Partial Label:", partial_label)
        print("Instruction Tag:", instruction_tag)
        print("Received Final Hash From Peer:", final_hash)

        #partial_data = partialhash.generatepartialdata(data, partial_label)
        #partial_hash = partialhash.generatepartialhash(instruction_tag, partial_data)
        #final_hash_server = partialhash.generatefinalhash(partial_hash)

        final_hash_server = partialhash.generatefinalhashquickserver(data, partial_label, instruction_tag)
        print("Calculated Final Hash:" ,final_hash_server)
        integrity_stat = 0
        if (final_hash_server == final_hash):
            integrity_stat = 1
            path = Path(file_path + ntpath.basename(filename))
            path.parent.mkdir(parents=True, exist_ok=True)
            print("Data integrity has been verified. Saving File as", file_path + ntpath.basename(filename))
            output_file = open(file_path + ntpath.basename(filename), "wb")
            output_file.write(received_data[0])
            output_file.close()
        else:
            print("Data integrity cannot be verified. It might have been modified by a third party.")

        data_send = []
        data_send.append(integrity_stat.to_bytes(4, byteorder='big'))
        data_send.append(final_hash_server.encode("utf-8"))
        serialized_data = pickle.dumps(data_send)
        data_size = len(serialized_data)
        connection.sendall(data_size.to_bytes(20, byteorder='big'))
        connection.sendall(serialized_data)

    finally:
        connection.close()
