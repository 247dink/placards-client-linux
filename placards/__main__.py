import os
import json
import glob
import shlex
import shutil
import tempfile
import subprocess
import logging
import asyncio

from os.path import dirname, join as pathjoin

from pyppeteer import launch
from pyppeteer.errors import PageError

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
]
PREFERENCES_PATH = 'Default/Preferences'
LOADING_HTML = pathjoin(dirname(__file__), 'html/index.html')


async def getPages(browser, count):
    "Close all tabs, open and return requested number of new tabs."
    pages = []
    for page in await browser.pages():
        await page.close()
    for i in range(count):
        pages.append(await browser.newPage())
    return tuple(pages)


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
    load, page = getPages(browser, 2)
    return browser, load, page


def edit_json_file(path, **kwargs):
    "Change keys in .json file and save."
    try:
        with open(path, 'r') as f:
            o = json.load(f)
        for key, value in kwargs.items():
            o[key] = value
        with tempfile.NamedTemporaryFile('wt',
                                         prefix=dirname(path),
                                         delete=False) as f:
            json.dump(o, f)
            os.remove(path)
            os.rename(f.name, path)

    except Exception:
        LOGGER.exception('Error modifying JSON file: %s', path)


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
        subprocess.Popen(
            [bin, *cmd[1:]],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    for fn in glob.glob('Singleton*', root_dir=profile_dir):
        try:
            os.remove(fn)

        except Exception as e:
            LOGGER.warning(f'Could not delete Singleton file {fn}')

    # Clear away crash status from Chrome prefs.
    edit_json_file(
        pathjoin(profile_dir, PREFERENCES_PATH),
        exited_cleanly=True,
        exit_type='Normal',
    )


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

    browser, load, page = await chrome(chrome_bin, profile_dir, debug)

    await load.goto(LOADING_HTML)
    await load.bringToFront()

    page.setDefaultNavigationTimeout(0)

    try:
        # We need this page to load, so we will keep trying until it works.
        while True:
            try:
                await page.goto(url, waitUntil='networkidle2')
                await page.bringToFront()
                break

            except PageError:
                LOGGER.exception('Error loading %s', url)
                asyncio.sleep(5.0)
                LOGGER.info('Trying again...')

        # Once the page is loaded, wait for it to close.
        while not page.isClosed():
            await asyncio.sleep(0.1)

    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
