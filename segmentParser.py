import edge_tts
import time


CHUNK_SIZE = 50 * 1024  # Assuming around 1024 bytes per chunk (adjust based on format)
voice = "zh-CN-XiaoxiaoNeural"

def synthese(text, callback) -> None:
    start_time = time.time()
    communicator = edge_tts.Communicate(text, voice)

    total_data = b''  # Store audio data instead of chunks

    for chunk in communicator.stream_sync():
        if chunk["type"] == "audio" and chunk["data"]:
            total_data += chunk["data"]
        if len(total_data) >= CHUNK_SIZE:
            print(f"Time elapsed: {time.time() - start_time:.2f} seconds")  # Print time
            callback(total_data[:CHUNK_SIZE])  # Play first CHUNK_SIZE bytes
            total_data = total_data[CHUNK_SIZE:]  # Remove played data

    if len(total_data) > 0:
        callback(total_data)


