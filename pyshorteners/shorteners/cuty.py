import json
from ..base import BaseShortener
from ..exceptions import BadAPIResponseException, ExpandingErrorException


class Shortener(BaseShortener):
    """
    Cuty.io shortener implementation

    Args:
        api_key (str): cuty.io API key

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_key='YOUR_KEY')
        >>> s.cuty.short('http://www.google.com')
        'https://cutty.app/TEST'
    """

    api_url = "https://api.cuty.io"

    def short(self, url, clean_url=True):
        """Short implementation for Cuty.io
        Args:
            url (str): the URL you want to shorten

        Returns:
            str: The shortened URL.

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
                status code on API response.
            ShorteningErrorException: If the API Returns an error as response
        """

        self.clean_url(url)
        expand_url = f"{self.api_url}/full"
        params = {"token": self.api_key, "url": url}
        response = self._post(expand_url, params=params)
        if not response.ok:
            raise ExpandingErrorException(response.text)

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise BadAPIResponseException("API response could not be decoded")

        return data["data"]["short_url"]