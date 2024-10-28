import random
from partialhash import partialhash
from Crypto.Hash import SHA512
import argparse
import os
import time
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
clock0 = time.time()
clock1 = clock0
while clock1 - clock0 < 120:
    sha512_hash = SHA512.new(data)
    sha512_value = sha512_hash.hexdigest()
    clock1 = time.time()
load1, load5, load15 = os.getloadavg()
print("SHA512 - Load Average over the last 1 minute:",load1)
