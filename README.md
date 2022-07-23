# ProcessParms
A selecction of useful functions Written in Python, that started with my own take on processing sys.argv

Filename:            included functions:
adCmdOpts.py       - ProcessParms()
adFilerFns.py      - CopyFile(), MoveFile()
adFns.py           - GetValue(), is_int(), is_float()
adRunLock.py       - class RunLock
adText.py          - JustifyLine(), JustifyText()

The following notes apply to the functions above.

**GetValue()** takes a string and does its best to return an appropriate value.
First it checks for a boolean True, False, t, f, plus a few others
Secondly, it checks for an integer,
Third, a float
If none of these match, then it just returns the string as passed in.

**is_int()** and **is_float()** which were the basis that became GetValue() and simply return True or False depending on the value passed in

**ProcessParms()**, there are a lot of comments at the top that may end up here,
but basically, you supply a dictionary containing variable names as the keys and details
of the parms expected and how to process them as values and it returns the same dictionary
with the dictionary values containing the validated parms from the invoking command line.

Pass in a dictionary, for example:
  parms = { }
  parms["number"] = "n,number:"
  parms["forcerun"] = "force"
  parms["dayOfWeek"] = "c,color,colour:[Red,Blue,Green]
  parms = adCmdOpts.ProcessParms(parms)

The minimal usage is shown for forcerun. In this example, parms["forcerun"] is assigned True if specified [--force above] or false [the default] if not. There is no colon in the value, so a boolean type is returned to the calling program.

parms["number"] is assigned to the value following -n or -number or an empty string if -n is not used in the command args.

parms["dayOfWeek"] is set if -c, -color or -colour is specified and the arg must be in the list in the square brackets, i.e. Red, Blue or Green in this example. If not specified then it defaults to the first option

the functionality of --help or -h is automatically built into ProcessParms. The programmer does not need to add --help to the dictionary. Add any text after the dictionary value inside braces, for example:
  parms["number"] = "n,number:{enter a number}"
and this will be output when the end user specifies the --help arg, for example pgmname --help:

Help Information for pgmame
 -n, --number    enter a number

If the program needs an -h option, for example -h for -humanreadable numbers:
parms["humanreadable"] = "h,humanreadable{output numbers in human readable format}"
then only --help would display the help text, -h would be returned to the calling program with the parm set accordingly.

Adding dictionary entries of "Help-Intro*" will be output after the Header line and before the parm definitions and "Help-Descr*" would be output after the parms. If any of these entries start with ". " or "o " or "- " then all lines after the first will be indented by 2 spaces, e.g.

parms["help-intro1"] = "- this is a wondeful program that does magic stuff"

- this is a wondeful program that
  does magic stuff

All text output is word wrapped and justified to fit on the screen depending on the width of the output terminal.

**JustifyLine()** and **JustifyText()** perform very similar functions. JustifyText() calls JustifyLine() for the actual justification. JustifyText takes as its first parm a string of text, this is split into multiple lines of whole words. Each line is then passed to JustifyLine() to for alignment.

Both functions have up to three parms:
  txt  .. .. .. .. the text to be justified
  lnWidth .. .. .. the width to justify the text to
  justify .. .. .. the justification type: left, right, centre or full. Note that justify = "full" is not well balanced but it looks well enough.
If the text begins with  ". " or "o " or "- " then all lines after the first will be indented by 2 spaces as shown above for --help in ProcessParms

... more documentation to come ...
