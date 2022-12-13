import json, requests, os

def fetch_title_streamers():
    folder_path = f"{os.getcwd()}\\edited_clips\\"
    top_streamers = {
        "top_streamers":[],
        "all_streamers":[]
    }

    all_streamers = []
    for clip in os.listdir(folder_path):
        clip_info = clip.split(".mp4")[0]
        clip_info = clip_info.split("_-")
        streamer_name = clip_info[0]
        clip_views = int(clip_info[4])

        if streamer_name not in top_streamers["all_streamers"]:
            top_streamers["all_streamers"].append(streamer_name)
            all_streamers.append((streamer_name, clip_views))
        else:
            for s in all_streamers:
                if s[0] == streamer_name:
                    original_s = s
                    s = list(s)
                    s[1] += clip_views
                    s = tuple(s)
                    all_streamers[all_streamers.index(original_s)] = s

    def takeSecond(elem):
        return elem[1]

    all_streamers.sort(key=takeSecond)
    all_streamers = reversed(all_streamers)

    top_counter = 0
    for s in all_streamers:
        if top_counter < 3:
            top_streamers["top_streamers"].append(s[0])
        else:
            break
        top_counter += 1

    title = "description"
    json_object = json.dumps(top_streamers, indent=4)
    with open(f"./montaged_clips/{title}.json", "w") as outfile:
        outfile.write(json_object)

def get_title_index():
    title_index = json.load(open("./montaged_clips/tracker.json", "r"))
    return title_index

def fetch_titledesc(weekly=False, monthly=False, daily=False, isGame=False, game=""):
    fetch_title_streamers()
    streamers = json.load(open("./montaged_clips/description.json", "r"))

    occurence = ""
    if weekly:
        occurence += "Week"
    elif monthly:
        occurence += "Month"
    elif daily:
        occurence += "Day"

    title = ""
    if isGame:
        title+= f"MOST POPULAR {game} Twitch Clips of The " + occurence
    else:
        # title+="Twitch"
        title+= "TWITCH FAILS AND HIGHLIGHTS of The " + occurence + "! w/ CHAT"

    # title += " ("
    # for s in streamers["top_streamers"]:
    #     title += f"#{s},"
    # title += "...) #highlights"

    description = ""
    description += title + "\n"
    description += "\n\n"
    description += "Submit Clips:\n"
    description += "https://forms.gle/XugXAAb8KuQusMfw6\n\n"
    description += "Credits:" + "\n"
    
    for s in streamers["all_streamers"]:
        description += f"twitch.tv/{s}\n"
    
    description += "___________________________________________\n"
    description += f"That's it for this video guys, if you liked {title}, hit that like button, if you want to see more videos like this, subscribe. Thank you so much for staying till the end of the video. Stay cool, and we will see you, in the next one.\n"
    description += "___________________________________________"

    with open("./montaged_clips/description.txt", "w") as file:
        file.write(title)
        file.write("\n")
        file.write(description)

    return (title, description)