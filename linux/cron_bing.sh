#!/bin/bash

PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)
export DISPLAY=:0.0

/usr/bin/python /home/mayuan/PROJECTS/Bing_wallpaper/getimg.py
