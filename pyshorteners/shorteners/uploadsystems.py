import json
from ..base import BaseShortener
from ..exceptions import BadAPIResponseException, ExpandingErrorException


class Shortener(BaseShortener):
    """
    Upload.systems shortener implementation

    Args:
        api_key (str): upload.systems API key

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_key='YOUR_KEY')
        >>> s.uploadsystems.short('http://www.google.com')
        'https://uploadi.ng/TEST'
    """

    api_url = "https://api.upload.systems"

    def short(self, url, clean_url=True):
        """Short implementation for upload.systems
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
        expand_url = f"{self.api_url}/shortenurl"
        params = {"key": self.api_key, "url": url}
        response = self._post(expand_url, json=params)
        if not response.ok:
            response = response.json()
            raise ExpandingErrorException(response["displayMessage"])

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise BadAPIResponseException("API response could not be decoded")

        return data["shortUrl"]