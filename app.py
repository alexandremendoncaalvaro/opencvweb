# import the necessary packages
from flask import Response
from flask import Flask
from flask import render_template
from flask import request
import cv2


# initialize a flask object
app = Flask(__name__, template_folder='./templates')

currentFrame = 0
camera = cv2.VideoCapture("video/becks.mp4")

class SelectionBox:
    x = 0
    y = 0
    h = 0
    w = 0

selectionBox = SelectionBox()

def drawFrame(frame):
    left = selectionBox.x
    top = selectionBox.y
    right = selectionBox.x + selectionBox.w
    bottom = selectionBox.y + selectionBox.h

    color = (255, 255, 255)

    cv2.rectangle(frame, (left, top),(right, bottom), color, 2)
    return frame

def gen_frames():
    global currentFrame
    runVideo = True
    while runVideo:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            if currentFrame == 10:
                runVideo = False
            if(selectionBox.h > 0):
                frame = drawFrame(frame)
                runVideo = True
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            currentFrame += 1
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/mark")
def add():
    selectionBox.x = int(request.args.get('x'))
    selectionBox.y = int(request.args.get('y'))
    selectionBox.h = int(request.args.get('h'))
    selectionBox.w = int(request.args.get('w'))
    return {"msg": "Created Successfully"}, 201