from flask import Blueprint, request, jsonify
from util.files import CloudflareR2

objects_bp = Blueprint('objects', __name__)
r2_client = CloudflareR2()

@objects_bp.route('/list_objects', methods=['GET'])
def list_objects():
    try:
        objects = r2_client.list_objects()
        return jsonify({'objects': objects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@objects_bp.route('/delete_object', methods=['POST'])
def delete_object():
    if 'objectKey' not in request.json:
        return jsonify({'error': 'Object key not provided'}), 400

    object_key = request.json['objectKey']

    try:
        r2_client.delete_object(object_key)
        return jsonify({'message': f'Object {object_key} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
