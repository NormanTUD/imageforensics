import tempfile
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
    return add_text(name, img_to_base64(img))

def add_pre(name, text):
    return add_text(name, "<pre>" + text + "</pre>")

def add_text(name, text):
    return "<h2>" + name + "</h2>" + text

@app.route('/analyze' , methods=['POST'])
def analyze():
    file = request.files.get('image', None)
    if file is None:
        return "File could not be POSTed from your Computer", 490

    file.seek(0)
    npimg = np.fromstring(file.read(), np.uint8)
    img = cv.imdecode(npimg,cv.IMREAD_COLOR)

    f1 = 500 / img.shape[1]
    f2 = 500 / img.shape[0]
    f = min(f1, f2)  # resizing factor
    dim = (int(img.shape[1] * f), int(img.shape[0] * f))
    img = cv.resize(img, dim)

    img = Image.fromarray(img.astype("uint8"))

    tmp_file = tempfile.NamedTemporaryFile()
    file.seek(0)
    tmp_file.write(file.read())
    tmp_file.flush()

    exif_str = foreimg.exif_check(str(tmp_file.name), 1)

    tamper_detection = foreimg.cfa_tamper_detection(str(tmp_file.name))
    ela = []
    for i in range (0, 100, 10):
        ela.append(foreimg.ela(str(tmp_file.name), i, 80))
    jpeg_ghosts_20 = foreimg.jpeg_ghost(None, 20, img)
    jpeg_ghosts_40 = foreimg.jpeg_ghost(None, 40, img)
    jpeg_ghosts_60 = foreimg.jpeg_ghost(None, 60, img)
    jpeg_ghosts_80 = foreimg.jpeg_ghost(None, 80, img)

    html = '<div id="toc"> <h3>Table of Contents</h3> </div> <hr/> <div id="contents">'
    html = html + add_pre("Exif-Daten:", exif_str)
    html = html + add("Tamper Detection (Median Filter Noise):", tamper_detection)
    html = html + add("JPEG-Ghosts (20):", jpeg_ghosts_20)
    html = html + add("JPEG-Ghosts (40):", jpeg_ghosts_40)
    html = html + add("JPEG-Ghosts (60):", jpeg_ghosts_60)
    html = html + add("JPEG-Ghosts (80):", jpeg_ghosts_80)
    k = 0
    for i in range (0, 100, 10):
        html = html + add("ELA (Demosaicing artifacts, block size: %d):" %i, ela[k])
        k = k + 1

    html += ' <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>'
    html += '<script type="text/javascript" src="static/index.js"></script>'
    html += '<script type="text/javascript">toc();</script>'

    html += "<div>"

    return html

@app.route('/')
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
