import random
from Crypto.Hash import MD4
from Crypto.Hash import SHA256
from Crypto.Hash import MD5
import pickle
class partialhash:
    def getpartial(data, initial, terminal):
        return data[initial:terminal]

    def generatepartiallabel(n, max_partial_size, data_size):
        label = []
        label.append(random.randint(1, max_partial_size))
        for i in range(1,n-1):
            label.append(random.randint(1,max_partial_size)+label[i-1])
        label.append(data_size)
        return label

    def generatepartialdata(data, partial_label):
        label_size = len(partial_label)
        partial_data = []
        partial_data.append(partialhash.getpartial(data,0,partial_label[0]))
        for i in range(1,label_size):
            partial_data.append(partialhash.getpartial(data,partial_label[i-1],partial_label[i]))
        return partial_data

    def generateinstructiontag(n):
        instruction_tag = []
        for i in range(0,n):
            instruction_tag.append(random.randint(0,2))
        return instruction_tag

    def generatepartialhash(instruction_tag, partial_data):
        partial_hash = []
        partial_array_size = len(instruction_tag)
        for i in range (0,partial_array_size):
            if instruction_tag[i] == 0:
                sha256_hash = SHA256.new(partial_data[i])
                partial_hash.append(sha256_hash.hexdigest())
            else:
                if instruction_tag[i] == 1:
                    md4_hash = MD4.new(partial_data[i])
                    partial_hash.append(md4_hash.hexdigest())
                else:
                    if instruction_tag[i] == 2:
                        md5_hash = MD5.new(partial_data[i])
                        partial_hash.append(md5_hash.hexdigest())
        return partial_hash

    def generatefinalhashquick(n, data, max_partial_size, data_size):
        param = []
        label = []
        partial_data = []
        instruction_tag = []
        partial_hash = []
        finalhashstr = ''

        for i in range(0, n):
            if i == 0:
                label.append(random.randint(1, max_partial_size))
                partial_data.append(partialhash.getpartial(data, 0, label[0]))
            else:
                label.append(random.randint(1, max_partial_size) + label[i - 1])
                partial_data.append(partialhash.getpartial(data, label[i - 1], label[i]))
            if i == n-1:
                label.append(data_size)
            instruction_tag.append(random.randint(0, 2))
            if instruction_tag[i] == 0:
                sha256_hash = SHA256.new(partial_data[i])
                partial_hash.append(sha256_hash.hexdigest())
            else:
                if instruction_tag[i] == 1:
                    md4_hash = MD4.new(partial_data[i])
                    partial_hash.append(md4_hash.hexdigest())
                else:
                    if instruction_tag[i] == 2:
                        md5_hash = MD5.new(partial_data[i])
                        partial_hash.append(md5_hash.hexdigest())
            finalhashstr = finalhashstr + partial_hash[i]

        md5_hash = MD5.new(str.encode(finalhashstr))
        finalhash = md5_hash.hexdigest()
        param.append(pickle.dumps(label))
        param.append(pickle.dumps(partial_data))
        param.append(pickle.dumps(instruction_tag))
        param.append(pickle.dumps(partial_hash))
        param.append(finalhash.encode("utf-8"))
        return param

    def generatefinalhashquickserver(data, partial_label, instruction_tag):
        n = len(partial_label)
        partial_data = []
        partial_hash = []
        finalhashstr = ''
        for i in range(0, n):
            if i == 0:
                partial_data.append(partialhash.getpartial(data, 0, partial_label[0]))
            else:
                partial_data.append(partialhash.getpartial(data, partial_label[i - 1], partial_label[i]))
            if i < n-1:
                if instruction_tag[i] == 0:
                    sha256_hash = SHA256.new(partial_data[i])
                    partial_hash.append(sha256_hash.hexdigest())
                else:
                    if instruction_tag[i] == 1:
                        md4_hash = MD4.new(partial_data[i])
                        partial_hash.append(md4_hash.hexdigest())
                    else:
                        if instruction_tag[i] == 2:
                            md5_hash = MD5.new(partial_data[i])
                            partial_hash.append(md5_hash.hexdigest())
                finalhashstr = finalhashstr + partial_hash[i]

        md5_hash = MD5.new(str.encode(finalhashstr))
        finalhash = md5_hash.hexdigest()
        return finalhash

    def generatefinalhash(partial_hash):
        finalhashstr = ''
        for i in partial_hash:
            finalhashstr = finalhashstr + i
        md5_hash = MD5.new(str.encode(finalhashstr))
        finalhash = md5_hash.hexdigest()
        return finalhash
