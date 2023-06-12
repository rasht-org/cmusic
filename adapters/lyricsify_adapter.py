from url_adapter import UrlAdapter
from lyric import Lyric
from bs4 import BeautifulSoup
import requests

class LyricsifyAdapter(UrlAdapter):
    
    name = "Lyricsify"
    url = "https://www.lyricsify.com/search?q=%s"
    
    def searchLyrics(self, keyword: str):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
        headers = {'User-Agent': user_agent}
        result = requests.get((self.url % keyword).replace(' ', '+'), headers=headers)
        if result.status_code == 200:
            content = BeautifulSoup(result.content, 'html.parser')
            names = content.find_all("a", class_="title")
            results = []
            for name in names:
                results.append(
                    Lyric(
                        name.contents[0], 
                        'https://www.lyricsify.com/' + name['href'] + '?download',
                        self
                    )
                )
            return results
        else: 
            return []