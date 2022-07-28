#!/usr/bin/python3
import os
import sys
import time

sys.path.append("/mnt/ref/Python")
import adFns
import adText

debugging = not True #: turn on/off internal debugging msgs

## This allows this file to dsiplay help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  print ("adCmdOpts.py Help Information")
  print ("-----------------------------")
  print ()
  print ("_IsHelp(text, suffix)_")
  helpText = "Returns True if text starts with 'help' or if text starts with 'help'+suffix, False otherwise. This is case insensitive and is primarily used to differentiate between parm args and help information in ProcessParms() and DisplayHelp()."
  for ln in adText.JustifyText(helpText):
    print (ln)
  print ()
  print (adText.JustifyText("_DisplayHelp()_"))
  helpText = "Uses the same parms as ProcessParms() plus the program name which is collected automatically from sys.argv[0]. The argument options are extracted from the parms as is the help text and any default values. These are formatted and output to the user using adText.JustifyText to automatically fit the screen width."
  for ln in adText.JustifyText(helpText):
    print (ln)
  print ()
  print ("_ProcessParms()_")
  helpInfo = [ ]
  helpInfo.append("ProcessParms takes in a dictionary of parameters to be processed against sys.argv")
  helpInfo.append("The Dictionary take the form string1, string2 where string 1 is the name of the parm, equivalent to the variable name and string2 defines how a matching sys.argv is to be processed.")
  helpInfo.append("Example  1: parms['verbose'] = 'v'")
  helpInfo.append("This example represents a True/False response. In this case, ProcessParms will look for -v in any element in sys.argv and if one is found then parms['verbose'] will be set to True upon return. If -v is not found parms['verbose'] is set to False.")
  helpInfo.append("Example  2: parms['verbose'] = 'v,verbose'")
  helpInfo.append("This also returns a True/False response. In this case, ProcessParms will look for either -v or --verbose in any element in sys.argv and if either is found then parms['verbose'] will be set to True upon return. If neither are found parms['verbose'] is set to False.")
  helpInfo.append("Example  3: parms['colour'] = 'c,color,colour:1'")
  helpInfo.append("This example is expecting a parameter, as represented by the ':'. In this case, ProcessParms will look for either -c or --color or --colour in any element in sys.argv and if any are found then parms['colour'] will be set to the value following the argument, or None if no value is specified. If none of the three arguments are specified then parms['colour'] is set to the value following the ':', in this example 1, although the value suplied need not be an integer or even a number; there is nothing to stop the user using '--colour red'. This will need to be validated in the calling program")
  helpInfo.append("Example  4: parms['colour'] = 'c,color,colour:[Red,Green,Blue]'")
  helpInfo.append("This example is expecting a parameter, as represented by the ':'. In this case, a value is expected after the argument and the value must be one of the values in the list, in this case Red, Green or Blue. If the argument is not specified then the first item in the list is the default value")
  helpInfo.append("In all cases, additional text may be added at the end of the parm value in braces { and }. this is help information and is output when cmd --help is called by the end user. It is automatically ghenerated and parms['help'] = 'help' does not need to be specified or checked for in the calling program")
  helpInfo.append("_Known issues and potential improvements_")
  helpInfo.append("- allow the calling program to specify it a particular value type, e.g. int or float")
  helpInfo.append("- warn with raised error if arguments are specified more than once, i.e. not unique")
  helpInfo.append("- JustifyText gets confused when '\\n' is included in text")
#  helpInfo.append("")
  for helpText in helpInfo:
    for ln in adText.JustifyText(helpText):
      print (ln)
    if not helpText[0:2] in "- ":
      print ()
  sys.exit(0)

# #########################################################
#
#   AAA   N   N  DDDD   RRRR   EEEEE  W   W    DD
#  A   A  N   N  D   D  R   R  E      W   W    D 
#  A   A  NN  N  D   D  R   R  E      W   W    D 
#  AAAAA  N N N  D   D  RRRR   EEE    W   W    D 
#  A   A  N  NN  D   D  R R    E      W W W    D 
#  A   A  N   N  D   D  R  R   E      W W W    D 
#  A   A  N   N  DDDD   R   R  EEEEE   WWW     DD
#
# #############################################################
#
#   AAA          d                   DDDD
#  A   A         d                   D   D               i
#  A   A nnn     d       ee          D   D                   ss
#  AAAAA n  n  ddd r rr e  e w   w   D   D  aa   v     v i  s
#  A   A n  n d  d rr   eee  w   w   D   D a  a   v   v  i   ss
#  A   A n  n d  d r    e    w w w   D   D a  a    v v   i     s
#  A   A n  n  ddd r     ee   w w    DDDD   aa a    v     i  ss
#
# #############################################################

def IsHelp(s, helpType = ""):
  return (s[0:4+len(helpType)].lower() == "help" + helpType)

def DisplayHelp(pgmName, parms):
  print ("Displaying Help for {}".format(pgmName))
  print ()
  for parm in parms:
    if (IsHelp(parm, "-intro")):
      for opLn in adText.JustifyText(parms[parm]):
        print (opLn)
## These are left here to demo the different types of justification:
#      time.sleep(1.7)
#      for opLn in adText.JustifyText(parms[parm], justify = "right"):
#        print (opLn)
#      time.sleep(1.7)
#      for opLn in adText.JustifyText(parms[parm], justify = "cent"):
#        print (opLn)
#      time.sleep(1.7)
#      for wd in range(17, os.get_terminal_size().columns):
#        print (("....:....|" * (int(wd / 10) + 1))[0:wd])
#        for opLn in adText.JustifyText("{}] {}".format(wd, parms[parm]), wd, "full"):
#          print (opLn)
#        print ()
#        time.sleep(0.5)
      print ()
  termSize = os.get_terminal_size()
  maxCmdLen = 0
  listCmds = []
  lastHelp = ""
  for parm in parms:
    if (type(parms[parm]) is str and len(parms[parm]) > 0):
      parmCmds = ""
      parmDflt = ""
      parmOpts = ""
      parmHelp = ""
      if (parms[parm][-1] != "}") and not IsHelp(parm):
        parms[parm] += "{No Help Information Available}"
      if (parms[parm][-1] == "}"):
        ptr = parms[parm].find(":")
        if (ptr < 0):
          ptr = parms[parm].find("{")
        parmCmds = parms[parm][0:ptr]
        parmDflt = parms[parm][ptr+1:parms[parm].find("{", ptr)]
        parmHelp = parms[parm][parms[parm].find("{", ptr)+1:-1]
        if (len(parmDflt) > 0 and parmDflt[0] == "["):
          parmOpts = parmDflt
          if (parmDflt.find(",") > 0):
            parmDflt = parmDflt[1:parmDflt.find(",")]
          else:
            parmDflt = parmDflt[1:-2]
        if parmDflt != "":
          parmHelp += ", default value = {}".format(parmDflt)
        if parmOpts != "":
          parmHelp += "; possible options are one of {}".format(parmOpts.replace(",", ", "))

        if parmCmds == "":
          lastHelp = parmHelp
        else:
          cmdList = " "
          for parmCmd in parmCmds.split(","):
            if len(parmCmd) > 0:
              if len(cmdList) > 2:
                cmdList += ", "
              if len(parmCmd) == 1:
                cmdList += "-{0}".format(parmCmd)
              else:
                cmdList += "--{0}".format(parmCmd)
          listCmds.append( [cmdList, parmHelp] )
        if (not IsHelp(parm)):
          maxCmdLen = max(maxCmdLen, len(cmdList))
  if lastHelp != "":
    listCmds.append( ["\nAny Remaining arguments:", lastHelp] )
  for cmd in listCmds:
    if cmd[0][0] == "\n":
      parmCmd = cmd[0]
    else:
      parmCmd = ((cmd[0] + " " * maxCmdLen)[0:maxCmdLen])
    opLn = ("{0}  ".format(parmCmd))
    parmHelp = cmd[1]
    while parmHelp != "":
      ptr = parmHelp.find(" ", 1)
      if (len(opLn) + (ptr if ptr >= 0 else len(parmHelp)) > termSize.columns - 2):
        print (opLn)
        opLn = " " * min(maxCmdLen, int(termSize.columns / 2)) + " "
      else:
        opLn += parmHelp[0:ptr] if ptr > 0 else parmHelp
        parmHelp = parmHelp[ptr:] if ptr > 0 else ""
    print (opLn)
  if (sum(IsHelp(parm) for parm in parms)):
    print ()
  for parm in parms:
    if (IsHelp(parm, "-descr")):
      for opLn in adText.JustifyText(parms[parm]):
        print (opLn)
#      print (adText.JustifyText(parms[parm]))
      print ()
  sys.exit(0)

###################################################################################################
def ProcessParms(parms, setRunLock = False):
# description: processes sys.args into parms
# usage: parms = ProcessParms(parms, <True|False>)
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
#     parms["verbose"]   = "v,verbose"            #- will be True if specified on cmd line
#                                                    or False if not
#     parms["runlevel"]  = "r,runlvl,runlevel:3"  #- set to the arg after -r --runlvl or
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
## define intial variables:
  rc          = {}       #: where to store the parms bring returned to the caller
  catchParm   = None     
  catchList   = None     
  adRunLock   = None     
  useHforHelp = True 

  for parm in parms:
    if (isinstance(parms[parm], str)):
      if (parms[parm] == '' or parms[parm][0:1] == "{"):
        catchParm = parm
      elif (parm[0:4].lower() != "help"):
        parms[parm] = ",{}".format(parms[parm].replace(":",",:"))
        if (parms[parm][-1] == "}" and parms[parm].find(":") < 0):
          parms[parm] = parms[parm].replace("{", ",{", 1)
        elif (parms[parm].find(":") == -1):
          parms[parm] += ","
        if ",h," in parms[parm].lower():
          useHforHelp = False
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
        adRunLock = adRunLock.RunLock()
        adRunLock.set()
      continue
##??    cmd = arg.lower()

## process help - send to other def?
    helpCmds = []
    if useHforHelp:
      helpCmds.append("-h")
    helpCmds.append("--help")
    if (arg in helpCmds):
      helpText = "," + ("h," if useHforHelp else "") + "help,{Displey this information}"
      parmsCpy = { "helptext": helpText }
      parmsCpy.update(parms)
      DisplayHelp(os.path.split(sys.argv[0])[1], parmsCpy)
      sys.exit(0)

###
    if (debugging):
      print ("a] checking arg: {}".format(arg))
    print (">>>", arg)
    if (arg[0:2] == "--"):
      cmd = arg[2:]
      arg = None
      if (cmd.find(":") > 0):
        arg = cmd[cmd.find(":") + 1 : ]
        cmd = cmd[0 : cmd.find(":")]
      elif (cmd.find("=") > 0):
        arg = cmd[cmd.find("=") + 1 : ]
        cmd = cmd[0 : cmd.find("=")]
      cmd = ",{},".format(cmd)
    elif (arg[0:1] == "-"):
      # cmd = arg.replace("-", "").lower()
      cmd = arg[1:2]
      if len(arg) > 2:
        arg = arg[2:]
        if arg[0] in ":=":
          # arg = adFns.GetValue(arg[1:])
          arg = arg[1:]
        print ("..>", cmd, arg)
      else:
        arg = None
      if (cmd.find(":") > 0):
        arg = cmd[cmd.find(":") + 1 : ]
        cmd = cmd[0 : cmd.find(":")]
      if (cmd.find("=") > 0):
        arg = cmd[cmd.find("=") + 1 : ]
        cmd = cmd[0 : cmd.find("=")]
      cmd = ",{},".format(cmd)
    if (debugging):
      print ("b] cmd: {0} .. arg: {1}".format(cmd, arg))

# causes more problems than it solves, commented out
#  if True: # because otherwise, I shall have to de-indent all the below lines by hand
    ## strip off any help information
    for parm in parms:
      if len(parms[parm]) > 0 and parms[parm][-1] == "}":
        ptr = parms[parm].find("{")
        parms[parm] = parms[parm][0:ptr]
        if debugging:
          print (".>>", parm, parms[parm])

    ## loop through parms, looking for the matching one
    for parm in parms:
      if (isinstance(cmd, str)):
        if debugging:
          print ("cmd is string", cmd)
        if (isinstance(parms[parm], str) and cmd in parms[parm]):
          if debugging:
            print("parms[parm]", parms[parm])

          ## no cmd args, so must be bool flag
          if parms[parm].find(":") == -1:
            if debugging:
              print ("Setting {} to True".format(parm))
            rc[parm] = True
            cmd = None

          else:
            ## assign a parm with a value
            if arg == None: ## not ready yet
              continue
            ## must passed arg be one of a list of allowable options?
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
                rc[parm] = adFns.GetValue(arg)
              else:
                rc[parm] = None
            else:
              ## assign the passed value [in its most appropriate type] to the parm
              rc[parm] = adFns.GetValue(arg)
            cmd = None
          arg = None

# fill unassigned parm to catch alls
    if (cmd == None and arg != None):
      if (debugging):
        print ("cmd+arg", cmd, arg)
        print ("catch parm, list", catchParm, catchList)
      if (catchParm != None):
        if (catchList != None and parms[catchParm] != ""):
          parms[catchList].append(parms[catchParm])
          if (debugging):
            print ("catchList", parms[catchList])
        if (debugging):
          print ("Assigning catchparm to", arg)
        parms[catchParm] = arg
        arg = None
      else:
        if (catchList != None):
          parms[catchList].append(arg)

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
    if (parm[0:4].lower() == "help"):
      pass
    elif (isinstance(parms[parm], str) and parms[parm].find(',:[') > 0 and parms[parm][-1] == "]"):
      parmOptions = parms[parm][parms[parm].find("[")+1:-1]
      rc[parm] = parmOptions.split(",")[0]
    elif (isinstance(parms[parm], str) and parms[parm].find(',:') > 0):
      rc[parm] = adFns.GetValue(parms[parm][parms[parm].find(":") + 1:])
    else:
      rc[parm] = False
  if (setRunLock):
    return rc, adRunLock
  else:
    return rc
