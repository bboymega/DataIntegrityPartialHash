import random
from partialhash import partialhash
import time
import argparse
import os
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
for x in range(10000):
    partial_param = partialhash.generatefinalhashquick(n, data, max_partial_size, data_size)
load1, load5, load15 = os.getloadavg()
print("Partial Hash - Load Average over 10000 times:",load1)
