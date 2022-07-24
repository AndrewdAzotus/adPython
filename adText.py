#!/usr/bin/python3
import os
#import sys

#sys.path.append("/mnt/ref/Python")
#import adFns

debugging = not True   #: turn on/off internal debugging msgs
############################################################################################################

## returns the max idx of any of the characters in findChrs in the string in inText
def GetLastIdx(findChrs, inText, startPosn = 0, endPosn = None):
  if endPosn == None:
    endPosn = len(inText)
  idx = -1
  for chr in findChrs:
    idx = max(idx, inText.rfind(chr, startPosn, endPosn))
  return idx

def JustifyLine(txt, lnWidth = os.get_terminal_size().columns, justify = "left"):
  justify = justify[0].lower()
  numWords = txt.count(" ")
  if numWords == 0 or justify == "l":
    return txt # default, do nowt, left is [probably] most likely, so pass the rest of the choices for performance reasons

  if justify == "r":
    return (" " * (lnWidth - len(txt))) + txt

  if justify == "c":
    return " " * int((lnWidth - len(txt)) / 2) + txt

  if justify == "f":
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

def JustifyText(txt, lnWidth = os.get_terminal_size().columns, justify = "left", wordDelimiter = "", indentLn = None):
  origLn = txt
  justify = justify[0].lower()
  wordDelimiter = " {}".format(wordDelimiter)
  if indentLn == None:
    indentLn = 0
    if origLn[0] in "-.o" and origLn[1] == " ":
      indentLn = 2
  if debugging:
    print (("....:....|" * (int(lnWidth / 10) + 1))[0:lnWidth])
  rc = []
  opLn = ""
  ptr = GetLastIdx(wordDelimiter, origLn, endPosn = lnWidth)
  while origLn != "":
    if (len(opLn) + (ptr if ptr > 0 else len(origLn)) > lnWidth):
      startIdx = 1 if origLn[0] == " " else 0
      rc.append(JustifyLine(opLn, lnWidth, justify))
      opLn = (" " * indentLn) + (origLn[startIdx:ptr] if ptr > 0 else origLn[startIdx:])
    else:
      opLn += origLn[0:ptr] if ptr >= 0 else origLn
    origLn = origLn[ptr:] if ptr > 0 else ""
    ptr = GetLastIdx(wordDelimiter, origLn, 1, lnWidth)
  rc.append(opLn if justify == "f" and ((len(opLn) - opLn.count(" ")) < (lnWidth / 2)) else JustifyLine(opLn, lnWidth, justify))
  return rc
