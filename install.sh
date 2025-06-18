#!/bin/sh -x

BRANCH="${BRANCH:-master}"
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

if ! which unclutter; then
    sudo apt install -y unclutter
fi

cat > "${CONFIG_PATH}" << EOF
[placards]
server_url=https://fishers.facman.site/placards/
profile_dir=${CHROME_PROFILE_DIR}
chrome_bin_path=${CHROME_BIN_PATH}
ignore_certificate_errors=true
EOF

cat > "${HOME}/.config/autostart/placards.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Placards
Exec=python3 -m placards
Terminal=false
EOF

# NOTE: Old method
# echo "python3 -m placards \&" > "${HOME}/.xinitrc"

if [ -f setup.py ]; then
    sudo pip install .

else
    sudo pip install git+https://github.com/247dink/placards-client-linux/@${BRANCH}#egg=placards

fi
