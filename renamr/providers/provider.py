from bs4 import BeautifulSoup as bs
from requests import Response, get


HEAD = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64) Gecko/20100101 Firefox/114.0',
}


class Provider:
    '''
    Basic, but useful methods for providers
    '''

    @classmethod
    def request(cls, url: str, header: dict = dict()) -> Response:
        '''
        Send get request to url, return response

        Args:
            url (str): Url to send get request
            header (dict): Header information

        Returns:
            Response: Get response from provided url
        '''

        if not header:  # Use default header if none passed in
            header = HEAD
        try:
            req = get(
                url=url,
                timeout=10,
                headers=header
            )
        except ConnectionError as e:
            #  Error getting info, may be max retries
            print(e)
            pass
        return req

    @classmethod
    def request_json(cls, url: str, header: dict | None = None) -> dict:
        '''
        Get url and header, return json object

        Args:
            url (str): Url to send get request
            header (dict): Header information

        Returns:
            dict: Get request returned as dictionary
        '''

        return cls.request(url=url, header=header).json()

    @classmethod
    def soup_me(cls, url: str, header: dict) -> bs:
        '''
        Using url and header, get html soup for parsing

        Args:
            url (str): Url to send get request
            header (dict): Header information

        Returns:
            bs: BeautifulSoup object to parse through
        '''

        req = cls.request(url=url, header=header)
        soup = bs(req.content, 'html.parser')
        return soup
