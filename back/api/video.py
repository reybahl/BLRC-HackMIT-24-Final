from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from util.files import CloudflareR2

video_upload = Blueprint('video_upload', __name__)

# Configuration
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

# Initialize CloudflareR2 client
access_key_id = '47111b0f99db6690ed0b7d340979de56'
secret_access_key = '77b487eb3acc7dbc4d8701ce9e62f4a7c44716d38116d061dc5a229395f239a0'
endpoint_url = 'https://752c3dd4c8e27b1f472a31fc8c6aad68.r2.cloudflarestorage.com'
bucket_name = 'hackmit2024'

r2_client = CloudflareR2(access_key_id, secret_access_key, endpoint_url)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_upload.route('/upload', methods=['POST', 'GET'])
def upload_video():
    # Check if a file is present in the request
    if 'video' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['video']
    
    # Check if a filename is present
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    # Validate file extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        try:
            # Read the file content
            file_content = file.read()
            
            # Upload to Cloudflare R2
            r2_client.upload_object(bucket_name, filename, file_content)
            
            return jsonify({'message': 'Video uploaded successfully', 'filename': filename}), 200
        except Exception as e:
            return jsonify({'error': f'An error occurred while uploading: {str(e)}'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400
