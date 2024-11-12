import logging
import asyncio

import pyppeteer
from pyppeteer import launch

from d_sign_client import DSignClient


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())
SERVER_URL = 'https://www.247dink.com'


async def chrome():
    browser = await launch(
        headless=False,
        args=[
            '--start-maximized',
            '--start-fullscreen',
            '--no-default-browser-check',
        ],
        ignoreDefaultArgs=["--enable-automation"],
        executablePath='/usr/bin/google-chrome',
        userDataDir='/home/btimby/.local/share/pyppeteer/.dev_profile/tmpo2vx5cr7',
        defaultViewport=None,
        autoClose=True,
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
    #await page.keyboard.press('F11')
    await page.screenshot({
        'type': 'png',
    })


async def main():
    client = DSignClient()
    playlist = client.playlist()
    browser, page = await chrome()

    async for url, delay in client.playlist():
        LOGGER.debug('Showing %s for %i seconds', url, delay)
        await goto(page, url)
        await asyncio.sleep(delay)

    await browser.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
