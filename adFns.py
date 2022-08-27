#!/usr/bin/python3
import os, sys
# ########################################################################## #
#                                                                            #
#   AAA          d                      d ''  AAA             t              #
#  A   A         d                      d  ' A   A           ttt             #
#  A   A         d       ee             d '  A   A            t         ss   #
#  AAAAA nnn   ddd  rrr e  e w   w    ddd    AAAAA zzzz  oo   t   u  u s     #
#  A   A n  n d  d r    eee  w   w   d  d    A   A   z  o  o  t   u  u  ss   #
#  A   A n  n d  d r    e    w w w   d  d    A   A  z   o  o  t   u  u    s  #
#  A   A n  n  ddd r     ee   w w     ddd    A   A zzzz  oo    tt  uuu  ss   #
#                                                                            #
# ########################################################################## #
debugging = not True #
version = "1.01.001" #
# ################## # ########### #
from adIntFns import AppendToSysPath #
AppendToSysPath("/mnt/ref/Python") #
from adText import print_justified #
# ################################ #

## This allows this file to display help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  print_justified("_adFns.py Help Information_")
  print ("")
  print ("General Purpose Functions that I could not find a better home for:")
  print (". GetValue(any-value)")
  print (". HumanTime(seconds)")
  print (". is_float(number)")
  print (". is_int(number)")
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

def HumanTime(s):
  rc = ""
  d = 0
  h = 0
  m = 0

  if s > 59:
    m = int(s / 60)
    s = s % 60
  if m > 59:
    h = int(m / 60)
    m = m % 60
  if h > 23:
    d = int(h / 24)
    h = h % 24

  if d > 0:
    rc += "{0:,} day{1}".format(d, "s" if d > 1 else "")
  if rc != "" and h + m + s > 0:
    rc += ", " if h > 0 or m > 0 or s > 0 else " and "
  if h > 0:
    rc += "{0:,} hour{1}".format(h, "s" if h > 1 else "")
  if rc != "" and m + s > 0:
    rc += ", " if m > 0 and s > 0 else " and "
  if m > 0:
    rc += "{0:,} minute{1}".format(m, "s" if m > 1 else "")
  if rc != "" and s > 0:
    rc += " and "
  if s > 0:
    rc += "{0:,} second{1}".format(s, "s" if s > 1 else "")
  return rc

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
