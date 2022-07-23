#!/usr/bin/python3

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
