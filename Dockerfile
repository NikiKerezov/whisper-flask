FROM python:3.9-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install git -y
# If are experiencing errors ImportError: cannot import name 'soft_unicode' from 'markupsafe'  please uncomment below
# RUN pip3 install markupsafe==2.0.1
RUN pip install --upgrade -r requirements.txt
RUN pip install openai-whisper
RUN apt-get install -y ffmpeg
RUN pip install TTS

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
