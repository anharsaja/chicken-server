import cv2
import base64
from flask import Flask
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Function to capture video and send frames to the client
def capture_video():
    cap = cv2.VideoCapture(0)  # 0 is for the default camera, change if using an external camera

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            # Convert to base64
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            # Send the frame to the client
            socketio.emit('video_frame', frame_base64)
        socketio.sleep(0.05)  # to control the frame rate
    cap.release()

@app.route('/')
def index():
    return "Socket.IO Video Server is running."

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(capture_video)  # Start capturing video when client connects

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
