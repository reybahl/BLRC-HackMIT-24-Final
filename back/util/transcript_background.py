import requests
import json
# import time
import os
import datetime as datetime

def seconds_to_time(seconds):
    """Convert seconds to a datetime.time object."""
    hours, remainder = divmod(float(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return datetime.time(int(hours), int(minutes), int(seconds))

# Model ID for production deployment
model_id = "nwxgg66q"
key = ""
video_link = "https://hackmit2024.lilbillbiscuit.com/output_short.aac"

def get_transcript(model_id, key, video_link):
    with open("../key/baseten.txt", "r") as file:
        key = file.read().strip()

    resp = requests.post(
        f"https://model-{model_id}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {key}"},
        json={'url': video_link},
    )

    # print(resp.json())
    json_str = resp.content.decode("utf-8")
    transcript = json.loads(json_str)
    captions = []
    curr = ""
    # timestamp_format = "%H:%M:%S"
    for segment in transcript["segments"]:
        if segment["text"] != curr:
            captions.append((segment["start"], segment["end"], segment["text"]))
            # captions[seconds_to_time(segment["end"])] = segment["text"]
        curr = segment["text"]
    return captions

# print(get_transcript(model_id, key))