RSSBOT
######


NAME

::

    RSSBOT - 24/7 feed Fetcher


INSTALL

::

    $ pipx install rssbot
    $ pipx ensurepath


SYNOPSIS

::

    rssbot <cmd> [key=val] [key==val]
    rssbotd


DESCRIPTION

::

    RSSBOT is a python3 bot able to display rss feeds in your channel.

    RSSBOT comes with a cli to configure and a daemon to run in the
    background, hooking the daemon in systemd brings a 24/7 available
    rssbot in your channel.


COMMANDS

::

    cfg - irc configuration
    cmd - commands
    dpl - sets display items
    mre - displays cached output
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    rss - add a feed


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


SYSTEMD

save the following it in /etc/systems/system/rssbot.service and
replace "<user>" with the user running pipx

::

    [Unit]
    Description=24/7 RSS Fetcher
    Requires=network-online.target
    After=network-online.target

    [Service]
    Type=simple
    User=<user>
    Group=<user>
    WorkingDirectory=/home/<user>/.rssbot
    ExecStart=/home/<user>/.local/pipx/venvs/rssbot/bin/rssbotd
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target


then run this

::

    $ mkdir ~/.rssbot
    $ sudo systemctl enable rssbot --now

default channel/server is #rssbot on localhost


FILES

::

    ~/.rssbot
    ~/.local/bin/rssbot
    ~/.local/bin/rssbotd
    ~/.local/pipx/venvs/rssbot/


AUTHOR

::

    Bart Thate <bthate@dds.nl>


COPYRIGHT

::

    RSSBOT is Public Domain.
