import os
from flask import Flask, request
import whisper
from TTS.api import TTS
import torch

# Load the model
model = whisper.load_model('small')
app = Flask(__name__)
volume_path = '/whisper-volume'

device = "cuda" if torch.cuda.is_available() else "cpu"

@app.route('/tts', methods=['POST'])
def tts():
    print(request.json)
    #get command from body
    text = request.json['text']
    # Load the model
    model_tts = TTS("tts_models/en/ek1/tacotron2").to(device)
    file_name = text.split(" ")[0] + ".wav"
    file_path = os.path.join(volume_path, file_name)
    #TODO: Add speaker_wav to the request
    model_tts.tts_to_file(text=text, file_path=file_path)
    return {'file_path': file_path}


@app.route('/ttsbg', methods=['POST'])
def ttsbg():
    #get command from body
    text = request.json['text']
    # Load the model
    model_tts = TTS("tts_models/bg/cv/vits").to(device)
    file_name = text.split(" ")[0] + ".wav"
    file_path = os.path.join(volume_path, file_name)
    #TODO: Add speaker_wav to the request
    model_tts.tts_to_file(text=text, file_path=file_path)
    return {'file_path': file_path}

@app.route('/stt', methods=['GET'])
def handler():
    print(request.args)
    # Get the filename from the query parameters
    filename = request.json['filename']
    if not filename:
        # If filename is not provided, return an error.
        return {'error': 'No filename provided in the request.'}, 400


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
