#!/usr/bin/python3
import os, sys
import time
# ########################################################################## #
#
#   AAA          d                      d ''  AAA             t              #
#  A   A         d                      d  ' A   A           ttt             #
#  A   A         d       ee             d '  A   A            t         ss   #
#  AAAAA nnn   ddd r rr e  e w   w    ddd    AAAAA zzzz  oo   t   u  u s     #
#  A   A n  n d  d rr   eee  w   w   d  d    A   A   z  o  o  t   u  u  ss   #
#  A   A n  n d  d r    e    w w w   d  d    A   A  z   o  o  t   u  u    s  #
#  A   A n  n  ddd r     ee   w w     ddd    A   A zzzz  oo    tt  uuu  ss   #
#
# ########################################################################## #
debugging = not True # turn on/off internal debugging msgs
version = "1.03.007" # added output msg if end user called calling pgm with an invalid parm
version = "1.03.008" # moved the output msg, it was in the wrong place.
# ################## # ########### #
sys.path.append("/mnt/ref/Python") #
import adFns                       #
from adText import print_justified #
# ################################ #

## This allows this file to display help, but only if executed directly:
if os.path.basename(__file__) in sys.argv[0]:
  print_justified("_adCmdOpts.py Help Information_")
  print ()
  print_justified("_IsHelp(text, suffix)_")
  print_justified("Returns True if text starts with 'help' or if text starts with 'help'+suffix, False otherwise. This is case insensitive and is primarily used to differentiate between parm args and help information in ProcessParms() and DisplayHelp().")
  print ()
  print_justified("_InitParms()_")
  print_justified("Creates the dictionary and creates verbose and timeDelay parms unless False is passed as a parm")
  print ()
  print_justified("_AddDfltParms()_")
  print_justified("Adds verbose and timeDelay parms to existing parms dictionary unless False is passed as a parm")
  print ()
  print_justified("_DisplayHelp()_")
  print_justified("Uses the same parms as ProcessParms() plus the program name which is collected automatically from sys.argv[0]. The argument options are extracted from the parms as is the help text and any default values. These are formatted and output to the user using adText.JustifyText to automatically fit the screen width.")
  print ()
  print_justified ("_ProcessParms()_")
  helpInfo = [ ]
  helpInfo.append("ProcessParms takes in a dictionary of parameters to be processed against sys.argv")
  helpInfo.append("usage: parms = ProcessParms(parms, <True|False>)")
  helpInfo.append("Parameter Arguments:")
  helpInfo.append("1] parms      - a dictionary of variable names and command arguments")
  helpInfo.append("2] setRunLock - boolean, when true create a file /run/lock/<pgmname>.lock containing the run time pid. It is up to the caller to check and use the file as appropriate to the program. When called with this parm = True, the adRunLock object is returned to the calling program as the second return value.")
  helpInfo.append("Initialise the dictionary with keys and values; the key is the name of the parm to be used within the calling program. Values need to follow a format:")
  helpInfo.append("- <arg command>(,...)  -- set to True [if specified as a cmd arg or False if not")
  helpInfo.append("- <arg command>(,...): -- set to value following cmd arg, or None if value does not follow cmd arg")
  helpInfo.append("- <arg command>(,...):<default value> -- set to value following cmd arg, or <default value> if value does not follow cmd arg")
  helpInfo.append("- <arg command>(,...):[<default option>,<list option>,...] -- set to value following cmd arg, or <default value> if value does not follow cmd arg. Cmd arg value _must_ be one value in the list")
  helpInfo.append("The value defines how a matching sys.argv item is to be parsed. Upon return to the calling program, value becomes either the value after the arg or the default as specified by the calling program. Note, value will change type and become an int, a float, a boolean or remain a string as appropriate.")

  helpInfo.append("Parm Example 1: parms['verbose'] = 'v'")
  helpInfo.append("This also returns a True/False response. In this case, ProcessParms will look for either -v in any element in sys.argv and if either is found then parms['verbose'] will be set to True upon return. If -v is not specified then parms['verbose'] is set to False.")
  helpInfo.append(". pgm          : parms['verbose'] = False")
  helpInfo.append(". pgm -v       : parms['verbose'] = True")
  helpInfo.append(". pgm -v 23    : parms['verbose'] = True and 23 will be added to catchparm or catchall if specified")
  helpInfo.append(". pgm -v Green : parms['verbose'] = True and 'Green' will be added to catchparm or catchall if specified")
  helpInfo.append(". pgm -v 4.7   : parms['verbose'] = True and 4.7 will be added to catchparm or catchall if specified")
  helpInfo.append("-v may be replaced with --verbose in each example")

  helpInfo.append("Parm Example 2: parms['verbose'] = 'v,verbose'")
  helpInfo.append("This also returns a True/False response. In this case, ProcessParms will look for either -v or --verbose in any element in sys.argv and if either is found then parms['verbose'] will be set to True upon return. If neither are found parms['verbose'] is set to False.")
  helpInfo.append(". pgm          : parms['verbose'] = False")
  helpInfo.append(". pgm -v       : parms['verbose'] = True")
  helpInfo.append(". pgm -v 23    : parms['verbose'] = True and 23 will be added to catchparm or catchall if specified")
  helpInfo.append(". pgm -v Green : parms['verbose'] = True and 'Green' will be added to catchparm or catchall if specified")
  helpInfo.append(". pgm -v 4.7   : parms['verbose'] = True and 4.7 will be added to catchparm or catchall if specified")
  helpInfo.append("-v may be replaced with --verbose in each example")

  helpInfo.append("Parm Example 3: parms['colour'] = 'c,color,colour:'")
  helpInfo.append("This example is expecting a parameter, as represented by the ':'. In this case, ProcessParms will look for either -c or --color or --colour in any element in sys.argv and if any are found then parms['colour'] will be set to the value following the argument, or 1 if no value is specified, although the value supplied need not be an integer or even a number; there is nothing to stop the user using '--colour red'. This will need to be validated in the calling program.")
  helpInfo.append(". pgm --color    : parms['colour'] = None")
  helpInfo.append(". pgm --color=23 : parms['colour'] = 23 [type is int]")
  helpInfo.append(". pgm -c:Green   : parms['colour'] = 'Green' [type is str")
  helpInfo.append(". pgm -c 4.7     : parms['colour'] = 4.7 [type is float]")
  helpInfo.append("-c or --color or --colour may be used interchangably")

  helpInfo.append("Parm Example 4: parms['colour'] = 'c,color,colour:1'")
  helpInfo.append("This example is expecting a parameter, as represented by the ':'. In this case, ProcessParms will look for either -c or --color or --colour in any element in sys.argv and if any are found then parms['colour'] will be set to the value following the argument, or 1 if no value is specified, although the value supplied need not be an integer or even a number; there is nothing to stop the user using '--colour red'. This will need to be validated in the calling program.")
  helpInfo.append(". pgm --colour : parms['colour'] = 1 [type is int]")
  helpInfo.append(". pgm -c Green : parms['colour'] = 'Green' [type is str")
  helpInfo.append(". pgm -c 4.7   : parms['colour'] = 4.7 [type is float]")
  helpInfo.append("-c or --color or --colour may be used interchangably")

  helpInfo.append("Parm Example 5: parms['colour'] = 'c,color,colour:[Red,Green,Blue]'")
  helpInfo.append("This example is expecting a parameter, as represented by the ':'. In this case, a value is expected after the argument and the value must be one of the values in the list, in this case either Red, Green or Blue. If the argument is not specified then the first item in the list is the default value. If the cmd arg value is not one of the items specified in the list then the value returned is None")
  helpInfo.append(". pgm -c        : parms['colour'] = 'Red'")
  helpInfo.append(". pgm -c Green  : parms['colour'] = 'Green'")
  helpInfo.append(". pgm -c Orange : parms['colour'] = None")
  helpInfo.append("-c may be replaced with --color or --colour in each example")

  helpInfo.append("Parm Example 6: parms['destPath'] = ''")
  helpInfo.append("This example will be filled with the last 'unattached' cmd arg.")
  helpInfo.append("If the following parms are defined:")
  helpInfo.append(". parms['verbose'] = 'v'")
  helpInfo.append(". parms['colour'] = 'c,color,colour:[Red,Green,Blue]'")
  helpInfo.append(". parms['mainPath'] = ''")
  helpInfo.append("and either of the following cmds were used:")
  helpInfo.append(". pgm -c Red -v userPath")
  helpInfo.append(". pgm -v userPath")
  helpInfo.append("Then the parms will be replaced with:")
  helpInfo.append(". parms['verbose'] = True")
  helpInfo.append(". parms['colour'] = 'Red'")
  helpInfo.append(". parms['mainPath'] = 'userPath'")
  helpInfo.append("because userPath [in the cmd arg list] is not associated with any cmd arg")

  helpInfo.append("Parm Example 7: parms['pathList'] = []")
  helpInfo.append("This example will be filled with the any 'unattached' cmd args.")
  helpInfo.append("If the following parms are defined:")
  helpInfo.append(". parms['verbose'] = 'v'")
  helpInfo.append(". parms['colour'] = 'c,color,colour:[Red,Green,Blue]'")
  helpInfo.append(". parms['argList'] = []")
  helpInfo.append("and either of the following cmds were used:")
  helpInfo.append(". pgm -c Red -v a b c d e")
  helpInfo.append(". pgm -v -c Red a b c d e")
  helpInfo.append("Then the parms will be replaced with:")
  helpInfo.append(". parms['verbose'] = True")
  helpInfo.append(". parms['colour'] = 'Red'")
  helpInfo.append(". parms['mainPath'] = ['a', 'b', 'c', 'd', 'e']")

  helpInfo.append("Parm Example 8: parms['destPath'] = '' combined with parms['pathList'] = []")
  helpInfo.append("This example will be filled with the any 'unattached' cmd args.")
  helpInfo.append("If the following parms are defined:")
  helpInfo.append(". parms['verbose'] = 'v'")
  helpInfo.append(". parms['colour'] = 'c,color,colour:[Red,Green,Blue]'")
  helpInfo.append(". parms['mainArg'] = ''")
  helpInfo.append(". parms['argList'] = []")
  helpInfo.append("and either of the following cmds were used:")
  helpInfo.append(". pgm -c Red -v a b c d e f")
  helpInfo.append(". pgm -v -c Red a b c d e f")
  helpInfo.append(". pgm a b c d e f -v")
  helpInfo.append("Then the parms will be replaced with:")
  helpInfo.append(". parms['verbose'] = True")
  helpInfo.append(". parms['colour'] = 'Red'")
  helpInfo.append(". parms['mainArg'] = 'f'")
  helpInfo.append(". parms['mainPath'] = ['a', 'b', 'c', 'd', 'e']")
  helpInfo.append("It was designed this way so that it will handle commands like 'cp -v <path1> <path2> <path3>' where all files in path1 and path2 are copied to path3")

  helpInfo.append("In all cases, additional text may be added at the end of the parm value in braces { and }, even parms['mainPath'] = from in example 6. Help text may not be added to parms['argList'] = [] from example 7. This is help information and is output when cmd --help is called by the end user. It is automatically generated and parms['help'] = 'help' does not need to be specified or checked for in the calling program. --help or -h must be the first cmd arg when called by the end user.")
  helpInfo.append("Additional help text may be specified:")
  helpInfo.append("- parms['help-intro<suffix>'] = 'help text'. help-intro paragraphs will be displayed before the help for the parms in the order that the help-intro parms are added to the diectionary.")
  helpInfo.append("- parms['help-descr<suffix>'] = 'help text'. help-descr paragraphs will be displayed after the help for the parms in the order that the help-descr parms are added to the diectionary.")

  helpInfo.append("_Known issues and potential improvements_")
  helpInfo.append("- if a cmd arg is specified by the caller but is not in the parms list then the end user needs to be notified")
  helpInfo.append("- allow the calling program to specify it a particular value type, e.g. int or float")
  helpInfo.append("- warn with raised error if arguments are specified more than once, i.e. not unique")
  helpInfo.append("- JustifyText gets confused when '\\n' is included in text")
  helpInfo.append("- work out a way to allow -v to be specified when -v2 is expected even when there is another arg afterward, perhaps even an argument destined for the catchall. This would allow ignoring the default and having a True/False returned")
  helpInfo.append("- Some[?] programs allow concatenated args, e.g. 'du -hd1' but not 'du -BGd2' needs to be 'du -BG -d2'")
  for helpText in helpInfo:
    print_justified(helpText)
    if not helpText[0:1] in "- . ":
      print ()
  sys.exit(0)

def InitParms(addDefaults = True):
  parms = { }
  if addDefaults:
    parms["verbose"]   = "v,verbose:0{display execution trace messages, 0 = off, 1 = high level, 2 = trace messages, 3 = very detailed}"
    parms["timeDelay"] = "t,timedelay:0{Length of time delay after verbose msgs}"
  return parms

def AddDfltParms(newParms = None):
  if newParms == None:
    newParms = { }
  newParms["verbose"]   = "v,verbose:0{display execution trace messages, 0 = off, 1 = high level, 2 = trace messages, 3 = very detailed}"
  newParms["timeDelay"] = "t,timedelay:0{Length of time delay after verbose msgs}"
  return newParms

def IsHelp(s, helpType = ""):
  return (s[0:4+len(helpType)].lower() == "help" + helpType)

def DisplayHelp(pgmName, parms):
  print ("Displaying Help for {}".format(pgmName))
  print ()
  for parm in parms:
    if (IsHelp(parm, "-intro")):
      print_justified(parms[parm])
      if debugging:
      ## These are left here to demo the different types of justification:
        time.sleep(4.7)
        print_justified(parms[parm], justify = "cent")
        time.sleep(4.7)
        print_justified(parms[parm], justify = "right")
        time.sleep(4.7)
        for wd in range(17, os.get_terminal_size().columns):
          print (("....:....|" * (int(wd / 10) + 1))[0:wd])
          print_justified("{}] {}".format(wd, parms[parm]), wd, "full")
          print ()
          time.sleep(0.7)
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
        if ptr < 0 or parms[parm].find("{") < ptr:
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
        if parms[parm][ptr] == ":" and parms[parm][ptr + 1] == "{":
          parmDflt = None
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
      print_justified(parms[parm])
      print ()
  sys.exit(0)

###################################################################################################
def ProcessParms(parms, setRunLock = False):
## define intial variables:
  rc          = {}       #: where to store the parms bring returned to the caller
  catchParm   = None     #
  catchList   = None     #
  adRunLock   = None     #

## prepare caller's parms for processing:
  useHforHelp = True # has -h been used for something else, such as -h,--human-readable-numbers
  for parm in parms:
    if (isinstance(parms[parm], str)):
      if (parms[parm] == '' or parms[parm][0:1] == "{"):
        catchParm = parm
      elif (parm[0:4].lower() != "help"):
        parms[parm] = ",{}".format(parms[parm].replace(":", ",:", 1))
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

## has user asked for help:
  if "--help" in sys.argv or (useHforHelp and "-h" in sys.argv):
    helpText = "," + ("h," if useHforHelp else "") + "help,{Display this information}"
    parmsCpy = { "helptext": helpText }
    parmsCpy.update(parms)
    DisplayHelp(os.path.split(sys.argv[0])[1], parmsCpy)
    sys.exit(0)
  else:
## strip off any help information
    for parm in parms:
      if len(parms[parm]) > 0 and parms[parm][-1] == "}":
        ptr = parms[parm].find("{")
        parms[parm] = parms[parm][0:ptr]
        if debugging:
          print (".>>", parm, parms[parm])

## start looping through args
  for arg in sys.argv:
    if (arg == sys.argv[0]):
      if (setRunLock):
        adRunLock = adRunLock.RunLock()
        adRunLock.set()
      continue

## Splitup the cmd args with ,s and separate out the arg value
    if (debugging):
      print ("a] checking arg: {}".format(arg))
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

### loop through parms, looking for the matching one
    foundParm = None
    for parm in parms:
      if (isinstance(cmd, str)):
        if debugging:
          print ("cmd is string", cmd)
        if (isinstance(parms[parm], str) and cmd in parms[parm]):
          foundParm = parm
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
              rc[parm] = None if arg == None else adFns.GetValue(arg)
            cmd = None
          arg = None
#    print (">>>", foundParm, parms)
    if foundParm == arg == None:					# 1.03.008
      print ("Unknown Cmd Arg: {}".format(cmd[1:-1]))			# 1.03.008

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
  if debugging:
    print("parms>", parms)
    print("rc ..>", rc)
  for parm in parms:
    if debugging:
      print (parm, parms[parm])
    if (parm[0:4].lower() == "help"):
      pass
    elif (isinstance(parms[parm], str) and parms[parm].find(',:[') > 0 and parms[parm][-1] == "]"):
      parmOptions = parms[parm][parms[parm].find("[")+1:-1]
      rc[parm] = parmOptions.split(",")[0]
    elif (isinstance(parms[parm], str) and parms[parm].find(',:') > 0):
      if parms[parm][-1] == ":": # parm was specified but no dflt given
        rc[parm] = None
      else: # set to provided dflt value
        rc[parm] = adFns.GetValue(parms[parm][parms[parm].find(":") + 1:])
    else:
      rc[parm] = False

  if (setRunLock):
    return rc, adRunLock
  else:
    return rc
