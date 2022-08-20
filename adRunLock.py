#!/usr/bin/python3
import os
import sys

# ########################################################################## #
#
#   AAA          d                      d ''  AAA             t              #
#  A   A         d                      d  ' A   A           ttt             #
#  A   A         d       ee             d '  A   A            t         ss   #
#  AAAAA nnn   ddd  rrr e  e w   w    ddd    AAAAA zzzz  oo   t   u  u s     #
#  A   A n  n d  d r    eee  w   w   d  d    A   A   z  o  o  t   u  u  ss   #
#  A   A n  n d  d r    e    w w w   d  d    A   A  z   o  o  t   u  u    s  #
#  A   A n  n  ddd r     ee   w w     ddd    A   A zzzz  oo    tt  uuu  ss   #
#
# ########################################################################## #

sys.path.append("/mnt/ref/Python")
from adText import print_justified

## This allows this file to display help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  print_justified ("_adRunLock.py Help Information_")
  print_justified("Class to create a file in /run/lock/<name>.lock where <name> is, by default, the name of the calling program. Optionally another name may be used.")
  print ("")
  print_justified("_Usage_")
  print_justified("import adRunLock")
  print_justified(":")
  print_justified(":")
  print_justified("# To Initialise:")
  print_justified("runLockPgm = adRunLock.RunLock()")
  print_justified("if runLockPgm.isrunning():")
  print_justified("  raise 'Program is already running as pid {}'.format(runLockPgm.check())")
  print_justified("runLockPgm.set() # create a lock file and remember the pid")
  print_justified(":")
  print_justified("<your program>")
  print_justified(":")
  print_justified("runLockPgm.clear() # to remove the lock file")
  print ("")
  print_justified("Optionally, the lock file may be created with a specified name allowing the program to be run multiple times each with a different lock file name")
  sys.exit(0)

#############################################################################################
class RunLock:
  debugging   = not True
  runLockName = ""
  pid         = -1

  ## constructor: build the run lock file name from cmd args
  def __init__(this, lockName = ""):
    if (lockName == ""):
      lockName = os.path.split(sys.argv[0])[1]
    this.runLockName = r"/run/lock/{0}.lock".format(lockName)
    return

  ## checks if a runlock file is running and returns the pid of the executing process or None
  def check(this):
    print ("Run Lock File: ",this.runLockName)
    if (os.path.exists(this.runLockName)):
      print ("Lock File Exists.")
    return this.GetPid()

  ## remove the runlock file when it is finished with, e.g. as the calling pgm finishes execution
  def clear(this):
    if (os.path.exists(this.runLockName)):
      os.remove(this.runLockName)
      return "Cleared"
    return "Not Set"

  ## return the pid, enables the caller to confirm if it is the pgm to create the lock file
  def GetPid(this):
    if (os.path.exists(this.runLockName)):
      runLockFile = open(this.runLockName, "r")
      lines = runLockFile.readlines()
      runLockFile.close()
      this.pid = int(lines[0])
    return this.pid

  ## check to see if a lock file exists and reports its existance as an indication the the pgm is running
  def isrunning(this):
    return os.path.exists(this.runLockName)

  ## create a lock file and write the pid as the contents
  def set(this, override = False):
    if (not override and os.path.exists(this.runLockName)):
      raise Exception("Lock File {} already set, processing pid {}".format(this.runLockName, this.pid))
    this.pid = os.getpid()
    if (this.debugging):
      print ("Process Pid: {}".format(this.pid))
      print (r"/run/lock/{0}.lock".format(this.runLockName))
    runLockFile = open(this.runLockName, "w")
    runLockFile.write("{}".format(this.pid))
    runLockFile.close()
    return this.pid
