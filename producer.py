import cv2
from confluent_kafka import Producer

#config file reader (default code provided in coonfluent client script)
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

def send_video_data(camera_id):
    # Set up the video capture
    cap = cv2.VideoCapture(camera_id)
    # Callback function to handle delivery reports
    def delivery_report(err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    # Create a producer instance
    producer = Producer(read_ccloud_config("config.ini"))

    # Start capturing frames
    while True:
        # Capture a frame
        ret, frame = cap.read()

        # Break the loop if the video capture is finished
        if not ret:
            break

        # Encode the frame to JPEG format
        _, jpeg_frame = cv2.imencode('.jpg', frame)

        # Produce a message to the topic
        producer.produce('distributed_video1', key=None, value=jpeg_frame.tobytes(), callback=delivery_report)

    # Wait for any outstanding messages to be delivered and delivery report callbacks to be received
    producer.flush()

    # Release the video capture
    cap.release()

    # Close the producer
    producer.close()


send_video_data(0)
