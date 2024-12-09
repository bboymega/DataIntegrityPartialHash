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
output_filename = "/home/dev/output/output.txt"
output_file = open(output_filename, "a")
data_size = len(data)
n_avg = 0
count_avg = 0
count_pt_avg = 0
for x in range(100):
    n = random.randint(3 + int(data_size / 10485760), 5 + int(data_size / 10485760))  # Average block size for large files: 1MB
    n_avg += n
    m = random.randint(3 + int(data_size / 10485760), 5 + int(data_size / 10485760))
    count = 1
    print("Executing partial count guessing attack, File:", args.file, "Test:", x)
    while n != m:
        m = random.randint(3 + int(data_size / 10485760), 5 + int(data_size / 10485760))
        count = count + 1
    count_avg += count
    max_partial_size = int(data_size / n * 2)
    label_alg = partialhash.generatepartiallabel(n, max_partial_size, data_size)
    label_hack = partialhash.generatepartiallabel(m, max_partial_size, data_size)
    print("Executing partial label guessing attack, File:", args.file, "Test:", x)
    count_pt = 1
    while label_alg[0] != label_hack[0]:
        label_hack = partialhash.generatepartiallabel(m, max_partial_size, data_size)
        count_pt = count_pt + 1
    count_pt_avg += count_pt
count_avg = count_avg/100
count_pt_avg = count_pt_avg/100
n_avg = n_avg/100
print("File: "+ args.file, file=output_file)
print("It takes", count_avg, "attempt(s) to match the partial count", n_avg, file=output_file)
print("It takes", count_pt_avg, "attempt(s) to match the first element", file=output_file)
print("It takes approx", pow(count_pt_avg,n_avg), "attempt(s) to match all elements of the partial labels with the given partial count", file=output_file)
print("It takes approx", pow(count_pt_avg,n_avg)*count_avg, "attempt(s) to match all elements of the partial labels from scratch", file=output_file)
#output_file.write.close()