import asyncio
import concurrent.futures
import logging
import requests

class DiscordWebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url
        self.loop = asyncio.new_event_loop()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def emit(self, record):
        try:
            message = self.format(record)
            data = {
                "content": message
            }

            def send_request():
                requests.post(self.webhook_url, data=data)

            future = self.loop.run_in_executor(self.executor, send_request)

        except Exception as e:
            self.handleError(record)
