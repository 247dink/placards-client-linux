#!/bin/bash -x

rm -rf /run/dbus/pid
dbus-daemon --system

if [ ! -z "${PROFILE_DIR}" ]; then
    chown -R placards ${PROFILE_DIR}
fi

sudo -H -u placards bash -c "touch ~/.Xauthority"
sudo -H -u placards bash -c "xauth add :0  MIT-MAGIC-COOKIE-1  ${XAUTH_COOKIE}"

sudo -H -u placards \
    PROFILE_DIR=${PROFILE_DIR} \
    IGNORE_CERTIFICATE_ERRORS=${IGNORE_CERTIFICATE_ERRORS} \
    DEBUG=true \
    LOG_LEVEL=DEBUG \
    bash -c "placards"
