import json, requests, os, datetime
from dotenv import load_dotenv

load_dotenv()
r = requests.session()


def fetch_popular_clips(lastDays = 0):
    return 0

start_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)
end_date = datetime.datetime.utcnow()

start_date = start_date.isoformat("T") + "Z"
end_date = end_date.isoformat("T") + "Z"

url = "https://www.twitch.tv/directory"

cookies = {
    "auth-token":"oc73io9u5j95l2tymdn7p195b13wjv"
}
data = r.get(url, cookies=cookies)

print(data.text)