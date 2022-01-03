#Load Libraries to run our applications
import io
import os
import sys
import random
import warnings
import cv2
import numpy as np
import flask
from tqdm import tqdm
from PIL import Image

import keras
keras.backend.clear_session()
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.models import load_model
from skimage.io import imread, imshow
import matplotlib.pyplot as plt
from skimage.transform import resize
from skimage.morphology import label


#Initialize flask application & Keras model
app = flask.Flask(__name__)
#app.run(host='0.0.0.0', port=5000)
def index():
  return "Hello world!"

model = None

# Set some parameters
IMG_WIDTH = 512
IMG_HEIGHT = 512
IMG_CHANNELS = 1

warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
seed = 42
random.seed = seed
np.random.seed = seed
sizes_test=[]
#load model function
def pre_load_model():
    # load the pre-trained Keras model
    global model
    model = load_model('model-POSITIVE-198-1.h5',compile=False)
    model._make_predict_function()
    print(model.summary() )

def rle_encoding(x):
    dots = np.where(x.T.flatten() == 1)[0]
    run_lengths = []
    prev = -2
    for b in dots:
        if (b>prev+1): run_lengths.extend((b + 1, 0))
        run_lengths[-1] += 1
        prev = b
    return run_lengths

def prob_to_rles(x, cutoff=0.3):
    lab_img = label(x > cutoff)
    for i in range(1, lab_img.max() + 1):
        yield rle_encoding(lab_img == i)


#Pre-processing of the image
def prepare_image(image, target):
    #if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    print(image.size)
    image = image.resize(target)
    image = img_to_array(image)
    #image = np.expand_dims(image, axis=0)
    # return the processed image
    #return X_test2
    return image

# this method processes any requests to the /predict endpoind
@app.route("/predict", methods=["POST"])
def predict():
    #global image
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(512, 512))
            X_test = image[:,:,0]
            X_test3=np.expand_dims(X_test, axis=0)
            X_test2=np.expand_dims(X_test3, axis=3)
            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds_test = model.predict(X_test2)

            preds_test_t = (preds_test > 0.3).astype(np.uint8)

            sizes_test.append([image.shape[0], image.shape[1]])
            #preds_test_upsampled = []
            preds_test_upsampled=resize(np.squeeze(preds_test),sizes_test[0], mode='constant', preserve_range=True)#TRUE
            print("***********************************")
            #print(preds_test_upsampled)
            #print("Len: ",len(preds_test_upsampled))
            #print("size: ",preds_test_upsampled.size)
            print("***********************************")
            test_rle = list(prob_to_rles(preds_test_upsampled))
            print(test_rle)
            print("predicted********************************************")
            #results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = [len(test_rle)]
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    #index()
    pre_load_model()
    app.run(host= '192.168.0.112', port = 5000)
    #app.run(host='0.0.0.0', port=5000)
    #app.run()
