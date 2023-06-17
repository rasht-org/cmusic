from adapters.url_adapter import UrlAdapter
import json

class JSONAdapter(UrlAdapter):
    
    def searchLyrics(self, keyword: str):
        return []
        
    
    def getLyric(self, link: str):
        return json.loads(link)