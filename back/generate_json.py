from transcript import get_transcript
from cut_scene import get_distinct_frames, get_scene_frames, split_video
from util.files import CloudflareR2
import random
import string
from PIL import Image
import io
import json

model_id = "nwxgg66q"
key = ""
video_link = "https://hackmit2024.lilbillbiscuit.com/output_short.aac"
path = "../videos/documentary_short.mp4"
video_name = "documentary_short"
r2 = CloudflareR2()

transcript = get_transcript(model_id, key, video_link)
frames = get_distinct_frames(get_scene_frames(path,split_video(path) ))

data = {"elements" : []}
for x in transcript:
	# print("NEW ELEMENT")
	elem = {}
	elem["timestamp_start"] = x[0]
	elem["timestamp_end"] = x[1]
	elem["content"] = x[2]

	photo_links = []
	keys = list(frames.keys())
	for x in keys:
		# print("START ",elem["timestamp_start"], "END ", elem["timestamp_end"], "CURR ", x)
		if elem["timestamp_end"] >= x:

			# make file name
			file_name = ''.join(random.choices(string.ascii_letters,
                             k=10)) 
			object_key = file_name + ".JPEG"

			# convert image to byte string
			byte_io = io.BytesIO()
			# Save the image to the BytesIO object
			frames[x].save(byte_io, format='JPEG')  # or 'PNG', 'GIF', etc. depending on your image format
			# Get the byte string
			byte_string = byte_io.getvalue()

			# upload photo
			r2.upload_object(object_key, byte_string)

			photo_links.append("https://hackmit2024.lilbillbiscuit.com/" + object_key)
			
			del frames[x]
		elif x > elem["timestamp_end"]:
			break
	
	if photo_links != []:
		elem["photo_urls"] = photo_links

	data["elements"].append(elem)

with open(video_name + ".json", 'w') as file:
	json.dump(data, file, indent=4)  # Convert Python object to JSON and write to file
	r2.upload_object(video_name + ".json", json.dumps(data).encode('utf-8'))

