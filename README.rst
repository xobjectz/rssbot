RSSBOT
######


NAME

::

    RSSBOT - feeding rss


INSTALL

::

    $ pipx install rssbot


SYNOPSIS

::

    rssbot <cmd> [key=val] 
    rssbot <cmd> [key==val]
    rssbot [-a] [-c] [-d] [-v] 


DESCRIPTION

::

    RSSBOT is a python3 bot able to display rss feeds in your channel.
    It has all the python3 code to program a unix cli program, such as
    disk perisistence for configuration files, event handler to
    handle the client/server connection, code to introspect modules
    for commands, deferred exception handling to not crash on an
    error, a parser to parse commandline options and values, etc.

    RSSBOT provides an objx namespace that allows for easy json save//load
    to/from disk of objects. It provides an "clean namespace" Object class
    that only has dunder methods, so the namespace is not cluttered with
    method names. This makes storing and reading to/from json possible.

    RSSBOT is Public Domain.


USAGE


without any argument the program does nothing

::

    $ rssbot
    $


see list of commands

::

    $ rssbot cmd
    cmd,err,mod,req,thr,ver


list of modules

::

    $ rssbot mod
    cmd,err,fnd,irc,log,mod,req,rss,tdo,thr


use mod=<name1,name2> to load additional modules

::

    $ rssbot cfg mod=irc


start a console

::

    $ rssbot -c mod=irc,rss
    >


use -v for verbose

::

    $ rssbot -cv mod=irc
    RSSBOT started CV started Sat Dec 2 17:53:24 2023
    >


start daemon

::

    $ rssbot
    $ 


CONFIGURATION

irc

::

    $ rssbot cfg server=<server>
    $ rssbot cfg channel=<channel>
    $ rssbot cfg nick=<nick>

sasl

::

    $ rssbot pwd <nsvnick> <nspass>
    $ rssbot cfg password=<frompwd>

rss

::

    $ rssbot rss <url>
    $ rssbot dpl <url> <item1,item2>
    $ rssbot rem <url>
    $ rssbot nme <url> <name>


COMMANDS

::

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    fnd - find objects 
    log - log some text
    met - add a user
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    thr - show the running threads


SYSTEMD

save the following it in /etc/systems/system/rssbot.service and
replace "<user>" with the user running pipx

::

    [Unit]
    Description=feeding rss
    Requires=network.target
    After=network.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.rssbot
    ExecStart=/home/<user>/.local/pipx/venvs/rssbot/bin/rssbotd
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target


then run this

::

    $ mkdir ~/.rssbot
    $ sudo systemctl enable rssbot --now

default channel/server is #objx on localhost


CODE

::

    >>> from rssbot import Object, read, write
    >>> o = Object()
    >>> o.a = "b"
    >>> write(o, "test")
    >>> oo = Object()
    >>> read(oo, "test")
    >>> oo
    {"a": "b"}


FILES

::

    ~/.rssbot
    ~/.local/bin/rssbot
    ~/.local/bin/rssbotd
    ~/.local/pipx/venvs/rssbot/


AUTHOR

::

    Bart Thate <objx@proton.me>


COPYRIGHT

::

    RSSBOT is Public Domain.
