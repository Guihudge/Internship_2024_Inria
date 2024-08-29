import os, subprocess

#Global var#
benchs_exec_path=[("/home/guillaume/Documents/composyx-private/build/src/driver/C++/composyx_distgemm", "", ""), ("chameleon_dtesting", "-o gemm", " MKL_NUM_THREADS=1")]
matrix_size=2048
ThreadList=[1,2,4]
BlockList=[256,512,1024,2048]
hybridThList = [(2,2)] #mpi,omp
nbRun = 4
#envVar = "MKL_DEBUG_CPU_TYPE=5"
envVar = ""

def fullThreadRun(exec, execOption, blockSize, nbRun, nbThread, envVar):
    #./src/driver/C++/composyx_distgemm -m 2048 -n 2048 -k 2048 -b 256 -l 5 -t 8 --check-centr -H
    command = "{env_var} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t {nbThread}".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, nbThread=nbThread, env_var=envVar, execOption=execOption)
    print(command)
    res = subprocess.run(command, shell=True, capture_output=True)
    val = res.stdout.decode().splitlines()
    val = val[-nbRun:]
    return val

def fullMPIRun(exec, execOption, blockSize, nbRun, nbThread, envVar):
    #./src/driver/C++/composyx_distgemm -m 2048 -n 2048 -k 2048 -b 256 -l 5 -t 8 --check-centr -H
    command = "{env_var} mpirun -np {nbThread} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t 1".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, nbThread=nbThread, env_var=envVar, execOption=execOption)
    print(command)
    res = subprocess.run(command, shell=True, capture_output=True)
    val = res.stdout.decode().splitlines()
    val = val[-nbRun:]
    return val

def hybridRun(exec, execOption, blockSize, nbRun, ompThread, mpiThread, envVar):
    #./src/driver/C++/composyx_distgemm -m 2048 -n 2048 -k 2048 -b 256 -l 5 -t 8 --check-centr -H
    command = "{env_var} mpirun -np {mpiThread} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t {ompThread}".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, mpiThread=mpiThread, env_var=envVar, execOption=execOption, ompThread=ompThread)
    print(command)
    res = subprocess.run(command, shell=True, capture_output=True)
    val = res.stdout.decode().splitlines()
    val = val[-nbRun:]
    return val

def writeVals(vals, file):
    with open(file,"a") as f:
        for v in vals:
            f.write(v)
            f.write("\n")
#Run#

def main():
    #Full Thread
    for exec,execOpt,customEnv in benchs_exec_path:
        resFileName=  "{}_thread_only.csv".format(exec.split("/")[-1])
        for thread in ThreadList:
            for bSize in BlockList:
                val = fullThreadRun(exec, execOpt, bSize, nbRun, thread, envVar+customEnv)
                writeVals(val, resFileName)
        
        resFileName=  "{}_mpi_only.csv".format(exec.split("/")[-1])
        for thread in ThreadList:
            for bSize in BlockList:
                val = fullMPIRun(exec, execOpt, bSize, nbRun, thread, envVar+customEnv)
                writeVals(val, resFileName)
        
        resFileName=  "{}_hybrid.csv".format(exec.split("/")[-1])
        for mpiTh,ompTh in hybridThList:
            for bSize in BlockList:
                val = hybridRun(exec, execOpt, bSize, nbRun, ompTh, mpiTh, envVar+customEnv)
                writeVals(val, resFileName)

main()
