#!/usr/bin/python3
import os
import sys

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def is_float(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def GetValue(s):
  if (s.lower() in ['true','false', 't','f', 'yes','no', 'y','n', 'up','down', 'u','d']):
    #print ("bool")
    return (s.lower() in ['true', 't', 'yes', 'y', 'up', 'u'])
  try:
    #print ("int")
    return int(s)
  except ValueError:
    pass
  try:
    #print ("float")
    return float(s)
  except:
    #print ("string")
    return s

def ProcessParms(parms, setRunLock = True):
# description: processes sys.args into parms
# usage: parms = ProcessParms(parms, <True|False>)
# Parameter Arguments:
# 1] parms      - a dictionary of variable names and command arguments
# 2] setRunLock - boolean, when true create a file /run/lock/<cmdname>.lock
#                 containing the run time pid. It is up to the caller to check
#                 and use the file as appropriate to the program
#
# parms example:
#  create parms in calling program thus:
#     parms = { }
#     parms["verbose"] = "v,verbose"
#     parms["runlevel"] = "r,runlvl,runlevel:3"
#     parms["catchparm"] = ""
#     parms["catchall"] = []
#
#  call program thus:
#  1] python-pgm -v -runlvl 4 a b c d e f
#   parms will become:
#     parms["verbose"] = True
#     parms["runlevel"] = "4"
#     parms["catchparm"] = "f"
#     parms["catchall"] = ["a", "b", "c", "d", "e"]
#
#  2] python-pgm -runlvl:47
#   parms will become:
#     parms["verbose"] = False
#     parms["runlevel"] = "47"
#     parms["catchparm"] = ""
#     parms["catchall"] = []
#
#  3] python-pgm -v p q
#   parms will become:
#     parms["verbose"] = True
#     parms["runlevel"] = "3"
#     parms["catchparm"] = "q"
#     parms["catchall"] = ["p"]
#
#  4] python-pgm thingy
#   parms will become:
#     parms["verbose"] = False
#     parms["runlevel"] = "3"
#     parms["catchparm"] = "thingy"
#     parms["catchall"] = []
#
#   The key is the parm name for use within the calling program
#   On calling ProcessParms, the value contains definitions for the calling args, where
#     arg names separated by commas
#     if there is no colon : in the value then this returned with a true/false boolean value
#     if there is a : then the argument following the cmd arg is placed in the value, see runlevel above
#         any value after the : is the default if not specified on the calling args, see runlevel on example 3
#     if there is an empty string in the incoming value then it is filled with the last arg not following a command
#     all preceeding args not related to a command arg are placed in a supplied list [see catchall above]
#
# Improvements:
# - be able to call as ProcessParms(parms, <True|False>) without the assignment
  debugging = False
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
        if (isinstance(parms[parm], str) and cmd in parms[parm]):
          if parms[parm].find(":") == -1: # bool flag
            rc[parm] = True
            cmd = None
          else:
            if arg == None:
              continue
            rc[parm] = GetValue(arg)
            cmd = None
          arg = None
    if (cmd == None and arg != None): # fill unassigned parm to catch alls
      if (debugging):
        print ("cmd+arg", cmd, arg)
      if (catchParm != None):
        if (catchList != None and parms[catchParm] != ""):
          parms[catchList].append(parms[catchParm])
          if (debugging):
            print ("catchList", parms[catchList])
        parms[catchParm] = arg
        arg = None
  for parm in rc:
    parms.pop(parm)
  if (catchParm != None and parms[catchParm] != None):
    rc[catchParm] = parms[catchParm]
    parms.pop(catchParm)
  if (catchList != None and parms[catchList] != None):
    rc[catchList] = parms[catchList]
    parms.pop(catchList)
  for parm in parms:
    if (isinstance(parms[parm], str) and parms[parm].find(',:') > 0):
      rc[parm] = GetValue(parms[parm][parms[parm].find(":") + 1:])
    else:
      rc[parm] = False
  return rc
