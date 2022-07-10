#!/usr/bin/python3
import os
import sys

def GetValue(s):
  debugging = not True
  if (debugging):
    print ("Checking:", s)
  if (s == None or s == ""):
    if (debugging):
      print ("empty")
    return s
  if (s.lower() in ['true','false', 't','f', 'yes','no', 'y','n', 'up','down', 'u','d']):
    if (debugging):
      print ("bool")
    return (s.lower() in ['true', 't', 'yes', 'y', 'up', 'u'])
  try:
    if (debugging):
      print ("int")
    return int(s)
  except ValueError:
    pass
  try:
    if (debugging):
      print ("float")
    return float(s)
  except:
    if (debugging):
      print ("string")
    return s

def is_float(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

###################################################################################################
###################################################################################################
###################################################################################################
def ProcessParms(parms, setRunLock = False):
# description: processes sys.args into parms                                                      #
# usage: parms = ProcessParms(parms, <True|False>)                                                #
# Parameter Arguments:
# 1] parms      - a dictionary of variable names and command arguments
# 2] setRunLock - boolean, when true create a file /run/lock/<cmdname>.lock
#                 containing the run time pid. It is up to the caller to check
#                 and use the file as appropriate to the program
#
#     Initialise the dictionary with keys and values
#       the key is the name of the parm to be used in the calling program
#       the value consists of: <arg command>,... (:<default value>)
#                              <arg command>,... (:[<default option>,<option>,...])
#     when a list of values is specified after the : in square brackets then the arg after
#          arg cmd must be one of those values and if not then the value returned is None
#          if the arg cmd is not specified then the first item in the list is the default value
#
# parms example:
#  create parms in calling program thus:
#     parms = { }
#     parms["verbose"]   = "v,verbose"            #- will be True if specified on cmd line        #
#                                                    or False if not                              #
#     parms["runlevel"]  = "r,runlvl,runlevel:3"  #- set to the arg after -r --runlvl or          #
#                                                    --runlevel, or 3 if not specified
#     parms["catchparm"] = ""
#     parms["catchall"]  = []
#     parms["testingx"]  = "x:[a,b,c]"
#
#  call program thus:
#  1] python-pgm -v -runlvl 4 a b c d e f
#   parms will become:
#     parms["verbose"]   = True       ##- 
#     parms["runlevel"]  = "4"        ##
#     parms["catchparm"] = "f"        ##
#     parms["catchall"]  = ["a", "b", "c", "d", "e"]
#     parms["testingx"]  = "a"
#
#  2] python-pgm -runlvl:47 -x:b
#   parms will become:
#     parms["verbose"] = False
#     parms["runlevel"] = "47"
#     parms["catchparm"] = ""
#     parms["catchall"] = []
#     parms["testingx"]  = "b"
#
#  3] python-pgm -v p q
#   parms will become:
#     parms["verbose"] = True
#     parms["runlevel"] = "3"
#     parms["catchparm"] = "q"
#     parms["catchall"] = ["p"]
#     parms["testingx"]  = "a"        ##
#
#  4] python-pgm thingy -x f
#   parms will become:
#     parms["verbose"]   = False      ##
#     parms["runlevel"]  = "3"        ##
#     parms["catchparm"] = "thingy"   ##
#     parms["catchall"]  = []         ##
#     parms["testingx"]  = None       ##-- because the -x arg is not in the list of a,b,c
#
#   Within the dictionary, the key is the parm name for use within the calling program
#   On calling ProcessParms, the value contains definitions for the calling args, where
#     arg names separated by commas
#     if there is no colon : in the value then this returned with a true/false boolean value
#     NOTE: boolean falgs cannot have defaults. Optionally, this could be post processed
#           using a logical and/or with the returned value
#     if there is a : then the argument following the cmd arg is placed in the value, see runlevel above
#         any value after the : is the default if not specified on the calling args, see runlevel on example 3
#     if there is an empty string in the incoming value then it is filled with the last arg not following a command
#     all preceeding args not related to a command arg are placed in a supplied list [see catchall above]
#
# Improvements:
# - be able to call as ProcessParms(parms, <True|False>) without the assignment
#
  debugging = not True
  rc = {}
  catchParm = None
  catchList = None
  for parm in parms:
    if (isinstance(parms[parm], str)):
      if (parms[parm] == ""):
        catchParm = parm
      else:
        parms[parm] = ",{}".format(parms[parm].replace(":",",:"))
        if (parms[parm].find(":") == -1):
          parms[parm] += ","
    elif (isinstance(parms[parm], list)):
      catchList = parm
    if (debugging):
      print ("parm: {} .. value: {}".format(parm, parms[parm]))
  if (debugging):
    print ()
  pgm = ""
  cmd = None
  if (debugging):
    print (sys.argv)
    for arg in sys.argv:
      print ("arg: {0}".format(arg))
    print ()
  for arg in sys.argv:
    if (arg == sys.argv[0]):
      if (setRunLock):
        pid = os.getpid()
        if (debugging):
          print ("Process Pid: {}".format(pid))
        runLockName = r"/run/lock/{0}.lock".format(os.path.split(arg)[1])
        runLockFile = open(runLockName, "w")
        runLockFile.write("{}".format(pid))
        runLockFile.close()
      continue
    if (debugging):
      print ("checking arg: {}".format(arg))
    if (arg[0:1] == "-"):
      cmd = arg.replace("-", "").lower()
      arg = None
      if (cmd.find(":") > 0):
        arg = cmd[cmd.find(":") + 1 : ]
        cmd = cmd[0 : cmd.find(":")]
      cmd = ",{},".format(cmd)
    if (debugging):
      print ("cmd: {0} .. arg: {1}".format(cmd, arg))
    for parm in parms:
      if (isinstance(cmd, str)):
        if debugging:
          print ("cmd is string", cmd	)
        if (isinstance(parms[parm], str) and cmd in parms[parm]):
          if debugging:
            print("parms[parm]", parms[parm])

          ## no optional values, so must be bool flag
          if parms[parm].find(":") == -1:
            if debugging:
              print ("Setting {} to True".format(parm))
            rc[parm] = True
            cmd = None

          else:
            ## assign a parm with a value
            if arg == None: ## not ready yet
              continue
            ## must passed arg be one of a list of allowable options
            if (parms[parm][-1] == "]"):
              parmOptions = parms[parm][parms[parm].find("[")+1:-1]
              parmOptList = parmOptions.split(",")
              if (debugging):
                print ("List Options Debug:")
                print ("  cmd        : ", cmd)
                print ("  parm name  : ", parm)
                print ("  parm value : ", parms[parm])
                print ("  arg        : ", arg)
                print ("  parmOptions: ", parmOptions)
                print ("  parmOptList: ", parmOptList)
              if (arg in parmOptList):
                rc[parm] = GetValue(arg)
              else:
                rc[parm] = None
            else:
              rc[parm] = GetValue(arg)
            cmd = None
          arg = None

# fill unassigned parm to catch alls
    if (cmd == None and arg != None):
      if (debugging):
        print ("cmd+arg", cmd, arg)
      if (catchParm != None):
        if (catchList != None and parms[catchParm] != ""):
          parms[catchList].append(parms[catchParm])
          if (debugging):
            print ("catchList", parms[catchList])
        if (debugging):
          print ("Assigning catchparm to", arg)
        parms[catchParm] = arg
        arg = None

# remove all of the already processed parms
  for parm in rc:
    parms.pop(parm)

# copy catchParm to parms being returned
  if (catchParm != None and parms[catchParm] != None):
    if (debugging):
      print ("Assigning catchparm to", parms[catchParm])
    rc[catchParm] = parms[catchParm]
    parms.pop(catchParm)

# copy catchList to parms being returned
  if (catchList != None and parms[catchList] != None):
    rc[catchList] = parms[catchList]
    parms.pop(catchList)

# copy any remaining unspecified parms to parms being returned
  for parm in parms:
    if (isinstance(parms[parm], str) and parms[parm].find(',:[') > 0 and parms[parm][-1] == "]"):
      parmOptions = parms[parm][parms[parm].find("[")+1:-1]
      rc[parm] = parmOptions.split(",")[0]
    elif (isinstance(parms[parm], str) and parms[parm].find(',:') > 0):
      rc[parm] = GetValue(parms[parm][parms[parm].find(":") + 1:])
    else:
      rc[parm] = False
  return rc

#############################################################################################
#############################################################################################
#############################################################################################
class RunLock:
  debugging   = not True
  runLockName = ""
  pid         = -1
  
  def __init__(this, lockName = ""):
    if (lockName == ""):
      lockName = os.path.split(sys.argv[0])[1]
    this.runLockName = r"/run/lock/{0}.lock".format(lockName)
    return
  
  def check(this):
    print ("Run Lock File: ",this.runLockName)
    if (os.path.exists(this.runLockName)):
      print ("Lock File Exists.")
    return this.GetPid()
  
  def clear(this):
    if (os.path.exists(this.runLockName)):
      os.remove(this.runLockName)
      return "Cleared"
    return "Not Set"
  
  def GetPid(this):
    if (os.path.exists(this.runLockName)):
      runLockFile = open(this.runLockName, "r")
      lines = runLockFile.readlines()
      runLockFile.close()
      this.pid = int(lines[0])
    return this.pid
  
  def isrunning(this):
    return os.path.exists(this.runLockName)
  
  def set(this):
    if (os.path.exists(this.runLockName)):
      raise Exception("Lock File {} already set".format(this.runLockName))
    this.pid = os.getpid()
    if (debugging):
      print ("Process Pid: {}".format(this.pid))
      print (r"/run/lock/{0}.lock".format(this.runLockName))
    runLockFile = open(this.runLockName, "w")
    runLockFile.write("{}".format(this.pid))
    runLockFile.close()
    return this.pid
