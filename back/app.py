from flask import Flask
from flask_cors import CORS
import ffmpeg
from util.files import CloudflareR2
import string
import random

app = Flask(__name__)
# CORS(app)

# Import and register blueprints
from api.presigned_url import presigned_url_bp
from api.objects import objects_bp
from api.transcript import transcript_bp
from api.img_segmentation import imgsegbp

app.register_blueprint(presigned_url_bp, url_prefix='/api')
app.register_blueprint(objects_bp, url_prefix='/api')
app.register_blueprint(transcript_bp, url_prefix='/api')
app.register_blueprint(imgsegbp, url_prefix='/api')

# def extract_audio(video_url):
#    r2 = CloudflareR2()
#    process = (
#         ffmpeg
#         .input(video_url)
#         .output('pipe:', format='mp3')  # Specify output format (e.g., mp3)
#         .run_async(pipe_stdout=True, pipe_stderr=True)
#     )
#    audio_bytes = process.stdout.read()
   
#    process.wait()
   
#    file_name = ''.join(random.choices(string.ascii_letters,
#                              k=10)) 
#    object_key = file_name + ".mp3"
#    r2.upload_object(object_key, audio_bytes)

#    return "https://hackmit2024.lilbillbiscuit.com/" + object_key



    


# print(f'Audio extracted and saved as {output_audio_file}')

if __name__ == '__main__':
    app.run(debug=True)
