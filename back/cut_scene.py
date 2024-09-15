from scenedetect import detect, ContentDetector, split_video_ffmpeg
import ffmpeg
import subprocess
import os
from PIL import Image
from io import BytesIO
import imagehash as ih
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
import json
import io
from datetime import datetime
import cv2
import sys

path = "../videos/documentary_short.mp4"
def split_video(video_path):
    scene_list = detect(video_path, ContentDetector())
    scene_times = []

    timestamp_format = "%H:%M:%S"
    for i in range(len(scene_list)):
        start_time = scene_list[i]
        start_time = datetime.strptime(start_time[0].get_timecode().split(".")[0], timestamp_format).time()
        # end_time = scene_list[i + 1]
        scene_times.append(start_time)

    return scene_times

def get_scene_frames(video_path, scene_times):
    # Convert datetime.time to total seconds
    frames = {}
    for x in scene_times:
        timestamp_seconds = x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Get the video's FPS (frames per second)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        # Calculate the frame number
        frame_number = int(fps * timestamp_seconds)
        
        # Set the video position to the specific frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read the frame
        ret, frame = cap.read()
        
        if not ret:
            raise ValueError("Frame could not be retrieved.")
        
        # Release the video capture object
        cap.release()
        
        # Convert the frame (OpenCV image) to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frames[timestamp_seconds] = pil_image
    return frames

def get_distinct_frames(frames):
    images = {}
    past = None
    for x in frames.keys():
        if past != None:
            if not compare_frames(past, frames[x]):
                images[x] = frames[x]
                past = frames[x]
        else:
            images[x] = frames[x]
            past = frames[x]
    return images
                
                
def compare_frames(img1, img2):
    similarity = 70
    threshold = 1 - similarity/100
    diff_limit = int(threshold*(20**2))
    hash1 = ih.average_hash(img1, 20).hash
    hash2 = ih.average_hash(img2, 20).hash
    if np.count_nonzero(hash1 != hash2) <= diff_limit:
        return True
    return False



if __name__ == "__main__":
    if(len(sys.argv) > 1 ):
        get_distinct_frames(get_scene_frames(sys.argv[1], split_video(sys.argv[1])))
    else:
        get_distinct_frames(get_scene_frames(path, split_video(path)))
