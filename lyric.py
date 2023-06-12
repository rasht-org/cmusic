from url_adapter import UrlAdapter

class Lyric:
    adapter: UrlAdapter
    name: str
    link: str
    params = {}
    
    def __init__(self, name: str, link: str, adapter: UrlAdapter, params = {}) -> None:
        self.name = name
        self.link = link
        self.adapter = adapter
        self.params = params
        
    def __str__(self):
        return "Lyric %s | Adapter: %s" % (self.name, self.adapter.name)
    
    def __repr__(self):
        return self.__str__()