from adapters.url_adapter import UrlAdapter
from classes.lyric import Lyric
from bs4 import BeautifulSoup
import requests
import re

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
                        'https://www.lyricsify.com' + name['href'] + '',
                        self
                    )
                )
            return results
        else: 
            return []
        
    
    def getLyric(self, link: str):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
        headers = {'User-Agent': user_agent}
        result = requests.get(link, headers=headers)
        lyric = {}
        if result.status_code == 200:
            content = BeautifulSoup(result.content, 'html.parser')
            lyric_id = int(link.split('.')[3])
            lyric_element = content.find("div", id="lyrics_%s_details" % lyric_id)
            if lyric_element:
                lyric_text = lyric_element.text
                lyric_lines = lyric_text.split('\n')
                for lyric_line in lyric_lines:
                    if (re.match(r'\[\d{2}:\d{2}.[0-9]+\]', lyric_line)):
                        pack = lyric_line.split(']')
                        
                        if re.match(r'\[\d{2}:\d{2}.[0-9]+', pack[1]) or re.match(r':', pack[1]):
                            continue
                        
                        pack[1] = pack[1].replace('"', '').strip()
                        if len(pack[1]) < 1:
                            continue
                        
                        timestr = pack[0].replace('[', '')
                        time_parts = timestr.split(':')
                        # second_parts = time_parts[1].split('.')
                        minute = int(time_parts[0])
                        second = float(time_parts[1])
                        # milisecond = int(second_parts[1])
                        time = str(round((minute * 60) + second, 2))
                        lyric[time] = pack[1]
        return lyric