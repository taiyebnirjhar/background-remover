from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
from io import BytesIO
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains (allowing all origins)
CORS(app, origins="*")

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Get image from POST request
        image_file = request.files['image']

        if not image_file:
            return jsonify({"error": "No image file provided"}), 400

        input_image = Image.open(image_file)

        # Remove background
        output_image = remove(input_image)

        # Save to a byte stream and send as response
        img_byte_arr = BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='output.png')

    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return jsonify({"error": "Failed to process the image"}), 500

if __name__ == '__main__':
    # Use Gunicorn for production deployment
    app.run(host='0.0.0.0', port=5050, debug=False)
