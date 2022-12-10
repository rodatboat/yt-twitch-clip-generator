import json, requests, os
from dotenv import load_dotenv

load_dotenv()
r = requests.session()

test_cids = ["AnimatedInterestingSproutPrimeMe-UYNXXdaGm_5IyobZ", "DeliciousRealWatercressMoreCowbell-4d_s4wMgqDY0tubW"]
# test_cid = "NastyNaiveOysterOSsloth-pvt3cTngOPKyXWuf"
TEST_AUTH_TOKEN = "isg4pa7sc1anbbctrn6pfs7ikl1wf8"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def fetch_auth_token(client_id, client_secret):
    auth_url = "https://id.twitch.tv/oauth2/token"
    req_params = {
        "client_id":client_id,
        "client_secret":client_secret,
        "grant_type":"client_credentials"
    }

    auth_token = r.post(auth_url, params=req_params)
    auth_token = json.loads(auth_token.text)
    try:
        auth_token = auth_token["access_token"]
        return auth_token
    except:
        auth_token = auth_token["status"]
        return auth_token

def fetch_game_by_id(game_id, client_id, token):
    game_url = "https://api.twitch.tv/helix/games"
    req_headers = {
        "Authorization":f"Bearer {token}",
        "Client-Id":client_id
    }
    req_params = {
        "id":game_id
    }
    game_info = r.get(game_url, headers=req_headers, params=req_params)
    game_info = json.loads(game_info.text)["data"][0]["name"]

    return game_info


def download_clip(clip_id, client_id, token):
    clip_url = f"https://api.twitch.tv/helix/clips"
    req_headers = {
        "Authorization":f"Bearer {token}",
        "Client-Id":client_id
    }
    req_params = {
        "id":clip_id
    }
    clip_info = r.get(clip_url, headers=req_headers, params=req_params)
    clip_info = json.loads(clip_info.text)["data"][0]

    broadcaster_name = clip_info["broadcaster_name"]
    creator_name = clip_info["creator_name"]
    title = clip_info["title"]
    duration = str(clip_info["duration"])
    game = str(clip_info["game_id"])
    

    clip_dl_url = clip_info["thumbnail_url"].split("-preview-")[0]
    clip_dl_url = clip_dl_url + ".mp4"

    clip_bytes = r.get(clip_dl_url, headers=req_headers)
    file_name = broadcaster_name + "_-" + title + "_-" + game + "_-" + duration + "_-" + creator_name + ".mp4"

    with open(f"./saved_clips/{file_name}", "wb") as saved_clip:
        saved_clip.write(clip_bytes.content)

def download_clips(clip_ids, client_id, token):
    clip_url = f"https://api.twitch.tv/helix/clips"
    req_headers = {
        "Authorization":f"Bearer {token}",
        "Client-Id":client_id
    }
    for index, id in enumerate(clip_ids):
        if index == 0:
            clip_url += "?id="
            clip_url += id
        else:
            clip_url += "&id="
            clip_url += id

    clip_info = r.get(clip_url, headers=req_headers)
    clip_info_all = json.loads(clip_info.text)["data"]

    for clip_info in clip_info_all:
        broadcaster_name = clip_info["broadcaster_name"]
        creator_name = clip_info["creator_name"]
        title = clip_info["title"]
        duration = str(clip_info["duration"])
        game = str(clip_info["game_id"])
        

        clip_dl_url = clip_info["thumbnail_url"].split("-preview-")[0]
        clip_dl_url = clip_dl_url + ".mp4"

        clip_bytes = r.get(clip_dl_url, headers=req_headers)
        file_name = broadcaster_name + "_-" + title + "_-" + game + "_-" + duration + "_-" + creator_name + ".mp4"

        with open(f"./saved_clips/{file_name}", "wb") as saved_clip:
            saved_clip.write(clip_bytes.content)

# download_clip(test_cid, CLIENT_ID, TEST_AUTH_TOKEN)

download_clips(test_cids, CLIENT_ID, TEST_AUTH_TOKEN)