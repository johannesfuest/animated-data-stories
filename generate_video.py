from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage
import textwrap
import numpy as np
import matplotlib.pyplot as plt
from gtts import gTTS
from pandas import Timestamp
import seaborn as sns

VIDEO_WIDTH, VIDEO_HEIGHT = VIDEO_SIZE = (500, 1000)
HEADLINE_Y = 300
TEXT_Y = 200
PLOT_Y = 'center'
PADDING_LEFT = 50
PADDING_LEFT_PLOT = 50
FONT = 'Helvetica-Bold'
AUDIO_BUFFER = 1

Violet = '#970a82'
Reddish = '#bb4a4e'
Orange = '#d57a27'
Yellow = '#f0ab00'

color_list = [Violet, Reddish, Orange, Yellow]
 
plt.style.use('dark_background')
sns.set_context("notebook", rc={"font.size":1,
                                "axes.titlesize":18,
                                "axes.labelsize":18})
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
fig, ax = plt.subplots()
sns.despine(right=True, top=True)


def make_frame(t):
    ax.clear()
    fig.autofmt_xdate()
    ax.set_ylabel(y_label)

    ax.plot_date(x, np.minimum(y * t * 4 / WAIT_UNTIL_TEXT, y), linestyle='solid', linewidth=5, marker='')
    ax.set_ylim(0, max(y) * 1.1)
    
    return mplfig_to_npimage(fig)


def move_headline(t):
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), HEADLINE_Y)
    else:
        return (PADDING_LEFT, HEADLINE_Y)

def move_text(t):
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), TEXT_Y)
    elif 2 <= t < WAIT_UNTIL_TEXT:
        return (PADDING_LEFT, TEXT_Y)
    else:
        return (linear_out(t, PADDING_LEFT, WAIT_UNTIL_TEXT), TEXT_Y)

def move_text2(t):
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), TEXT_Y)
    else:
        return (PADDING_LEFT, TEXT_Y)

def move_plot(t):
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT_PLOT), PLOT_Y)
    else:
        return (PADDING_LEFT_PLOT, PLOT_Y)

def linear_in(t, padding):
    return min(padding, int(-VIDEO_WIDTH + VIDEO_WIDTH*t))

def linear_out(t, padding, wait):
    return padding + VIDEO_WIDTH*(t-wait)


def get_audio(txt, filename):
    tts = gTTS(txt)
    tts.save(f'{filename}.mp3')
    audio = AudioFileClip(f'{filename}.mp3')

    return audio


def intro_video(txt):
    txt_clip = TextClip(textwrap.fill(txt, 20), font=FONT, color='white', fontsize=36, align='west')
    txt_clip = txt_clip.set_position(move_headline)
    audio = get_audio(txt, 'intro')

    total_duration = audio.duration + AUDIO_BUFFER

    background = ImageClip('bg.jpg', duration=total_duration).resize((VIDEO_WIDTH, VIDEO_HEIGHT//3))
    background = background.set_position((0, VIDEO_HEIGHT - background.h))
    video = CompositeVideoClip([background, txt_clip], size=VIDEO_SIZE).set_duration(total_duration)
                                                                               
    return video, audio, total_duration


def plot_video(txt1, txt2):
    audio1 = get_audio(txt1, 'txt1')

    global WAIT_UNTIL_TEXT
    WAIT_UNTIL_TEXT = audio1.duration

    txt_clip1 = TextClip(textwrap.fill(txt1, 25), font=FONT, color='white', fontsize=32, align='west')
    txt_clip1 = txt_clip1.set_position(move_text)

    audio2 = get_audio(txt2, 'txt2')
    
    global WAIT_UNTIL_TEXT2
    WAIT_UNTIL_TEXT2 = audio2.duration

    txt_clip2 = TextClip(textwrap.fill(txt2, 25), font=FONT, color='white', fontsize=32, align='west')
    txt_clip2 = txt_clip2.set_position(move_text)

    total_duration = audio1.duration + AUDIO_BUFFER + audio2.duration

    plot_clip = VideoClip(make_frame, duration=total_duration).set_position(move_plot)

    background = ImageClip('bg.jpg', duration=total_duration).resize((VIDEO_WIDTH, VIDEO_HEIGHT//3))
    background = background.set_position((0, VIDEO_HEIGHT - background.h))
    
    video = CompositeVideoClip([background, txt_clip1, txt_clip2.set_start(audio1.duration), plot_clip], size=VIDEO_SIZE).set_duration(total_duration)
    audio = CompositeAudioClip([audio1, audio2.set_start(audio1.duration)])

    return video, audio, total_duration


def generate_line_story(intro_text, plot_text1, plot_text2, x_data, y_data):
    global x
    global y
    x = x_data
    y = y_data
    
    v1, a1, d1 = intro_video(intro_text)
    v2, a2, d2 = plot_video(plot_text1, plot_text2)

    video = CompositeVideoClip([v1, v2.set_start(d1)], size=VIDEO_SIZE).set_duration(d1 + d2)
    audio = CompositeAudioClip([a1, a2.set_start(d1)])

    video.audio = audio
    return video