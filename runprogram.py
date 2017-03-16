# import shlex
from subprocess import Popen, PIPE


def runprogram(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    # args = shlex.split(cmd)

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err
