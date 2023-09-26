
from flask import Flask
from flask import jsonify, request, render_template, flash, redirect, url_for
import os

from werkzeug.utils import secure_filename
from Extractor import extract_para_head_bullet_num



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # Check if the file has a valid extension
        if file and allowed_file(file.filename):
            # Securely save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".pdf")

            # Check if the UPLOAD_FOLDER directory exists, and create it if not
            if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])

            # Open the file in binary write mode and write the binary content
            with open(filepath, 'wb') as f:
                f.write(file.read())

            # Call your address_extraction function here with the uploaded file
            extracted_addresses = extract_para_head_bullet_num(filepath)

            # Convert the extracted addresses into a list of dictionaries
            addresses_json = [{"text": obj.text, "bbox": obj.bbox} for obj in extracted_addresses]

            return jsonify(addresses_json)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
 