from rich import print
from dotenv import dotenv_values
from adapters.lyricsify_adapter import LyricsifyAdapter
from pick import pick
from classes.project import Project
import json
import os


# Load main config
config = dotenv_values(".env")
config['DEBUG'] = (config['DEBUG'] == "True")
urlAdapters = [
    LyricsifyAdapter()
]
lyric = None
project = Project()


# Read music name from user input
def select_music():
    print("[bold magenta]CMusic script[/bold magenta]", "[bold red]| Debug[/bold red]" if config['DEBUG'] else "")
    print("please input music title or artist name to search:")
        
    search_term = input()
    print("[yellow]searching for %s ...[/yellow]" % search_term)
    return search_term


# Search for music lyric in websites
def search_for_music(keyword):
    global lyric
    lyrics = []
    for adapter in urlAdapters:
        adapter_lyrics = adapter.searchLyrics(keyword=keyword)
        lyrics = lyrics + adapter_lyrics
    option, index = pick([*map(lambda lyric: str(lyric), lyrics)], "Select a lyric:")
    if option:
        lyric = lyrics[index]
        print("[green]%s[/green]" % lyric.name)
        lyric.download()
        
        
def additional_prompts():
    print("[cyan]Add additional positive prompts:[/cyan]")
    possitives = input()
    print("[magenta]Add additional negative prompts:[/magenta]")
    negatives = input()
    if lyric:
        if len(possitives) > 0:
            lyric.append_positives(possitives)
        if len(negatives) > 0:
            lyric.append_negatives(negatives)
    print("[cyan]Output video frames per second (default: 15 fps):")
    fps = input()
    if fps:
        fps = int(fps)
        if fps > 0:
            project.fps = fps
    print("[cyan]Shift frames, number of frames to shift starting frame of each lyric line (default: -5 frames):")
    shift = input()
    if shift:
        shift = int(shift)
        project.frame_shift = shift
            
            
def save():
    if lyric:
        if not os.path.exists('export/'):
            os.makedirs('export/')
        file_name = 'export/' + lyric.name.replace(':', '-').replace('.', '-') + '.json'
        with open(file_name, 'w') as file:
            prompts = lyric.__prompt__()
            transformed_prompts = project.transform(prompts=prompts)
            file.write(json.dumps(transformed_prompts, indent=4, sort_keys=True))
            print('[bold green]Your file is saved at %s[/bold green]' % file_name)
            file.close()
            

def main():
    term = select_music()
    if term:
        search_for_music(term)
        additional_prompts()
        save()
        

if __name__ == "__main__":
    main()
