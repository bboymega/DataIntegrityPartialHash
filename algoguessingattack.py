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
output_filename = "/home/dev/output/output_alg.txt"
output_file = open(output_filename, "a")
data_size = len(data)
count_avg = 0
for x in range(100):
    n = random.randint(3 + int(data_size / 10485760), 5 + int(data_size / 10485760))
    m = n
    print("Executing algorithm guessing attack, File:", args.file, "Test:", x)
    n_ins = partialhash.generateinstructiontag(n)
    m_ins = partialhash.generateinstructiontag(m)
    count = 1
    while n_ins != m_ins:
        m_ins = partialhash.generateinstructiontag(m)
        count = count + 1
    count_avg = count_avg + count
count_avg = count_avg / 100
print("File: "+ args.file, file=output_file)
print("It takes", count_avg, "attempt(s) to reproduce the instruction array", file=output_file)