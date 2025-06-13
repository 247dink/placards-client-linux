#!/bin/sh -x

EXEC_NAMES="chrome google-chrome chromium chromium-browser"
CONFIG_PATH="${CONFIG_PATH:-${HOME}/.placards/config.ini}"
CHROME_PROFILE_DIR="${CHROME_PROFILE_DIR:-${HOME}/.placards/profile/}"

mkdir -p "${CHROME_PROFILE_DIR}"
chown -R ${USER} "${CHROME_PROFILE_DIR}"

# Try to find chrome executable...
for EXEC_NAME in "${EXEC_NAMES}"; do
    CHROME_BIN_PATH=$(which ${EXEC_NAME})
    if [ ! -z "${CHROME_BIN_PATH}" ]; then
        break;
    fi
done

if [ -z "${CHROME_BIN_PATH}" ]; then
    sudo apt install -y chromium-browser
    CHROME_BIN_PATH=$(which chromium-browser)
fi

if ! which pip; then
    sudo apt install -y python3-pip
fi

cat > "${CONFIG_PATH}" << EOF
[placards]
server_url=https://fishers.facman.site/
profile_dir=${CHROME_PROFILE_DIR}
chrome_path=${CHROME_BIN_PATH}
EOF

echo placards \& > "${HOME}/.xinitrc"

if [ ! -f setup.py ]; then
    sudo pip install git+https://github.com/247dink/placards-client-linux/@master#egg=placards

else
    sudo pip install .

fi