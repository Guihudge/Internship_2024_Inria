import subprocess, os

nbrun = 10
envRun = os.environ.copy()
numThread = 8

config = ""
envRun["OMP_NUM_THREADS"] = "{}".format(numThread)
subprocess.run('echo "[" > stat.json', env=envRun, shell=True)
for i in range(nbrun):
    subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product >> stat.json", env=envRun, shell=True)
    subprocess.run('echo "," >> stat.json', env=envRun, shell=True)

envRun["OMP_NUM_THREADS"] = "4"
for i in range(nbrun):
    subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product >> stat.json", env=envRun, shell=True)
    subprocess.run('echo "," >> stat.json', env=envRun, shell=True)

envRun["OMP_NUM_THREADS"] = "1"
for i in range(nbrun):
    subprocess.run("/home/guillaume/Documents/produit_matriciel_omp/build_guix/product >> stat.json", env=envRun, shell=True)
    if (i != nbrun -1 ):
        subprocess.run('echo "," >> stat.json', env=envRun, shell=True)

subprocess.run('echo "]" >> stat.json', env=envRun, shell=True)