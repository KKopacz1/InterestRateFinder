import os
import io
import numpy as np
from PIL import Image
import base64

import tensorflow as tf

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras import backend as K

from flask import Flask, request, redirect, jsonify, render_template
#import deeplearning modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.utils import to_categorical

app = Flask(__name__)
model = None
graph = None

def load_model():
    global model
    global graph
    model = keras.models.load_model("loan_model_trained.h5")
    graph = K.get_session().graph

load_model()

# def prepare_image(image):
#     if image.mode != "RGB":
#         image = image.convert("RGB")
#     image_size = (28, 28)
#     image = image.resize(image_size)
#     # image.save("fromform.png")
#     image = img_to_array(image)[:,:,0]
#     image /= 255
#     image = 1 - image
#     return image.flatten().reshape(-1, 28*28)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        if request.form.get('credit_score'):
            # read the base64 encoded string
            #image_string = request.form.get('digit')

            investment = request.form.get('investment')
            term = request.form.get('term')
            grade = request.form.get('grade')
            employment_length = request.form.get('employment_length')
            home_ownership = request.form.get('home_ownership')
            annual_income=request.form.get('annual_income')
            purpose = request.form.get('purpose')
            state = request.form.get('state')
            dti_ratio = request.form.get('dti_ratio')
            delinquency = request.form.get('delinquency')

            loan_array = [investment,term,grade,employment_length,home_ownership,annual_income,purpose,state,dti_ratio,delinquency]

            #construct loan_input
            for column in loan_array:
    
                if column.dtype == type(object):
                    le = LabelEncoder()
                    column=le.fit_transform(column.astype(str))

            X_scaler = StandardScaler().fit(loan_array)

            X_test_scaled = X_scaler.transform(loan_array)

            # Get the tensorflow default graph
            global graph
            with graph.as_default():

                # Use the model to make a prediction
                predicted_interest_rate = model.predict_classes(X_test_scaled)
                data["prediction"] = str(predicted_interest_rate)

                # indicate that the request was a success
                data["success"] = True

        return jsonify(data)
    return render_template("index.html")

if __name__ == "__main__":
    load_model()
    app.run()
