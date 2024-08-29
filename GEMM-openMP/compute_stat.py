import json

stat = json.load(open("stat_omp.json"))

compute = {}
init = {}
nb = {}

for e in stat:
    th = e["nbThread"]
    if th in compute:
        compute[th] += e["compute"]
        init[th] += e["init"]
        nb[th] +=1
    else:
        compute[th] = e["compute"]
        init[th] = e["init"]
        nb[th] = 1

for k in compute:
    compute[k] = compute[k] / nb[k]
    init[k]=  init[k] / nb[k]

print("Summary:")
for k in compute:
    print("\t- blockSize: {}, init: {}, compute: {}".format(k, init[k], compute[k]))