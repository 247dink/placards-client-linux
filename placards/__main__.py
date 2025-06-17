import os
import shlex
import shutil
import subprocess
import logging
import asyncio

from pyppeteer import launch

from placards import config
from placards.errors import ConfigError


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())
STARTUP = [
    # Hide mouse cursor.
    'unclutter',

    # Disable screen blanking and screensaver.
    'xset s noblank',
    'xset s off',
    'xset -dpms',

    # Ensure any potential errors are not display when Chrome starts.
    'sed -i \'s/"exited_cleanly":false/"exited_cleanly":true/\' /home/$USER/.config/chromium/Default/Preferences'
    'sed -i \'s/"exit_type":"Crashed"/"exit_type":"Normal"/\' /home/$USER/.config/chromium/Default/Preferences',
]


async def chrome(chrome_bin, profile_dir, debug=False):
    "Launch Chrome browser and navigate to placards server."
    args = [
        '--start-maximized',
        '--start-fullscreen',
        '--no-default-browser-check',
        '--autoplay-policy=no-user-gesture-required',
    ]
    if config.getbool('IGNORE_CERTIFICATE_ERRORS', False):
        args.append('--ignore-certificate-errors')
    if not debug:
        args.extend([
            '--noerrdialogs',
            '--disable-infobars',
            '--kiosk',
        ])
    browser = await launch(
        headless=False,
        args=args,
        ignoreDefaultArgs=["--enable-automation"],
        dumpio=debug,
        executablePath=chrome_bin,
        userDataDir=profile_dir,
        defaultViewport=None,
        autoClose=False,
    )
    pages = await browser.pages()
    if len(pages):
        page = pages[0]
    else:
        page = await browser.newPage()
    return browser, page


async def goto(page, url):
    page.setDefaultNavigationTimeout(0)
    await page.goto(url, waitUntil='networkidle2')
    await page.screenshot({
        'type': 'png',
    })


def setup(profile_dir):
    "Set up directories, permission, environment."
    # Ensure profile directory exists.
    try:
        os.makedirs(profile_dir)

    except FileExistsError:
        pass

    # Run startup commands to prepare X.
    for command in STARTUP:
        cmd = shlex.split(command)
        bin = shutil.which(cmd[0])
        if not bin:
            LOGGER.warning('Could not find program', cmd[0])
            continue
        LOGGER.debug('Running startup command', [bin, *cmd[1:]])
        subprocess.Popen([bin, *cmd[1:]])


async def main():
    "Main entry point."
    log_level_name = config.get('LOG_LEVEL', 'ERROR').upper()
    log_level = getattr(logging, log_level_name)
    debug = (log_level_name == 'DEBUG')

    root = logging.getLogger()
    root.addHandler(logging.StreamHandler())
    root.setLevel(log_level)

    LOGGER.debug('Loading web client...')

    try:
        url = config.SERVER_URL
        chrome_bin = config.CHROME_BIN_PATH
        profile_dir = config.PROFILE_DIR

    except ConfigError as e:
        LOGGER.error(f'You must configure {e.args[0]} in config.ini!')
        return

    setup(profile_dir)

    browser, page = await chrome(chrome_bin, profile_dir, debug)
    try:
        await goto(page, url)

        while not page.isClosed():
            await asyncio.sleep(0.1)

    finally:
        await browser.close()


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())

        except Exception:
            LOGGER.exception('Error running Placards, restarting...')
