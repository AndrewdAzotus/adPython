#!/usr/bin/python3
import os
import sys

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

