import json
MIN_LENGHT = 40
lines = open("all_methods.txt").readlines()
data = [json.loads(x) for x in lines]
data2 = [item for item in data if len(item) > MIN_LENGHT]

def split2line(l):
    split_token = [";", "{", "}"]
    result = []
    line = []
    for item in l:
        line.append(item)
        if item in split_token:
            result.append(line)
            line = []
    result.append(line)
    return result

data3 = [split2line(item) for item in data2]

def split2pair(l):
    result = []
    for i in range(1,len(l)):
        input = []
        for j in range(i):
            input += l[j]
        output = l[i]
        result.append((input,output))
    return result

data4 = []
for item in data3:
    data4 += split2pair(item)

f = open("pair_methods20000.txt", "w")
for item in data4[:20000]:
    json_str = json.dumps(item) + '\n'
    f.write(json_str)
pass