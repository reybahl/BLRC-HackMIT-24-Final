import os
import json
from flask import Blueprint, jsonify, abort
from botocore.exceptions import ClientError
import requests
import json
import os
import datetime as datetime
from util.files import CloudflareR2

transcript_bp = Blueprint('transcript', __name__)
r2_client = CloudflareR2()

@transcript_bp.route('/transcript/get/<video_id>', methods=['GET'])
def get_transcript(video_id):
    """
    Retrieves the transcript for a given video ID.
    
    Args:
    video_id (str): The ID of the video to fetch the transcript for.
    
    Returns:
    dict: The transcript data if found.
    
    Raises:
    404: If the transcript file doesn't exist.
    500: If there's an error reading or decoding the file.
    """
    if "." in video_id: video_id = video_id.split('.')[0]# TODO errors if there are dots in the video_id
    
    # Construct the file path
    file_path = f"transcripts/{video_id}.json"

    try:
        print(file_path)
        data = r2_client.get_object(file_path)
        return data
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            abort(404, description=f"Transcript not found for video ID {video_id}")
        else:
            abort(500, description=f"An error occured for video ID {video_id}")
            raise
    except json.JSONDecodeError:
        abort(500, description=f"Error decoding transcript for video ID {video_id}")
    except IOError:
        abort(500, description=f"Error reading transcript file for video ID {video_id}")
    except Exception as e:
        print(e)
        abort(500, description=f"Error reading transcript file for video ID {video_id}")

def process_transcript(video_id):
    """
    Begins processing the transcript for a given video ID.
    This make take a long time to complete, so the function just returns "success" if the process starts.
    """
    pass