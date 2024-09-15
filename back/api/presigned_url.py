from flask import Blueprint, request, jsonify
from util.files import CloudflareR2
import random
import string

presigned_url_bp = Blueprint('presigned_url', __name__)
r2_client = CloudflareR2()

@presigned_url_bp.route('/video', methods=['POST'])
def get_presigned_url():
    if 'filename' not in request.json:
        return jsonify({'error': 'Filename not provided'}), 400
    
    extension = request.json['filename'].split('.')[-1]
      
    # generate random 8 character hex string as filename
    hex_chars = string.hexdigits.lower()[:16]
    filename = ''.join(random.choices(hex_chars, k=8)) + '.' + extension
    file_type = request.json.get('fileType', 'application/octet-stream')

    try:
        object_key = f"uploads/{filename}"
        presigned_url = r2_client.generate_presigned_url(
            object_key, 
            expiration=3600,
            http_method='put'
        )

        return jsonify({
            'presignedUrl': presigned_url, 
            'filename': filename,
            'objectKey': object_key
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
