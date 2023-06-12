from rich import print
from requests import get
from dotenv import dotenv_values
from json import decoder

config = dotenv_values(".env")

config['DEBUG'] = (config['DEBUG'] == "true")
urls_file = open('urls.json')
with open('urls.json'):
    print()
urls = decoder(urls_file)
print("urls", urls)

def select_music():
    # Get search keyword
    print("[bold magenta]CMusic script[/bold magenta]", "[bold red]| Debug[/bold red]" if config['DEBUG'] else "")
    print("please input music title or artist name to search:")
        
    if config['DEBUG'] : search_term = 'as it was'
    else: search_term = input()
    print("[yellow]searching for %s ...[/yellow]" % search_term)


def search_for_music(keyword):
    pass

def main():
    term = select_music()
    if term:
        search_for_music(term)

if __name__ == "__main__":
    main()
