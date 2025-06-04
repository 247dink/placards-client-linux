import logging
import asyncio

from pyppeteer import launch

from placards import config
from placards.errors import ConfigError


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


async def chrome(chrome_bin, profile_dir):
    browser = await launch(
        headless=False,
        args=[
            # '--no-sandbox',
            '--start-maximized',
            '--start-fullscreen',
            '--no-default-browser-check',
        ],
        ignoreDefaultArgs=["--enable-automation"],
        # dumpio=True,
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
    # await page.keyboard.press('F11')
    await page.screenshot({
        'type': 'png',
    })


async def main():
    LOGGER.debug('Loading web client...')

    try:
        url = config.SERVER_URL
        chrome_bin = config.CHROME_BIN_PATH
        profile_dir = config.PROFILE_DIR

    except ConfigError as e:
        LOGGER.error(f'You must configure {e.args[0]} in placards.ini!')
        return

    browser, page = await chrome(chrome_bin, profile_dir)
    await goto(page, url)

    while not page.isClosed():
        await asyncio.sleep(0.1)

    await browser.close()


asyncio.run(main())
