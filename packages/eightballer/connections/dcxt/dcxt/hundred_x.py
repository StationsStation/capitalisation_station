"""
Implements the HundredXClient class, which is a client for the HundredX API.
"""


class HundredXClient:
    """
    A client for the HundredX API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises the client.

        :param api_key: The API key.
        :param api_secret: The API secret.
        """
        del args, kwargs

    async def fetch_markets(self, *args, **kwargs):
        """
        Fetches the markets.

        :return: The markets.
        """
        del args, kwargs

    async def fetch_tickers(self, *args, **kwargs):
        """
        Fetches the tickers.

        :return: The tickers.
        """
        del args, kwargs

    async def fetch_ticker(self, *args, **kwargs):
        """
        Fetches a ticker.

        :return: The ticker.
        """
        del args, kwargs
