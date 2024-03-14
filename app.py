import os

from flask import Flask, request
import whisper
from tempfile import NamedTemporaryFile

# Load the model
model = whisper.load_model('small')
app = Flask(__name__)


@app.route('/', methods=['POST'])
def handler():
    if not request.files:
        # If the user didn't submit any files, return an error.
        return {'error': 'No files were submitted.'}, 400

    results = []

    for filename, handle in request.files.items():
        temp = NamedTemporaryFile(dir=os.curdir, delete=False, suffix=".mp3")

        handle.save(temp)

        result = model.transcribe(temp.name)

        results.append({
            'filename': filename,
            'transcript': result['text'],
        })
        temp.close()
        os.remove(temp.name)
    return {'results': results}


if __name__ == '__main__':
    app.run()