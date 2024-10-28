import random
from partialhash import partialhash
import datetime
from Crypto.Hash import MD5
import argparse
parser = argparse.ArgumentParser(description='Efficiency Test of Data Integrity Verification with Dynamic Partial Hash Algorithm.')
parser.add_argument('file', type=str)
args = parser.parse_args()
file = open(args.file, "rb")
data = bytearray(file.read())
file.close()
data_size = len(data)
n = random.randint(3 + int(data_size / 10485760),  5 + int(data_size / 10485760))  #Average block size for large files: 1MB
max_partial_size = int(data_size / n * 2)
print("Calculating Hash value of", file.name)
clock0 = datetime.datetime.now()
for x in range(100):
    partial_param = partialhash.generatefinalhashquick(n, data, max_partial_size, data_size)
clock1 = datetime.datetime.now()
print("Time elapsed with partial hashing for 100 times:", clock1-clock0)
clock2 = datetime.datetime.now()
for x in range(100):
    md5_hash = MD5.new(data)
    md5_value = md5_hash.hexdigest()
clock3 = datetime.datetime.now()
print("Time elapsed with MD5 hashing for 100 times:", clock3-clock2)



