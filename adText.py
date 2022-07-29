#!/usr/bin/python3
import os
import sys
import time

######################################################################################
debugging = not True #: turn on/off internal debugging msgs
version = "2.03.011" #: JustifyText now allows a string to indent following lines by
######################################################################################
## This allows this file to display help, but only if executed directly:
## moved to end of file so the help text information can use itself...
#if os.path.basename(__file__) in sys.argv[0]:
# ...
######################################################################################

def JustifyLine(txt, lnWidth = None, justify = "left"):
  if lnWidth == None:
    try:
      lnWidth = os.get_terminal_size().columns
    except:
      lnWidth = 9999
  justify = justify[0].lower()
  numWords = txt.count(" ")
  if numWords == 0 and justify == "l":
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

############################################################################################
def JustifyText(txt, lnWidth = None, justify = "left", wordDelimiter = "", indentLn = None):
  if lnWidth == None:
    try:
      lnWidth = os.get_terminal_size().columns
    except:
      lnWidth = 9999
  txt = str(txt)
  if len(txt) < lnWidth:
    if len(txt) > 0 and txt[0] == txt[-1] == "_":
      return [ txt[1:-1], "-" * (len(txt) - 2) ]
    return [ txt ]

  origLn = txt
  justify = justify[0].lower()
  wordDelimiter = " {}".format(wordDelimiter)
  indentTxt = '' if justify == "f" else " "
  if indentLn == None:
    indentLn = 0
    if origLn[0] in "-.o" and origLn[1] == " ":
      indentLn = 2
  elif type(indentLn) is str:
    indentTxt = indentLn
    indentLn = 1

  if debugging:
    print (("....:....|" * (int(lnWidth / 10) + 1))[0:lnWidth])

  indentPfx = ""
  rc = []
  opLn = ""
  underlng = False
  while origLn != "":
    indentSz = len(indentPfx)
    startIdx = 1 if origLn[0] == " " else 0
    opLn = (indentPfx + origLn[startIdx:])
    if len(opLn) > lnWidth:
      ptr = -1
      for chr in wordDelimiter:
        ptr = max(ptr, opLn.rfind(chr, 0, lnWidth))
      opLn = opLn[0:ptr]
      origLn = origLn[(len(opLn) + startIdx - indentSz):]
    else:
      origLn = ""
    rc.append(JustifyLine(opLn, lnWidth, justify))
    indentPfx = indentTxt * indentLn
  return rc

## The best way to use this next function is:
# from adText import print_justified
## then, instead of print ( ... ), use
# print_justified ( ... )
def print_justified(txt = '', lnWidth = None, justify = "left", wordDelimiter = "", indentLn = None):
  for ln in JustifyText(txt, lnWidth, justify, wordDelimiter, indentLn):
    print (ln)
  return

if os.path.basename(__file__) in sys.argv[0]:
  print_justified ("_adText.py Help Information_")
  print_justified ("The purpose of this is to print text but in such a way that words are not broken across lines and are word wrapped correctly and uses the following functions:")
  print_justified (". JustifyLine()")
  print_justified (". JustifyText()")
  print_justified (". print_justified() -- from adText import print_justified")
  print_justified ()
  print_justified ("_JustifyLine()_")
  print_justified ("Takes a single line of text and returns a justified text. The four justification choices are left, right, center or full")
  print_justified ('')
  print_justified ("_JustifyText()_")
  print_justified ("Takes text and breaks it down into multiple lines based on lnWidth then calls JustifyLine() to justify each line and returns a list of justified lines of text")
  print_justified ('')
  print_justified ("_print_justified()_")
  print_justified ("By using the following import command:")
  print_justified ('')
  print_justified ("from adText import print_justified")
  print_justified ('')
  print_justified ("then you can use print_justified() as a near drop in replacement for print() with different parms")
  print_justified ()
  print_justified ("The following parms are applicable to all functions:")
  print_justified ("o txt = '' - the first parm is the object to be printed.")
  print_justified ("o lnWidth = None - the maximum width to format the text to, defaults to terminal size is not specified")
  print_justified ("o justify = 'left' - how to justify the supplied text, choices are left, right, centre and full")
  print_justified ("o wordDelimiter = '' - separator to use when breaking text. space is always added to this parm. If printing file paths, for example, pass in '//' to separate the text at both spaces and directory separators.")
  print_justified ("o indentLn = None - indent 2nd line onward by an indentation. If this is a number then indent lines by n spaces. If this is some text then indent line by that text e.g. '... ' to start lines 2 onward with ... ")
  print_justified ('')
  print_justified ("Improvements:")
  print_justified ("- allow pass through of the following parms in print():")
  print_justified (". sep='separator' - Optional. Specify how to separate the objects, if there is more than one. Default is ' '", indentLn=20)
  print_justified (". end='end'       - Optional. Specify what to print at the end. Default is '\\n' (line feed)", indentLn=20)
  print_justified (". file            - Optional. An object with a write method. Default is sys.stdout", indentLn=20)
  print_justified (". flush           - Optional. A Boolean, specifying if the output is flushed (True) or buffered (False). Default is False", indentLn=20)
  print_justified ('')
  print_justified ("Test output line for print_justified: {} things make up stuff as {:2.2%} percentage... on lnWidth then calls JustifyLine() to justify each line and returns a list of justified lines of text. Takes text and breaks it down into multiple lines based on lnWidth then calls JustifyLine() to justify each line and returns a list of justified lines of text. Takes text and breaks it down into multiple lines based on lnWidth then calls JustifyLine() to justify each line and returns a list of justified lines of text".format(11, 23 / 137))
  print_justified ("")
