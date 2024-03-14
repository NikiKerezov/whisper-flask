import os
from flask import Flask, request
import whisper
import shutil

# Load the model
model = whisper.load_model('small')
app = Flask(__name__)


@app.route('/', methods=['GET'])
def handler():
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    if not filename:
        # If filename is not provided, return an error.
        return {'error': 'No filename provided in the request.'}, 400

    # Define the path to the Docker volume
    volume_path = 'whisper-volume'  # Replace with the actual path

    # Construct the full path to the file in the Docker volume
    file_path = os.path.join(volume_path, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return {'error': f'File {filename} not found in the Docker volume.'}, 404

    # Transcribe the audio file
    result = model.transcribe(file_path)

    return {'transcript': result['text']}


if __name__ == '__main__':
    app.run()
