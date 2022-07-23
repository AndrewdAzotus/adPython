# ProcessParms
A selecction of useful functions Written in Python, that started with my own take on processing sys.argv

adCmdOpts.py       - ProcessParms()
adFilerFns.py      - CopyFile(), MoveFile()
adFns.py           - GetValue(), is_int(), is_float()
adRunLock.py       - 
adText.py          - 

First, a few useful functions at the top:

GetValue() takes a string and does its best to return an appropriate value.
First it checks for a boolean True, False, t, f, plus a few others
Secondly, it checks for an integer,
Third, a float
if none of these match, then it just returns the string.

is_int() and is_float() which were the basis that became GetValue() and simply return True or False depending on the value passed in

ProcessParms(), there are a lot of comments at the top that may end up here,
but basically, you supply a dictionary containing variable names as the keys and details
of the parms expected and how to process them as values and it returns the same dictionary
with the dictionary values containing the validated parms from the invoking command line.

On the invoking command, the args are considered to be cmds with an optional argument,
e.g. python-pgm -n 23 --force
where the cmds are n and force and the cmd arg is 23. It does break the rules a little as
python-pgm --n 23 -force is equally valid, any number of hyphens in fact.

The dictionary passed to ProcessParms defines what is expected to be processed on the 
invoking cmd, e.g. the above could be processed with:

parms = { }
parms["number"] = "n,number:"
parms["forcerun"] = "force"
parms["dayOfWeek"] = "c,color,colour:[Red,Blue,Green]

parms["number"] is assigned to the value following -n or -number or an empty string if -n is not used.
parms["forcerun"] is assigned True if specified [--force above] or false [the default] if not. There is
  no colon in the value, so a boolean type is returned to the calling program.
parms["dayOfWeek"] is set if -c, -color or -colour is specified and the arg must be in the list in the
square brackets, i.e. Red, Blue or Green in this example. If not specified then it defaults to the first
option

The final part of this is a class called RunLock that can create a file in /run/lock [Linux specific]
and places the PId as the contents. The implication is that setting this file allows a calling pgm to 
check if it is already running and to return the pid of that other running instance and allows a clean
way to quit, note ProcessParms above has the option to set this file too, but does not make use of nor
returns the object create by this object...
...but it could :) -- perhaps a later update
