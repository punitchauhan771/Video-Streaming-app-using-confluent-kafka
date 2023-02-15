import cv2
import numpy as np
from flask import Flask, Response
from confluent_kafka import Consumer, KafkaError
import threading
from producer import read_ccloud_config

app = Flask(__name__)

@app.route('/')
def index():
    return Response('hello')

def video_consumer():
    # Set up the consumer configuration
    props = read_ccloud_config("config.ini")
    props["group.id"] = "python-group-1"
    props["auto.offset.reset"] = "earliest"

    consumer = Consumer(props)
    consumer.subscribe(["distributed_video1"])
    # Continuously retrieve video data from the topic
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Reached end of partition event for {} [{}] at offset {}'.format(msg.topic(), msg.partition(), msg.offset()))
            else:
                print('Error while polling for messages: {}'.format(msg.error()))
            continue

        # Decode the video frame
        jpeg_frame = np.frombuffer(msg.value(), np.uint8)
        frame = cv2.imdecode(jpeg_frame, cv2.IMREAD_COLOR)

        # Send the frame to the Flask application
        send_frame(frame)

def send_frame(frame):
    global frame_data
    ret, jpeg = cv2.imencode('.jpg', frame)
    frame_data = jpeg.tobytes()

@app.route('/video')
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        if not 'frame_data' in globals():
            time.sleep(0.1)
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

if __name__ == '__main__':
    t = threading.Thread(target=video_consumer)
    t.start()
    app.run()
