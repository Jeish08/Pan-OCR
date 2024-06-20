from flask import Flask, render_template, request, url_for, Response, jsonify, make_response
import pytesseract
import cv2
from PIL import Image
import json
import pan_read
import io
import numpy as np
import json
import json_serialize
import regex
import pan_read
import re
import nlp

app = Flask(__name__)


@app.route('/homepage/')
def homepage():
    return render_template('index.html')


@app.route("/upload/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        imagefile = request.form["imagefile"]
        image = Image.open(imagefile)
        imag = cv2.imread(imagefile)
        img = cv2.resize(imag, (500, 500))
        roi = cv2.rectangle(img, (5, 140), (350, 460), (255, 0, 0), 2)
        roi = img[140:470, 15: 360]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([360, 255, 80])
        mask = cv2.inRange(hsv, lower_black, upper_black)
        thresh = cv2.threshold(mask, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh)
        if (imagefile) == 'pan1.jpg':
            return nlp.pan_data(text)
        else:
            return pan_read.pan_read_data(text)
@app.route("/gettext")
def gettext():
        with open("templates/sample.json") as fp:
            src = fp.read()
        return Response(
            src,
            mimetype="data/json",
            headers={"Content-disposition":
                     "attachment; filename=sample.json"})


if __name__ == '__main__':
    app.run(debug = True)