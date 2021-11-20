import random

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
plot_color = color_list[0]

plt.style.use('dark_background')
sns.set_context("notebook", rc={"font.size":1,
                                "axes.titlesize":18,
                                "axes.labelsize":18})
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
fig, ax = plt.subplots()
sns.despine(right=True, top=True)


def make_frame(t):
    """
    New plot for each frame.

    Make updated version of the plot for each frame.
    """
    ax.clear()
    fig.autofmt_xdate()
    ax.set_ylabel(y_label)

    ax.plot_date(x, np.minimum(y * t * 4 / WAIT_UNTIL_TEXT, y), linestyle='solid', linewidth=5, marker='', color=plot_color)
    ax.set_ylim(0, max(y) * 1.1)
    
    return mplfig_to_npimage(fig)


def move_headline(t):
    """
    Fly-in of headline.
    """
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), HEADLINE_Y)
    else:
        return (PADDING_LEFT, HEADLINE_Y)

def move_text(t):
    """
    Fly-in of data observation.
    """
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), TEXT_Y)
    elif 2 <= t < WAIT_UNTIL_TEXT:
        return (PADDING_LEFT, TEXT_Y)
    else:
        return (linear_out(t, PADDING_LEFT, WAIT_UNTIL_TEXT), TEXT_Y)

def move_text2(t):
    """
    Fly-in of observation explanation.
    """
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT), TEXT_Y)
    else:
        return (PADDING_LEFT, TEXT_Y)

def move_plot(t):
    """
    Fly-in of plot.
    """
    if 0 <= t < 2:
        return (linear_in(t, PADDING_LEFT_PLOT), PLOT_Y)
    else:
        return (PADDING_LEFT_PLOT, PLOT_Y)

def linear_in(t, padding):
    return min(padding, int(-VIDEO_WIDTH + VIDEO_WIDTH*t))

def linear_out(t, padding, wait):
    return padding + VIDEO_WIDTH*(t-wait)


def get_audio(txt, filename):
    """
    Text-to-Speech generation.

    Creation of AudioFileClip using google Text-to-Speech.
    """
    tts = gTTS(txt)
    tts.save(f'{filename}.mp3')
    audio = AudioFileClip(f'{filename}.mp3')

    return audio


def intro_video(txt):
    """
    Intro video generation.

    Creation of intro video with intro text, audio, and background.
    """
    txt_clip = TextClip(textwrap.fill(txt, 22), font=FONT, color='white', fontsize=34, align='west')
    txt_clip = txt_clip.set_position(move_headline)
    audio = get_audio(txt, 'intro')

    total_duration = audio.duration + AUDIO_BUFFER

    background = ImageClip('bg.png', duration=total_duration).resize((VIDEO_WIDTH, VIDEO_HEIGHT//5))
    background = background.set_position((0, VIDEO_HEIGHT - background.h))
    video = CompositeVideoClip([background, txt_clip], size=VIDEO_SIZE).set_duration(total_duration)
                                                                               
    return video, audio, total_duration


def plot_video(txt1, txt2):
    """
    Plot video generation.

    Creation of plot video with observation, plot, explanation, audio, and background.
    """
    global plot_color
    plot_color = random.choice(color_list)

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

    background = ImageClip('bg.png', duration=total_duration).resize((VIDEO_WIDTH, VIDEO_HEIGHT//5))
    background = background.set_position((0, VIDEO_HEIGHT - background.h))
    
    video = CompositeVideoClip([background, txt_clip1, txt_clip2.set_start(audio1.duration), plot_clip], size=VIDEO_SIZE).set_duration(total_duration)
    audio = CompositeAudioClip([audio1, audio2.set_start(audio1.duration)])

    return video, audio, total_duration


def generate_line_story(plot_text1, plot_text2, intro_text=''):
    """
    Creation of entire line plot story.

    Creation of line plot story with 2 seperate videos (intro & data observation).
    """
    videos, audios, duration = [], [], 0
    if intro_text:
        v1, a1, d1 = intro_video(intro_text)
        videos.append(v1)
        audios.append(a1)
        duration += d1

    v2, a2, d2 = plot_video(plot_text1, plot_text2)
    if intro_text:
        v2 = v2.set_start(d1)
        a2 = a2.set_start(d1)
    videos.append(v2)
    audios.append(a2)
    duration += d2

    video = CompositeVideoClip(videos, size=VIDEO_SIZE).set_duration(duration)
    audio = CompositeAudioClip(audios)

    video.audio = audio
    return video
