from flask import Flask, render_template , request , jsonify
from PIL import Image
import os , io , sys
import numpy as np 
import cv2 as cv
import base64
import foreimg
from pprint import pprint
import sys

def dier (msg):
    pprint(msg);
    sys.exit(1)

app = Flask(__name__)

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    """

    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def img_to_base64 (img):
    return "<img src='data:image/png;base64," + img + "' />"

def add(name, img):
    return "<h2>" + name + "</h2>" + img_to_base64(img)

@app.route('/test' , methods=['POST'])
def test():
    file = request.files['image'].read() ## byte file
    #if not file:
    #    return "file image was not defined."
    npimg = np.fromstring(file, np.uint8)
    img = cv.imdecode(npimg,cv.IMREAD_COLOR)
    img = Image.fromarray(img.astype("uint8"))

    img = foreimg.jpeg_ghost(None, 80, img)

    html = add("JPEG-Ghosts:", img)

    return html

@app.route('/home')
def home():
    return render_template('./index.jinja2')



@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(debug = True)
