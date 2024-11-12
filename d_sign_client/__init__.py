import aiohttp


SERVER_URL = ''


class DSignClient:
    def __init__(self, server_url=SERVER_URL):
        self.server_url = server_url

    async def playlist(self):
        yield ('http://localhost:8000/', 60)
