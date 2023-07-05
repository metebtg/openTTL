from random import choice
import json
import re
from urllib.parse import urljoin, urlencode, urlparse, urlunparse
import requests

from .utils import get_path

USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
]

# with open(f'{get_path()}/datas/phraseList.json', 'r', encoding='utf-8') as file:
#     PHRASE_LIST = json.load(file)

class TranslatorDuck:
    base_url = 'https://duckduckgo.com/'
    headers = {'user-agent': choice(USERAGENTS)}

    def __init__(self):
        self.vqd = self._get_vqd()

    def _get_vqd(self, timeout: int = 5) -> str:
        """Return vqd as string. Required for Duckduckgo api."""
        
        # For getting random vqd...
        query_string = 'translate'
        query_params = {'q': query_string}       

        # Build req url
        vqd_req_url = urlunparse(
            urlparse(self.base_url)._replace(query=urlencode(query_params))
        )

        vqd_res = requests.get(vqd_req_url, headers=self.headers, timeout=timeout)      

        vqd: str = ''

        vqd_list = re.findall('vqd="([^"]*)"', vqd_res.text)
        if vqd_list:
            vqd = vqd_list[0]

        return vqd
    
    def _change_vqd(self):
        self.vqd = self._get_vqd()

    def _change_useragent(self):
        new_useragent = choice(USERAGENTS)

        while self.headers['user-agent'] == new_useragent:
            new_useragent = choice(USERAGENTS)

        self.headers['user-agent'] = new_useragent

    def translate(self, text: str, src: str = '', dest: str = 'en', timeout: int = 5, new_vqd: bool = False, new_useragent: bool = False) -> str:
        """Return translated text."""

        ## I do not know what is vqd, but it seems like an identifier,
        # cause its required for translation, let user can reset it.
        if new_vqd:
            self._change_vqd()
        if new_useragent:
            self._change_useragent()
            

        vqd = self.vqd

        if not vqd:
            return ''

        # Max lenth is 1000 for data
        data = text.strip()[:1000]

        # Set query params
        query_params = {
            'vqd': vqd,
            'query': 'translate',
            'to': dest,
        }
        # when from is not exist, duckduckgo uses auto detection for it
        if src:
            query_params.update({'from': src})

        # build url from base_url
        req_url = urlunparse(
            urlparse(self.base_url)._replace(query=urlencode(query_params), path='translation.js')
        )
        
        res = requests.post(req_url, data=data, timeout=timeout, headers=self.headers)
        return res.json()


if __name__ == '__main__':
    duck = TranslatorDuck()
    print(duck.translate('hello'))
      
