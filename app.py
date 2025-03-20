import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import numpy as np
#from keras.preprocessing import image
from tensorflow.keras.preprocessing import image



model=load_model("Esophageal_model.h5")

UPLOAD_FOLDER = 'static/img'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Home Page
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/prediction', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        import uuid
        u = uuid.uuid4()
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename="temp"+u.hex+".jpg"
            fullname=os.path.join(UPLOAD_FOLDER, "temp"+u.hex+".jpg")
            file.save(fullname)
            test_image = image.load_img('static/img/'+filename, target_size = (224,224))
            test_image = image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis = 0)
            test_image = test_image.astype('float') / 255
            result = model.predict(test_image)
            pred_prob = result.item()
            print(result)
            if result[0]>0.5:
                label = 'NON-Esophageal'
                accuracy = round(pred_prob * 100, 2)
            else:
                pred_1 = round((1 - pred_prob) * 100, 2)
                if pred_1 < 75:
                    label = 'Early Detection of Esophageal'
                    accuracy = round((1 - pred_prob) * 100, 2)
                else:
                    label = 'Esophageal'
                    accuracy = round((1 - pred_prob) * 100, 2)
                    
         
    return render_template('index.html', label=label, image_file_name=filename, accuracy=accuracy)


@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=False)
    
    
    
