from edit import *
from scout import *
from download import *
from upload import *
from scout import *
import os, json, requests, base64

from cryptography.fernet import Fernet

TEST_AUTH_TOKEN = "isg4pa7sc1anbbctrn6pfs7ikl1wf8"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")





# popular_clips = fetch_popular_clips(
#     top_games(CLIENT_ID, TEST_AUTH_TOKEN, count=5), 
#     CLIENT_ID, 
#     TEST_AUTH_TOKEN,
#     count=5,
#     lastDays=7
#     )

# print(popular_clips)

# download_clips(popular_clips, CLIENT_ID, TEST_AUTH_TOKEN)

folder_path = f"{os.getcwd()}\\saved_clips\\"
for file in os.listdir(folder_path):
    mark_clip(file)

folder_path = f"{os.getcwd()}\\edited_clips\\"
edited_clips = []
for file in os.listdir(folder_path):
    edited_clips.append(file)
    
transition = "transition_tvstatic.mp4"
montage(edited_clips, transition, max_duration = 600)