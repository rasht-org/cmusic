import gradio as gr
from dotenv import dotenv_values
from adapters.lyricsify_adapter import LyricsifyAdapter
from adapters.json_adapter import JSONAdapter
from adapters.lrc_adapter import LRCAdapter
from pick import pick
from classes.project import Project
from classes.lyric import Lyric
import json
import os


# Load main config
config = dotenv_values(".env")
config['DEBUG'] = (config['DEBUG'] == "True")
urlAdapters = [
    LyricsifyAdapter()
]
lyric = None
lyric_options = []
project = Project()

# Search for music lyric in websites
def search_for_music(keyword: str):
    global lyric, lyric_options
    lyrics = []
    for adapter in urlAdapters:
        adapter_lyrics = adapter.searchLyrics(keyword=keyword)
        lyrics = lyrics + adapter_lyrics
    lyric_options = lyrics
    return gr.Dropdown.update(choices=[*map(lambda lyric: str(lyric), lyrics)])


# Fetch selected lyric
def fetch_music(option: str):
    global lyric
    if option:
        for lyric_option in lyric_options:
            if option == str(lyric_option):
                lyric = lyric_option
                break
    if lyric:
        lyric.download()
        return lyric.__text__(), lyric.__json__()
    return 'Lyric not found, Please search for a music first and then select music from dropdown list. Also you can add lyric manualy in \"Generate prompt\" tab', ''


def generate_prompt(lyric_text: str, lyric_type: str, fps: int = 15, shift: int = -5, possitives: str = '', negatives: str = ''):
    if lyric_type == 'Json lyric (default)':
        adapter = JSONAdapter()
    else:
        adapter = LRCAdapter()
    input_lyric = Lyric('Custom lyric', lyric_text, adapter)
    input_lyric.download()
    if len(possitives) > 0:
        input_lyric.append_positives(possitives)
    if len(negatives) > 0:
        input_lyric.append_negatives(negatives)
    if fps:
        fps = int(fps)
        if fps > 0:
            project.fps = fps
    if shift:
        shift = int(shift)
        project.frame_shift = shift
    
    # Generate prompts
    prompts = input_lyric.__prompt__()
    transformed_prompts = project.transform(prompts=prompts)
    return json.dumps(transformed_prompts, indent=4, sort_keys=True)
            


with gr.Blocks(title='CMusic Script') as blocks:
    
    gr.Markdown(
        """
        # CMusic script
        
        Please first search for your music lyric in \"Find lyric\" tab and then move to \"Generate prompt\" tab.
        
        You can also add timed lyric manualy in \"Generate prompt\" tab.
        """
    )
    
    with gr.Tab("Find lyric"):
        name_input = gr.Textbox(label='Music title or artist name')
        search_button = gr.Button("Search")
        music_options = gr.Dropdown(['Use search to find music lyrics first ...'], label="Searched music lyrics")
        fetch_button = gr.Button("Fetch selected lyric")
        lyric_output = gr.JSON(label='Lyric')
        
    with gr.Tab("Generate prompt"):
        gr.Markdown(
            """
            Lyric input is fetched from \"Find music\" tab. You can update it or even add your custom lyric here
            """
        )
        lyric_type_input = gr.Radio(label='Lyric text format', info='If you don\'t know about lyric formats set this to default', choices=['Json lyric (default)', '.lrc file format'], value='Json lyric (default)')
        lyric_input = gr.Textbox(label='Lyric', lines=10, info='A map of lyric lines, key: time in seconds(float), value: lyric line', value='{}')
        fps_input = gr.Textbox(label='FPS', info='Output video frames per second (default: 15 fps)', value='15')
        shift_input = gr.Textbox(label='Shift frames', info='number of frames to shift starting frame of each lyric line (default: -5 frames)', value='-5')
        positives_input = gr.Textbox(label='Global positive prompts', lines=5, info='Add additional positive prompts', value='')
        negatives_input = gr.Textbox(label='Global negative prompts', lines=5, info='Add additional negative prompts', value='')
        generate_button = gr.Button("Generate")
        prompt_output = gr.JSON(label='Output | Generated prompts')
        
    search_button.click(search_for_music, inputs=name_input, outputs=music_options)
    fetch_button.click(fetch_music, inputs=music_options, outputs=[lyric_output, lyric_input])
    generate_button.click(generate_prompt, inputs=[lyric_input, lyric_type_input, fps_input, shift_input, positives_input, negatives_input], outputs=prompt_output)
        
blocks.launch(share=True)