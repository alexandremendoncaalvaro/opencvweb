# import the necessary packages
from flask import Flask
from flask import Response
from flask import render_template
from flask import request
from flask import jsonify
import cv2

# initialize a flask object
app = Flask(__name__, template_folder='./templates')

currentFrame = 0
video = cv2.VideoCapture("video/becks.mp4")


class VideoSize:
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


videoSize = VideoSize()


class SelectionBox:
    x = 0
    y = 0
    h = 0
    w = 0


selectionBox = SelectionBox()


def draw_frame(frame):
    left = selectionBox.x
    top = selectionBox.y
    right = selectionBox.x + selectionBox.w
    bottom = selectionBox.y + selectionBox.h

    color = (255, 255, 255)

    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    return frame


def gen_frames():
    global currentFrame
    runVideo = True
    while runVideo and video.isOpened():
        success, frame = video.read()  # read the camera frame
        if not success:
            break
        else:
            if currentFrame == 10:
                runVideo = False
            if(selectionBox.h > 0):
                frame = draw_frame(frame)
                runVideo = True
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            currentFrame += 1
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def start_base():
    return render_template('base.html', video_size=videoSize)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/mark")
def add_mark():
    selectionBox.x = int(request.args.get('x'))
    selectionBox.y = int(request.args.get('y'))
    selectionBox.h = int(request.args.get('h'))
    selectionBox.w = int(request.args.get('w'))
    return {"msg": "Created Successfully"}, 201
