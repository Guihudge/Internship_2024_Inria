import subprocess, os, math

nbrun = 1

numThread = 8

config = ""


for matSize in range(1000, 12000, 1000):
    envRun = os.environ.copy()
    subprocess.run('echo "[" > stat_{}.json'.format(matSize), env=envRun, shell=True)
    envRun["MKL_DEBUG_CPU_TYPE"] = "5"
    for i in range(nbrun):
        subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product {n} {m} {p} {blockSize} >> stat_{s}.json".format(n=matSize, m=matSize, p=matSize, blockSize=matSize/8, s=matSize), env=envRun, shell=True)
        subprocess.run('echo "," >> stat_{}.json'.format(matSize), env=envRun, shell=True)
    envRun["OMP_NUM_THREADS"] = "1"
    envRun["MKL-NUM_THREADS"] = "64"
    for i in range(nbrun):
        subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product {n} {m} {p} {blockSize} >> stat_{s}.json".format(n=matSize, m=matSize, p=matSize, blockSize=matSize, s=matSize), env=envRun, shell=True)
        subprocess.run('echo "," >> stat_{}.json'.format(matSize), env=envRun, shell=True)


    subprocess.run('echo "]" >> stat_{}.json'.format(matSize), env=envRun, shell=True)