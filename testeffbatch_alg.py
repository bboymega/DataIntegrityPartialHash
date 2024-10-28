import random
from partialhash import partialhash
import datetime
from Crypto.Hash import MD5
import argparse
import os
import psutil
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
pid = os.getpid()
process = psutil.Process(pid)
memory_info = process.memory_info()
memory_usage_mb = memory_info.rss / (1024 * 1024)
load1, load5, load15 = os.getloadavg()
print("Time elapsed with partial hashing for 100 times:", clock1-clock0)
print("Load Average over the last 1 minute:",load1)
print(f"Memory usage: {memory_usage_mb:.2f} MB")
