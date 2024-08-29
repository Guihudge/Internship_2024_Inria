import os, subprocess, math

def divisorGenerator(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor

#Global var#
benchs_exec_path=[("srun /home/gdindart/composyx-private/build/src/driver/C++/composyx_distgemm", "-a 3 ", ""), ("srun chameleon_dtesting", "-o dgemm ", "")] #Executable, cmd option, env options
matrix_size=14000
BlockList=list(divisorGenerator(matrix_size))
minBlockSize = 401
nbRun = 2
envVar = ""

def Run(exec, execOption, blockSize, nbRun, envVar):
    command = "{env_var} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} ".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, env_var=envVar, execOption=execOption)
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
        resFileName = "/home/gdindart/multinode_bench/{}_multinode_big_matrix.csv".format(exec.split("/")[-1], execOpt.replace(" ", "_").replace("-",""))
        for bSize in BlockList:
            if bSize < minBlockSize:
                continue
            val = Run(exec, execOpt, bSize, nbRun, envVar+customEnv)
            writeVals(val, resFileName)

main()
