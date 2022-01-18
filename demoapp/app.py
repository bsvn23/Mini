from crypt import methods
import os
import tensorflow as tf
import numpy as np
import keras as k
from keras.models import load_model
from keras.preprocessing import image
from PIL.Image import open
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)

model= load_model('/home/saivnb/Downloads/vgg_model_brain.h5')

def getClassName(classNo):
    if classNo == 0:
        return "No Brain Tumor"
    else:
        return "Yes Brain Tumor"
    
def getResult(fpath):
    l=[]
    img=np.asarray(open(fpath).resize((224,224)))
    b_img=img.astype(np.float32)
    img_array=image.img_to_array(b_img)
    i=k.applications.vgg16.preprocess_input(img_array)
    l.append(i)

    xx=np.array(l)

    abc=model.predict(xx)
    c=round(abc[0][0])
    return c

@app.route("/",methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath=os.path.dirname(__file__)
        file_path=os.path.join(basepath,'uploads',secure_filename(f.filename))
        f.save(file_path)
        value=getResult(file_path)
        result=getClassName(value)
        return result
    return None

if __name__=='__main__':
    app.run(debug=True)