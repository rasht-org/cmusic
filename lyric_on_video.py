from moviepy.editor import *
import json

audioclip = AudioFileClip("files/input.mp3")
clip = VideoFileClip("files/input.mp4")
clip = clip.set_audio(audioclip)

text_clips = []

with open('files/lyric.json') as file:
    lyric = json.load(file)
    time_keys = list(lyric.keys())
    for index, time in enumerate(lyric):
        duration = 10
        if len(time_keys) > index + 1:
            duration = float(time_keys[index+1]) - float(time)
        txt_clip = TextClip(
            lyric[time],
            font='IRANSansX-ExtraBold',
            fontsize=40,
            color='white',
            kerning=-2, interline=-1,
            stroke_width=1.5,
            stroke_color='black',
            method='caption',
            align='north',
            size=clip.size
        )
        txt_clip = txt_clip.set_pos(("center", "top")).set_duration(
            duration).set_start(float(time)).crossfadein(0.5).margin(top=50, opacity=0)
        text_clips.append(txt_clip)

video = CompositeVideoClip([
    clip,
    *text_clips
])
video.write_videofile("files/output.mp4")
