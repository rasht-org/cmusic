from rich import print
from dotenv import dotenv_values
from adapters.lyricsify_adapter import LyricsifyAdapter


# Load main config
config = dotenv_values(".env")
config['DEBUG'] = (config['DEBUG'] == "True")
urlAdapters = [
    LyricsifyAdapter()
]


# Read music name from user input
def select_music():
    print("[bold magenta]CMusic script[/bold magenta]", "[bold red]| Debug[/bold red]" if config['DEBUG'] else "")
    print("please input music title or artist name to search:")
        
    if config['DEBUG'] : search_term = 'as it was'
    else: search_term = input()
    print("[yellow]searching for %s ...[/yellow]" % search_term)
    return search_term


# Search for music lyric in websites
def search_for_music(keyword):
    found = []
    for adapter in urlAdapters:
        lyrics = adapter.searchLyrics(keyword=keyword)
        print(lyrics)
    

def main():
    term = select_music()
    if term:
        search_for_music(term)

if __name__ == "__main__":
    main()
