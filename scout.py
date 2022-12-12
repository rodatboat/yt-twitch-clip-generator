import json, requests, os, datetime
from dotenv import load_dotenv
from download import *

load_dotenv()
r = requests.session()

def top_games(client_id, token, count = 64):
    games_url = f"https://api.twitch.tv/helix/games/top"
    req_headers = {
        "Authorization":f"Bearer {token}",
        "Client-Id":client_id
    }
    req_params = {
        "first":count
    }
    games_info = r.get(games_url, headers=req_headers, params=req_params)
    games_info = json.loads(games_info.text)["data"]
    
    top_games_ids = []
    for game in games_info:
        top_games_ids.append(game["id"])
    return top_games_ids


def fetch_popular_clips(top_games_ids, client_id, token, lastDays = 0, language = "en", count=20):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=lastDays)
    end_date = datetime.datetime.utcnow()

    start_date = start_date.isoformat("T") + "Z"
    end_date = end_date.isoformat("T") + "Z"

    clip_ids = []
    for games in top_games_ids:
        top_clips_url = f"https://api.twitch.tv/helix/clips"
        req_headers = {
            "Authorization":f"Bearer {token}",
            "Client-Id":client_id
        }
        req_params = {
            "game_id":games,
            "started_at":start_date,
            "ended_at":end_date,
            "first":count
        }
        clips_info = r.get(top_clips_url, headers=req_headers, params=req_params)
        clips_info = json.loads(clips_info.text)["data"]

        for clip_id in clips_info:
            if(clip_id["language"] == language):
                clip_ids.append(clip_id["id"])

    return clip_ids

def fetch_popular_clips_by_streamer(broadcaster_id, client_id, token, lastDays = 0, language = "en", count=20):
    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=lastDays)
    end_date = datetime.datetime.utcnow()

    start_date = start_date.isoformat("T") + "Z"
    end_date = end_date.isoformat("T") + "Z"

    clip_ids = []
    for broadcaster in broadcaster_id:
        top_clips_url = f"https://api.twitch.tv/helix/clips"
        req_headers = {
            "Authorization":f"Bearer {token}",
            "Client-Id":client_id
        }
        req_params = {
            "broadcaster_id":broadcaster,
            "started_at":start_date,
            "ended_at":end_date,
            "first":count
        }
        clips_info = r.get(top_clips_url, headers=req_headers, params=req_params)
        clips_info = json.loads(clips_info.text)["data"]

        for clip_id in clips_info:
            if(clip_id["language"] == language):
                clip_ids.append(clip_id["id"])

    return clip_ids