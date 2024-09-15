from util.files import CloudflareR2

r2_client = CloudflareR2()
r2_client.get_object("ksfjnsdf")
with open("documentary_short.json", "rb") as f:
    r2_client.upload_object("transcripts/32f3ad7b.mp4.json", f)