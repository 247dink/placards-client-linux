#!/bin/sh -x

# TODO: not sure if this is needed.
CHROME_USER="${CHROME_USER:-orangepi}"
CHROME_USER_HOME="$(eval echo ~${CHROME_USER})"
EXEC_NAMES="chrome google-chrome chromium chromium-browser"
CONFIG_PATH="${CONFIG_PATH:-${CHROME_USER_HOME}/.placards.ini}"
CHROME_PROFILE_DIR="${CHROME_PROFILE_DIR:-/var/tmp/placards}"

mkdir -p "${CHROME_PROFILE_DIR}"
chown -R ${CHROME_USER} "${CHROME_PROFILE_DIR}"

# Try to find chrome executable...
for EXEC_NAME in "${EXEC_NAMES}"; do
    CHROME_BIN_PATH=$(which ${EXEC_NAME})
    if [ ! -z "${CHROME_BIN_PATH}" ]; then
        break;
    fi
done

if [ -z "${CHROME_BIN_PATH}" ]; then
    apt install -y chromium-browser
    CHROME_BIN_PATH=$(which chromium-browser)
fi

if ! which pip; then
    apt install -y python3-pip
fi

echo EOF > "${CONFIG_PATH}" << EOF
[placards]
server_url=https://fishers.facman.site/
profile_dir=${CHROME_PROFILE_DIR}
chrome_path=${CHROME_BIN_PATH}
EOF
chown ${CHROME_USER} ${CONFIG_PATH}

echo placards \& > "${CHROME_USER_HOME}/.xinitrc"
chown ${CHROME_USER} "${CHROME_USER_HOME}/.xinitrc"

if [ ! -f setup.py ]; then
    pip install https://github.com/247dink/placards-client-linux/@master#egg=placards_client
else
    pip install .
fi
