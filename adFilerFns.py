#!/usr/bin/python3
import os
import shutil
import time

debugging = False

def CopyFile(fromPath, destPath, fileName, parms = {"timeDelay": 2.3, "verbose": 0}):
  fromFull = os.path.join(fromPath, fileName)
  if (parms["verbose"] > 1):
    print (" copying: {0}".format(fromFull))
    print ("      to: {0}".format(destPath))
    time.sleep(parms["timeDelay"])
  if (debugging):
    return
  if (not os.path.exists(destPath)):
    os.makedirs(destPath)
  shutil.copy(fromFull, destPath)
  destFull = os.path.join(destPath, fileName)
  shutil.copystat(fromFull, destFull)
  fromStat = os.stat(fromFull)
  os.chown(destFull, fromStat.st_uid, fromStat.st_gid)
  return

def MoveFile(fromPath, destPath, fileName, parms = {"timeDelay": 2.3, "verbose": 0}):
  fromFull = os.path.join(fromPath, fileName)
  destFull = os.path.join(destPath, fileName)
  if (os.path.exists(destFull)):
    os.remove(fromFull)
  return
