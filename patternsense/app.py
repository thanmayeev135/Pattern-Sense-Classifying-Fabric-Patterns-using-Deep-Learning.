import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

MODEL_PATH = 'model_cnn(2).h5'

model = None
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('home.html')
def home_redirect():
    return redirect(url_for('home'))

@app.route('about.html')
def about():
    return render_template('about.html')

@app.route('contact.html')
def contact():
    return render_template('contact.html')

@app.route('predict.html')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('predictionpage.html', prediction_result="No file part in the request.", uploaded_image_url="")

    file = request.files['file']

    if file.filename == '':
        return render_template('predictionpage.html', prediction_result="No selected file.", uploaded_image_url="")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        prediction_result = f"Image uploaded successfully! Filename: {filename}. <br> Model not loaded for prediction (placeholder result)."

        uploaded_image_url = url_for('uploaded_file', filename=filename)

        return render_template('predictionpage.html',
                               prediction_result=prediction_result,
                               uploaded_image_url=uploaded_image_url)
    else:
        return render_template('predictionpage.html',
                               prediction_result="Invalid file type. Please upload an image (png, jpg, jpeg, gif).",
                               uploaded_image_url="")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
