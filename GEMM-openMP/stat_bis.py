import subprocess, os, math

nbrun = 1
envRun = os.environ.copy()
numThread = 8
matrixSize = 10000

def alldivisor(x, min=1):
    ret = []
    for i in range(min,x+1):
        if(x%i == 0):
            ret.append(i)
    return ret

divisor = alldivisor(matrixSize, 100)


print(divisor)

config = ""
envRun["OMP_NUM_THREADS"] = "4"
subprocess.run('echo "[" > stat.json', env=envRun, shell=True)
for blockSize in divisor:
    for i in range(nbrun):
        subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product {n} {m} {p} {blockSize} >> stat.json".format(n=matrixSize, m=matrixSize, p=matrixSize, blockSize=blockSize), env=envRun, shell=True)
        subprocess.run('echo "," >> stat.json', env=envRun, shell=True)


subprocess.run('echo "]" >> stat.json', env=envRun, shell=True)
