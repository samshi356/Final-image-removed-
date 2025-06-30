import os
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
RESULT_FOLDER = 'result'

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            if 'image' not in request.files:
                return "No file uploaded", 400

            image = request.files['image']
            if image.filename == '':
                return "No file selected", 400

            input_path = os.path.join(UPLOAD_FOLDER, image.filename)
            output_path = os.path.join(RESULT_FOLDER, "output_" + image.filename)
            image.save(input_path)

            with Image.open(input_path) as img:
                output = remove(img)
                output.save(output_path)

            return send_file(output_path, as_attachment=True)

        return render_template('index.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
    
