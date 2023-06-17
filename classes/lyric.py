from adapters.url_adapter import UrlAdapter
import json

class Lyric:
    
    adapter: UrlAdapter
    name: str
    link: str
    positives = {}
    negatives = {}
    
    
    def __init__(self, name: str, link: str, adapter: UrlAdapter) -> None:
        self.name = name
        self.link = link
        self.adapter = adapter
        self.positives = {}
        self.negatives = {}
        
        
    def download(self):
        self.positives = self.adapter.getLyric(self.link)
        for (index, value) in enumerate(self.positives):
            self.negatives[value] = ''
        
        
    def append_positives(self, positives):
        terms = self.clean_terms(positives)
        for (index, value) in enumerate(self.positives):
            self.positives[value] = self.positives[value] + ', ' + ','.join(terms)
            
            
    def append_negatives(self, negatives):
        terms = self.clean_terms(negatives)
        for (index, value) in enumerate(self.negatives):
            self.negatives[value] = self.negatives[value] + ','.join(terms)
        
        
    def clean_terms(self, terms: str):
        cleaned_terms = []
        terms = terms.split(',')
        for term in terms:
            cleaned_terms.append(term.strip())
        return cleaned_terms
    
    def __prompt__(self):
        prompts = {}
        for (index, value) in enumerate(self.positives):
            prompts[value] = self.positives[value] + ' --neg ' + self.negatives[value]
        return prompts
    
    def __json__(self):
        return json.dumps(self.positives, indent=4, sort_keys=False)
        
        
    def __str__(self):
        return "Lyric %s | Adapter: %s" % (self.name, self.adapter.name)
    
    
    def __repr__(self):
        return self.__str__()
    
    def __text__(self):
        return self.positives