import os
from uuid import uuid4
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
from scipy.ndimage import imread
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D,Flatten
from os import rename, listdir
from keras.models import model_from_json
from flask import Flask, request, render_template, send_from_directory
from keras import backend as K

app = Flask(__name__)
# app = Flask(__name__, static_folder="images")



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    K.clear_session()
    if(createPredictionData(str("./images/"+filename))):
        return render_template("hotdog.html", image_name=filename)
    else:
        return render_template("nothotdog.html", image_name=filename)
    # return send_from_directory("images", filename, as_attachment=True)
    

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

def resizeImage(path):
    img = Image.open(path)
    new_img = img.resize((250,250))
    new_img.save(path)

def normalize(x_train):
    x_train_normalized = x_train/255
    return x_train_normalized

def createPredictionData(path):
    resizeImage(path)

    img = img_to_array(load_img(path))
    img = np.array(img)
    img = normalize(img)
    img = np.expand_dims(img, axis=0)

    model = openModel()
    if(model.predict_classes(img) == 1):
        print("This is a hotdog!")
        return True
    else:
        print("This is not a hotdog :(")
        return False

def openModel():
    jsonFile = open("model.json","r")
    model = model_from_json(jsonFile.read())
    model.load_weights("model.h5")
    jsonFile.close()
    return model

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=80, debug=False)
    