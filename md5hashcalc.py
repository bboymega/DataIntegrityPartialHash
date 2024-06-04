from Crypto.Hash import MD5
import datetime
file = open("/Volumes/RAMDISK/test.mp3", "rb")
data = file.read()
file.close()
clock0 = datetime.datetime.now()
md5_hash = MD5.new(data)
md5_value = md5_hash.hexdigest()
clock1 = datetime.datetime.now()
print("Time elapsed with MD5 hashing:", clock1-clock0)
print("Calculated MD5 Hash:", md5_value)