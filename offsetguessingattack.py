import random
import argparse
from partialhash import partialhash
parser = argparse.ArgumentParser(description='Offset-guessing Attack Bench.')
parser.add_argument('file', type=str)
parser = argparse.ArgumentParser(description='Efficiency Test of Data Integrity Verification with Dynamic Partial Hash Algorithm.')
parser.add_argument('file', type=str)
args = parser.parse_args()
file = open(args.file, "rb")
data = bytearray(file.read())
file.close()
data_size = len(data)
n = random.randint(3 + int(data_size / 10485760),  5 + int(data_size / 10485760))  #Average block size for large files: 1MB
m = random.randint(3 + int(data_size / 10485760),  5 + int(data_size / 10485760))
count = 1
print("Executing partial count guessing attack...")
while n != m:
    m = random.randint(3 + int(data_size / 10485760), 5 + int(data_size / 10485760))
    count = count + 1
max_partial_size = int(data_size / n * 2)
label_alg = partialhash.generatepartiallabel(n,max_partial_size,data_size)
label_hack = partialhash.generatepartiallabel(m,max_partial_size,data_size)
print("Executing partial label guessing attack...")
count_pt = 1
while label_alg[0] != label_hack[0]:
    label_hack = partialhash.generatepartiallabel(m, max_partial_size, data_size)
    count_pt = count_pt + 1

print("It takes",count,"attempt(s) to match the partial count",n)
print("It takes",count_pt,"attempt(s) to match the first element")
print("It takes approx",pow(count_pt,n),"attempt(s) to match all elements of the partial labels with the given partial count")
print("It takes approx",pow(count_pt,n)*count,"attempt(s) to match all elements of the partial labels from scratch")