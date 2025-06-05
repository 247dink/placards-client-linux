#!/bin/bash -x

rm -rf /run/dbus/pid
dbus-daemon --system

sudo -H -u placards bash -c "touch ~/.Xauthority"
sudo -H -u placards bash -c "xauth add :0  MIT-MAGIC-COOKIE-1  ${XAUTH_COOKIE}"
# sudo -H -u dsign bash -c "python3 -m placard"
