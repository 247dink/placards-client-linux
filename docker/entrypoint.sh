#!/bin/bash -x

dbus-daemon --system

run_chrome() {
    touch ~/.Xauthority
    xauth add :0  MIT-MAGIC-COOKIE-1  ecdc511b6ffe69772fb1dd18290dceea
    python3 -m placard
}

sudo -H -u dsign bash -c "$(declare -f run_chrome); run_chrome"
