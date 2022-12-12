import json

streamers = json.load(open("./montaged_clips/Popular Clips 2022-12-12 06-22-37.json", "r"))

for s in streamers["all_streamers"]:
    print(f"twitch.tv/{s}")