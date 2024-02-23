# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0401,W0622,E0402,E0603


"""Original Programmer Daemon

opd <cmd> [key=val] [key==val] [mod=n1,n2]
opd [-a] [-c] [-d] [-h] [-v]

commands:

cmd - commands
mod - show available modules

modules:

$ opd mod
cmd,flt,irc,log,mod,mre,pwd,req,rss,tdo,thr

options:

-a     load all modules
-c     start console
-d     start daemon
-h     display help
-v     use verbose
"""
