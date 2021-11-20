from moviepy.editor import *
from moviepy.video.io.bindings import mplfig_to_npimage

import numpy as np
import matplotlib.pyplot as plt
from gtts import gTTS
from pandas import Timestamp

VIDEO_WIDTH, VIDEO_HEIGHT = VIDEO_SIZE = (500, 1000)
HEADLINE_Y = 300
TEXT_Y = 200
PLOT_Y = 500
PADDING_LEFT = 20
FONT = 'Helvetica-Bold'
AUDIO_BUFFER = 1

WAIT_UNTIL_TEXT, WAIT_UNTIL_TEXT2 = 0, 0

X, Y = np.array([]), np.array([])
fig, ax = plt.subplots()
def make_frame(t):
    ax.clear()
    ax.plot_date(X, Y, linestyle='solid')
    
    return mplfig_to_npimage(fig)

def move_headline(t):
    if 0 <= t < 2:
        return (linear_in(t), HEADLINE_Y)
    else:#if 2 <= t < WAIT_UNTIL:
        return (PADDING_LEFT, HEADLINE_Y)
    #else:
     #   return (linear_out(t, WAIT_UNTIL), HEADLINE_Y)

def move_text(t):
    if 0 <= t < 2:
        return (linear_in(t), TEXT_Y)
    elif 2 <= t < WAIT_UNTIL_TEXT:
        return (PADDING_LEFT, TEXT_Y)
    else:
        return (linear_out(t, WAIT_UNTIL_TEXT), TEXT_Y)

def move_text2(t):
    if 0 <= t < 2:
        return (linear_in(t), TEXT_Y)
    else:#if 2 <= t < WAIT_UNTIL_TEXT2:
        return (PADDING_LEFT, TEXT_Y)
    #else:
     #   return (linear_out(t, WAIT_UNTIL_TEXT2), TEXT_Y)

def move_plot(t):
    if 0 <= t < 2:
        return (linear_in(t), PLOT_Y)
    else:#if 2 <= t < (WAIT_UNTIL_TEXT + WAIT_UNTIL_TEXT2):
        return (PADDING_LEFT, PLOT_Y)
    #else: # > 4
      #  return (linear_out(t, WAIT_UNTIL_TEXT + WAIT_UNTIL_TEXT2), PLOT_Y)

def linear_in(t):
    return min(PADDING_LEFT, int(-VIDEO_WIDTH + VIDEO_WIDTH*t))

def linear_out(t, wait):
    return PADDING_LEFT + VIDEO_WIDTH*(t-wait)

def get_audio(txt, filename):
    tts = gTTS(txt)
    tts.save(f'{filename}.mp3')
    audio = AudioFileClip(f'{filename}.mp3')

    return audio

def intro_video(txt):
    txt_clip = TextClip(txt, font=FONT, color='white', fontsize=32, align='west')
    txt_clip = txt_clip.set_position(move_headline)

    audio = get_audio(txt, 'intro')

    total_duration = audio.duration + AUDIO_BUFFER

    background = ImageClip(np.full((VIDEO_HEIGHT, VIDEO_WIDTH, 3), 0), duration=total_duration)
    video = CompositeVideoClip([background, txt_clip], size=VIDEO_SIZE).set_duration(total_duration)
                                                                               
    return video, audio, total_duration

def plot_video(txt1, txt2):
    audio1 = get_audio(txt1, 'txt1')

    global WAIT_UNTIL_TEXT
    WAIT_UNTIL_TEXT = audio1.duration

    txt_clip1 = TextClip(txt1, font=FONT, color='white', fontsize=24, align='west')
    txt_clip1 = txt_clip1.set_position(move_text)

    audio2 = get_audio(txt2, 'txt2')
    
    global WAIT_UNTIL_TEXT2
    WAIT_UNTIL_TEXT2 = audio2.duration

    txt_clip2 = TextClip(txt2, font=FONT, color='white', fontsize=24, align='west')
    txt_clip2 = txt_clip2.set_position(move_text)

    total_duration = audio1.duration + AUDIO_BUFFER + audio2.duration

    plot_clip = VideoClip(make_frame, duration=total_duration).set_position(move_plot)

    background = ImageClip(np.full((VIDEO_HEIGHT, VIDEO_WIDTH, 3), 0), duration=total_duration)
    video = CompositeVideoClip([background, txt_clip1, txt_clip2.set_start(audio1.duration), plot_clip], size=VIDEO_SIZE).set_duration(total_duration)
    audio = CompositeAudioClip([audio1, audio2.set_start(audio1.duration)])

    return video, audio, total_duration

def generate_video(data):
    global X
    global Y
    X, Y = data

    v1, a1, d1 = intro_video('Good morning David,\n\nhere are your Daily Insights')
    v2, a2, d2 = plot_video('Yesterday\'s daily revenue\nfor store S0017fell below \n5 percent of the\n14 day average',
                            'Check in with sotre manager\n to determine cause.')

    video = CompositeVideoClip([v1, v2.set_start(d1)], size=VIDEO_SIZE).set_duration(d1 + d2)
    audio = CompositeAudioClip([a1, a2.set_start(d1)])

    video.audio = audio
    video.write_videofile("story.mp4",fps=30)
    #video.ipython_display(fps=10, loop=True, autoplay=True)

if __name__ == '__main__':
    x = np.array([
                    Timestamp('2018-09-04 00:00:00'), Timestamp('2018-09-05 00:00:00'),
                    Timestamp('2018-09-06 00:00:00'), Timestamp('2018-09-07 00:00:00'),
                    Timestamp('2018-09-08 00:00:00'), Timestamp('2018-09-09 00:00:00'),
                    Timestamp('2018-09-10 00:00:00'), Timestamp('2018-09-11 00:00:00'),
                    Timestamp('2018-09-12 00:00:00'), Timestamp('2018-09-13 00:00:00'),
                    Timestamp('2018-09-14 00:00:00'), Timestamp('2018-09-15 00:00:00'),
                    Timestamp('2018-09-16 00:00:00'), Timestamp('2018-09-17 00:00:00')
       ],dtype=object)
    y = np.array([134.74, 207.39, 275.56, 106.89, 176.14, 162.75, 46.32, 452.76, 287.28, 87.05, 174.73, 65.6, 119.83, 0.0], dtype=object)
    generate_video((x,y))