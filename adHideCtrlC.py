#!/usr/bin/python3
import os
import signal
import sys

sys.path.append("/mnt/ref/Python")
import adText

## This allows this file to dsiplay help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  for ln in adText.JustifyText("_adHideCtrlC.py Help Information_"):
    print (ln)
  print ("")
  for ln in adText.JustifyText("Absorbs Ctrl-C hiding the dump stack trace"):
    print (ln)
  sys.exit(0)

def handler(signum, frame):
  print ("\rAborting")
  exit(1)

signal.signal(signal.SIGINT, handler)
