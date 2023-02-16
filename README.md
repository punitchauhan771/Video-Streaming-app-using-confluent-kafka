# Video Streaming App using Confluent Kafka and Python

This repository contains a video streaming application built using Confluent Kafka and Python. The application streams video frames from a webcam or a video file, and displays the frames as a live video stream on a Flask web application.

Prerequisites

To run the application, you'll need the following software installed on your machine:

Python 3.x
Confluent Kafka cluster (use web hosted kafka cluster given by confluent)
OpenCV
Flask
Getting Started

To get started, clone the repository to your local machine:

```
git clone https://github.com/punitchauhan771/video-streaming-app.git
```

Then, navigate to the cloned directory and install the required Python packages using pip:

```
cd video-streaming-app
pip install -r requirements.txt
```

Before running the application, you'll need to start the Kafka broker and create a topic to receive the video frames. 


The application will start streaming video frames from your webcam, and display them as a live video stream on a Flask web application. 
To stream video from a file, simply use this command
```
python consumer.py
```

The consumer.py will receive frame stored in kafka topic and will stream the video

```
python producer.py
```

The producer.py will use your web cam to capture the video and will convert into image frames which will then be uploaded to the kafka topic.

You can access the live video stream by navigating to http://localhost:5000/video in your web browser.

License

This project is licensed under the MIT License - see the LICENSE file for details.

