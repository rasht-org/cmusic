from adapters.url_adapter import UrlAdapter
import re

class LRCAdapter(UrlAdapter):
    
    def searchLyrics(self, keyword: str):
        return []
        
    
    def getLyric(self, link: str):
        lyric = {}
        lyric_text = link
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