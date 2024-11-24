from io import BytesIO
from flask import Flask
from flask_socketio import SocketIO, emit
from segmentParser import synthese
from pydub import AudioSegment


app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")

def response(bytes):
    #raw_data = AudioSegment.from_mp3(BytesIO(bytes)).raw_data
    emit("audio_chunk", bytes)

# WebSocket endpoint for TTS live streaming
@sio.on("start_tts")
def start_tts(data):
   print("data->",data)
   text = data.get('text', '')
   synthese(text, response)



@sio.on("connect")
def on_connect():
    print("Client connected")


@sio.on("disconnect")
def on_disconnect():
    print("Client disconnected")



# Start the Flask-SocketIO app
if __name__ == "__main__":
    sio.run(app, host="0.0.0.0", port=5000, debug=True)
    