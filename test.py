import edge_tts
import pyaudio
from io import BytesIO
from pydub import AudioSegment
import time

TEXT = ' 根据2023年1月联合国世界人口展望，very good中国的人口估计为 14.26 亿, Hello, 这是一个测试。This is a test'
VOICE = "zh-CN-YunjianNeural"
CHUNK_SIZE = 20 * 1024  # Assuming around 1024 bytes per chunk (adjust based on format)

def main() -> None:
  start_time = time.time()
  communicator = edge_tts.Communicate(TEXT, VOICE)

  pyaudio_instance = pyaudio.PyAudio()
  audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

  total_data = b''  # Store audio data instead of chunks

  for chunk in communicator.stream_sync():
    if chunk["type"] == "audio" and chunk["data"]:
      total_data += chunk["data"]
      if len(total_data) >= CHUNK_SIZE:
        print(f"Time elapsed: {time.time() - start_time:.2f} seconds")  # Print time
        play_audio(total_data[:CHUNK_SIZE], audio_stream)  # Play first CHUNK_SIZE bytes
        total_data = total_data[CHUNK_SIZE:]  # Remove played data

  # Play remaining audio
  play_audio(total_data, audio_stream)

  audio_stream.stop_stream()
  audio_stream.close()
  pyaudio_instance.terminate()

def play_audio(data: bytes, stream: pyaudio.Stream) -> None:
  stream.write(AudioSegment.from_mp3(BytesIO(data)).raw_data)

if __name__ == "__main__":
  main()