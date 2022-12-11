import moviepy.editor as mpy
from moviepy.editor import *
from datetime import date
import base64
from dotenv import load_dotenv

load_dotenv()

def mark_clip(file_name):
    file_name = file_name.split(".mp4")[0]

    clip_info = file_name.split("_-")
    clip_streamer = clip_info[0]
    clip_title = clip_info[1]
    clip_title = base64.b64decode(clip_title).decode('ascii')
    clip_game = int(clip_info[2])
    clip_duration = float(clip_info[3])
    clip_author = clip_info[4]

    clip = mpy.VideoFileClip(f"./saved_clips/{file_name}.mp4").resize(height=1080, width=1920)  # .subclip(0,1)

    twitch_logo = mpy.ImageClip("./resources/twitch_logoW.png").set_duration(clip_duration).set_position((5, "top")).resize(height = 50, width = 50).margin(top=5)
    watermark = mpy.ImageClip("./resources/clipit_watermark.png").set_duration(clip_duration).set_position(("right", "top")).resize(height = 50, width = 50).margin(bottom=5)
    streamer_name = mpy.TextClip(clip_streamer, fontsize = 50, color = "white", font="Arial-Bold").set_opacity(1).set_position((60, "top")).set_duration(clip_duration)
    sn_width, sn_height = streamer_name.size
    text_bg = mpy.ColorClip(size=(sn_width+20+50, sn_height+5), color=(0,0,0)).set_position((0, "top")).set_duration(clip_duration)


    final  = mpy.CompositeVideoClip([clip, text_bg, twitch_logo, streamer_name, watermark], size = (1920,1080))

    # final.ipython_display()
    # final_clip = concatenate(clip_list, method = "compose")

    final.write_videofile(f"./edited_clips/{file_name}.mp4", fps = 30)

def montage(clips=[], transition=None, max_duration=9999, title=""):
    duration = 0
    montage_clips = []
    if transition != None:
        transition = mpy.VideoFileClip(f"./transitions/{transition}").subclip(0,.5).resize(height=1080, width=1920).volumex(.4)
    
    clip_count = 0
    while duration <= max_duration:
        for clip in clips:
            clip_count+=1
            clip = clip.split(".mp4")[0]

            clip_info = clip.split("_-")
            clip_streamer = clip_info[0]
            clip_title = clip_info[1]
            clip_title = base64.b64decode(clip_title).decode('ascii')
            clip_game = int(clip_info[2])
            clip_duration = int(round(float(clip_info[3])))
            clip_author = clip_info[4]

            temp_clip = mpy.VideoFileClip(f"./edited_clips/{clip}.mp4")

            montage_clips.append(temp_clip)
            if transition != None:
                if not (len(clips) == clip_count):
                    montage_clips.append(transition)

            duration += clip_duration
        break

    if title == "":
        today = str(date.today())
        title = f"Popular Clips {today}"
    final_montage  = mpy.concatenate_videoclips(montage_clips, method="compose")
    final_montage.write_videofile(f"./montaged_clips/{title}.mp4", fps = 30)




# montage_ = [
#     "xQc_-xqc realises how crazy breast reduction can be_-509658_-17.1_-martiiniblu2.mp4",
#     "xQc_-xqc realises how crazy breast reduction can be_-509658_-17.1_-martiiniblu.mp4"
# ]
# transition = "transition_tvstatic.mp4"
# montage(montage_, transition)


# file_name = "xQc_-xqc realises how crazy breast reduction can be_-509658_-17.1_-martiiniblu.mp4"
# mark_clip(file_name)
