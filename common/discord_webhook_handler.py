import asyncio
import aiohttp
import logging

class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url
        self.loop = asyncio.get_event_loop()

    async def async_emit(self, record):
        try:
            message = self.format(record)
            data = {
                "content": message
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=data) as resp:
                    pass

        except Exception as e:
            self.handleError(record)

    def emit(self, record):
        asyncio.ensure_future(self.async_emit(record))
