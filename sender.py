import random
from partialhash import partialhash
from partialdataIO import partialdataIO
n = random.randint(2,10)
file = open("/Volumes/RAMDISK/test.mp3", "rb")
data = file.read()
file.close()
max_partial_size = int(len(data) / n * 2)
data_size = len(data)
partial_label = partialhash.generatepartiallabel(n, max_partial_size, data_size)
partial_data = partialhash.generatepartialdata(data, partial_label)
print(n)
instruction_tag = partialhash.generateinstructiontag(n)
partial_hash = partialhash.generatepartialhash(instruction_tag, partial_data)
print(instruction_tag)
print(partial_hash)
#partialdataIO.savepartialdata('/Volumes/RAMDISK', partial_data, instruction_tag)