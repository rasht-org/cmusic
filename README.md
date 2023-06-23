# See Music

A python script to convert music lyric files into stable diffusion prompts

## Run on colab

You can run this project on colab. It uses gradio ui and needs no installation on your local machine

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rasht-org/cmusic/blob/main/CMusic.ipynb)

## Install dependencies

```shell
    pip install -r requirements.txt
```

## Run with gradio web ui

```shell
    python cmusic_gradio.py
```

## Run on cli

```shell
    python cmusic.py
```

Follow prompts in cli to download lyric for your music and convert it into stable diffusion prompts

![alt text](https://github.com/rasht-org/cmusic/blob/main/sample.png?raw=true)

## Merge video, audio with lyric caption

Put your files in files directory with following names:

- input.mp4
- input.mp3
- lyric.json

Run this script to merge them into one clip, You will need to install and configure ImageMagick library first.

```shell
python lyric_on_video.py
```

The file will be generated at:

- output.mp4

## Tested Environment

- Python 3
- Deforum extension with automatic1111 web ui

## Development notes

You can add other music website databases. It is done by defining your custom adapter in adapters folder and implementing adapters.url_adapter interface.

Then add your new adapter class to adapters list initialzed at the begining of cmusic and cmusic_gradio python files.
