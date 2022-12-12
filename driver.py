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

def gen_clips_list(game_count = 5, clip_per_game = 5, last_days = 7):
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
    best_clips = []
    for file in os.listdir(folder_path):
        file_name = file.split(".mp4")[0]
        clip_info = file_name.split("_-")
        clip_views = round(int(clip_info[4]))
        best_clips.append((file, clip_views))
        # clip_duration = int(round(float(clip_info[3])))
    ordered_clips_temp = []
    for (curr_file, curr_file_views) in best_clips:
        if len(ordered_clips_temp) == 0:
            ordered_clips_temp.append((curr_file, curr_file_views))
        else:
            inserted = False
            for (ind, x) in enumerate(ordered_clips_temp):
                file, file_views = x
                if curr_file_views >= file_views:
                    ordered_clips_temp.insert(ind, (curr_file, curr_file_views))
                    inserted = True
                    break
            if not inserted:
                ordered_clips_temp.append((curr_file, curr_file_views))

    total_duration = 0
    for (ind, x) in enumerate(ordered_clips_temp):
        file, views = x
        if total_duration <= maxDuration:
            file_name = file.split(".mp4")[0]
            clip_info = file_name.split("_-")
            clip_duration = float(clip_info[3])
            total_duration += clip_duration
        else:
            ordered_clips_temp.pop(ind)

    print(f"Total Duration: {total_duration}")
    ordered_clips = []
    for (file, views) in ordered_clips_temp:
        ordered_clips.append(file)
        
    filtered_path = f"{os.getcwd()}\\filtered_clips\\"
    for file in os.listdir(folder_path):
        if file not in ordered_clips:
            shutil.move(folder_path+file, filtered_path+file)
        else:
            pass

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



max_duration = 600

allClips = gen_clips_list(game_count=20, clip_per_game=5, last_days=7)
dl_clips(allClips)
filter_clips(maxDuration=max_duration)
mark_all_clips()
create_montage()