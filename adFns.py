#!/usr/bin/python3
import os
import sys

debugging = not True
from adText import print_justified

## This allows this file to display help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  print_justified("_adFns.py Help Information_")
  print ("")
  print ("General Purpose Functions that I could not find a better home for:")
  print (". AddDevPaths()")
  print (". GetValue()")
  print (". is_float()")
  print (". is_int()")
  print ("")
  print ("Planned Improvements:")
  print ("- ")
  sys.exit(0)

def GetValue(s):
  debugging = not True
  if (debugging):
    print ("Checking:", s)
  if (s == None or s == ""):
    if (debugging):
      print ("empty")
    return s
  if (s.lower() in ['true','false', 't','f', 'yes','no', 'y','n']):
    if (debugging):
      print ("bool")
    return (s.lower() in ['true', 't', 'yes', 'y'])
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
