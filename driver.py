from edit import *
from scout import *
from download import *
from upload import *
from scout import *
import os, threading, shutil


TEST_AUTH_TOKEN = "isg4pa7sc1anbbctrn6pfs7ikl1wf8"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

def gen_clips_list(game_count = 5, clip_per_game = 5, last_days = 7, byGame = False, game_id = -1):
    if byGame and game_id != -1:
        popular_clips = fetch_popular_clips(
        game_id, 
        CLIENT_ID, 
        TEST_AUTH_TOKEN,
        count=clip_per_game,
        lastDays=last_days
        )
    else:
        popular_clips = fetch_popular_clips(
        top_games(CLIENT_ID, TEST_AUTH_TOKEN, count=game_count), 
        CLIENT_ID, 
        TEST_AUTH_TOKEN,
        count=clip_per_game,
        lastDays=last_days
        )

    return popular_clips

def dl_clips(popular_clips):
    download_clips(popular_clips, CLIENT_ID, TEST_AUTH_TOKEN)

def filter_clips(top = 20, maxDuration = 1099):
    folder_path = f"{os.getcwd()}\\saved_clips\\"
    most_viewed_clips = []
    for file in os.listdir(folder_path):
        file_name = file.split(".mp4")[0]
        clip_info = file_name.split("_-")
        clip_views = round(int(clip_info[4]))
        most_viewed_clips.append((file, clip_views))

    def takeSecond(elem):
        return elem[1]

    most_viewed_clips.sort(key=takeSecond)
    most_viewed_clips = reversed(most_viewed_clips)

    clips_kept = []

    total_duration = 0
    while total_duration <= maxDuration:
        for (file, views) in most_viewed_clips:
            if total_duration > maxDuration:
                break
            file_name = file.split(".mp4")[0]
            clip_info = file_name.split("_-")
            clip_duration = float(clip_info[3])
            
            clips_kept.append(file)
            total_duration+=clip_duration
        break
        
    filtered_path = f"{os.getcwd()}\\filtered_clips\\"
    for file in os.listdir(folder_path):
        if file not in clips_kept:
            shutil.move(folder_path+file, filtered_path+file)
        else:
            pass
    print(f"Total Duration: {total_duration}")
        

def mark_all_clips(max_threads = 1):
    folder_path = f"{os.getcwd()}\\saved_clips\\"
    edited_folder_path = f"{os.getcwd()}\\edited_clips\\"

    t_arr = []
    for file in os.listdir(folder_path):
        found = False
        for check_exists_file in os.listdir(edited_folder_path):
            if file == check_exists_file:
                found = True
        if not found:
            if len(t_arr) < max_threads:
                t1 = threading.Thread(target=mark_clip, args=(file,))
                t_arr.append(t1)
                t1.start()
            else:
                t_arr[0].join()
                t_arr.pop(0)

                t1 = threading.Thread(target=mark_clip, args=(file,))
                t_arr.append(t1)
                t1.start()
    for t in t_arr:
        try:
            t.join()
            t_arr.pop(0)
        except:
            pass

def create_montage(maxDuration = 1099):
    folder_path = f"{os.getcwd()}\\edited_clips\\"
    edited_clips = []
    for file in os.listdir(folder_path):
        edited_clips.append(file)
        
    transition = "transition_tvstatic.mp4"
    montage(edited_clips, transition, max_duration = maxDuration)


# 600 daily, 1000 weekly
max_duration = 600
game_id = [515025]

# game_count = 20, cpg = 5, ld = 7 weekly
# gc = 1, cpg = 100, ld = 1 daily
# allClips = gen_clips_list(game_count=1, clip_per_game=100, last_days=1, byGame=True, game_id=game_id)

# # allClips = gen_clips_list(game_count=20, clip_per_game=5, last_days=1.5)
# dl_clips(allClips)
# filter_clips(maxDuration=max_duration)
# mark_all_clips()
# create_montage()

# 
fetch_title_streamers()
title, desc = fetch_titledesc(weekly=False, monthly=False, daily=True, isGame=True, game="Overwatch 2")
# title, desc = fetch_titledesc(weekly=False, monthly=False, daily=True)


print(title, desc)