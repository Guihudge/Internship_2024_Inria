import subprocess

# Global var#
benchs_exec_path = [("/home/gdindart/composyx-private/build/src/driver/C++/composyx_distgemm", "-a 2 ", ""), 
                    ("/home/gdindart/composyx-private/build/src/driver/C++/composyx_distgemm", "-a 1 ", "")] # Executable, cmd option, env options
matrix_size = 4096
ThreadList = [2, 4, 6, 12, 16, 20, 24]
BlockList = [256, 512, 1024, 2048]
nbRun = 1
envVar = ""


def optimalP(n):
    q = 1
    for i in range(1, n):
        if n % i == 0:
            q = i
        if q * q >= n:
            break
    return q

def fullThreadRun(exec, execOption, blockSize, nbRun, nbThread, envVar):
    command = "{env_var} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t {nbThread}".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, nbThread=nbThread, env_var=envVar, execOption=execOption)
    print(command)
    res = subprocess.run(command, shell=True, capture_output=True)
    val = res.stdout.decode().splitlines()
    val = val[-nbRun:]
    return val


def fullMPIRun(exec, execOption, blockSize, nbRun, nbThread, envVar):
    command = "{env_var} mpirun -np {nbThread} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t 1".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, nbThread=nbThread, env_var=envVar, execOption=execOption)
    print(command)
    res = subprocess.run(command, shell=True, capture_output=True)
    val = res.stdout.decode().splitlines()
    val = val[-nbRun:]
    return val


def hybridRun(exec, execOption, blockSize, nbRun, ompThread, mpiThread, envVar):
    command = "{env_var} mpirun --bind-to none -np {mpiThread} {exec} {execOption} -m {size} -n {size} -k {size} -b {blockSize} -l {nbRun} -t {ompThread}".format(exec=exec, size=matrix_size, nbRun=nbRun, blockSize=blockSize, mpiThread=mpiThread, env_var=envVar, execOption=execOption, ompThread=ompThread)
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


# Run#
def main():
    # Full Thread
    for exec, execOpt, customEnv in benchs_exec_path:
        resFileName = "{}_mpi_only.csv".format(exec.split("/")[-1])
        for thread in ThreadList:
            for bSize in BlockList:
                exeOptRun = ""
                p = optimalP(thread)
                if execOpt == "-a 2 ":
                    exeOptRun = execOpt + "--debug_comm_output commRes/{}_{}_{}_2_{}.csv -P {}".format(matrix_size, bSize, thread,p,p)
                else:
                    exeOptRun = execOpt + "--debug_comm_output commRes/{}_{}_{}_1_{}.csv -P {}".format(matrix_size, bSize, thread,p,p)
                val = fullMPIRun(exec, exeOptRun, bSize, nbRun, thread, envVar+customEnv)
                writeVals(val, resFileName)


main()