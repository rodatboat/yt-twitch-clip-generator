from edit import *
from scout import *
from download import *
from upload import *
from scout import *
import os, threading


TEST_AUTH_TOKEN = "isg4pa7sc1anbbctrn6pfs7ikl1wf8"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

def get_pop_clips(game_count = 5, clip_per_game = 5, last_days = 7):
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

def mark_all_clips(max_threads = 1):
    folder_path = f"{os.getcwd()}\\saved_clips\\"

    t_arr = []
    for file in os.listdir(folder_path):
        if len(t_arr) < max_threads:
            t1 = threading.Thread(target=mark_clip, args=(file,))
            t_arr.append(t1)
            t1.start()
        else:
            t_arr[0].join()
            t_arr.pop(0)
    for t in t_arr:
        t.join()
        
mark_all_clips()

def create_montage():
    folder_path = f"{os.getcwd()}\\edited_clips\\"
    edited_clips = []
    for file in os.listdir(folder_path):
        edited_clips.append(file)
        
    transition = "transition_tvstatic.mp4"
    montage(edited_clips, transition, max_duration = 1000)

create_montage()