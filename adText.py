#!/usr/bin/python3
import os
#import sys

#sys.path.append("/mnt/ref/Python")
#import adFns

debugging = not True   #: turn on/off internal debugging msgs

def JustifyLine(txt, lnWidth, justify = "left"):
  justify = justify[0].lower()
  if justify == "l":
    return txt # default, do nowt, here is it is [probably] most likely to pass the rest of the choices for performance reasons

  if justify == "r":
    return (" " * (lnWidth - len(txt))) + txt

  elif justify == "c":
    return " " * int((lnWidth - len(txt)) / 2) + txt

  elif justify == "f":
    numWords = txt.count(" ")
    if numWords > 0:
      numSpcs = int((lnWidth - len(txt)) / numWords) + 1
      opLn = txt.replace(" ", " " * numSpcs)
      if len(opLn) < lnWidth:
        ptr = int(lnWidth / 2)
        opLn = opLn[0:ptr] + opLn[ptr:].replace(" ", "  ", 1)
      ptr = 0
      while len(opLn) < lnWidth:
        ptr += 1
        if ptr < len(opLn) and opLn[ptr] == " " and opLn[ptr+1] != " ":
         opLn = opLn[0:ptr] + " " + opLn[ptr:]
         ptr += 1
      return opLn
  return txt

def JustifyText(txt, lnWidth = os.get_terminal_size().columns, justify = "left"):
  origLn = txt
  indentLn = 0
  if origLn[0] in "-.o" and origLn[1] == " ":
    indentLn = 2
  justify = justify[0].lower()
  if debugging:
    print (("....:....|" * (int(lnWidth / 10) + 1))[0:lnWidth])
  rc = []
  opLn = ""
  numWords = 0
  ptr = origLn.find(" ")
  while origLn != "":
    if len(opLn) + (ptr if ptr > 0 else len(origLn)) > lnWidth:
      rc.append(JustifyLine(opLn, lnWidth, justify))
      opLn = (" " * indentLn) + origLn[1:ptr] if ptr > 0 else origLn[1:]
      numWords = 1
    else:
      opLn += origLn[0:ptr] if ptr >= 0 else origLn
      numWords += 1
    origLn = origLn[ptr:] if ptr > 0 else ""
    ptr = origLn.find(" ", 1)
  rc.append(opLn if justify == "f" and ((len(opLn) - opLn.count(" ")) < (lnWidth / 2)) else JustifyLine(opLn, lnWidth, justify))
  return rc
