import tensorflow as tf
import numpy as np
from PIL import Image
import logging
from pathlib import Path
import cv2
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO

# Get configuration from environment variables
PORT = int(os.getenv('PORT', '5000'))
HOST = os.getenv('HOST', '0.0.0.0')
MODEL_PATH = Path(os.getenv('MODEL_PATH', str(Path(__file__).parent / 'results' / '2025-04-09_wellpad_model_.keras')))
ML_SERVICE_URL = os.getenv('ML_SERVICE_URL', 'http://localhost:3000/api/ml/detect')
PYTHON_BACKEND_URL = os.getenv('PYTHON_BACKEND_URL', 'http://localhost:5000/api/detect')

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define custom loss functions
@tf.keras.utils.register_keras_serializable()
def dice_coeff(y_true, y_pred):
    smooth = 1.0
    y_true_f = tf.reshape(y_true, [-1])
    y_pred_f = tf.reshape(y_pred, [-1])
    intersection = tf.reduce_sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)

@tf.keras.utils.register_keras_serializable()
def dice_loss(y_true, y_pred):
    return 1 - dice_coeff(y_true, y_pred)

@tf.keras.utils.register_keras_serializable()
def bce_dice_loss(y_true, y_pred):
    return tf.keras.losses.binary_crossentropy(y_true, y_pred) + dice_loss(y_true, y_pred)

# Load the model
try:
    print(f"Attempting to load model from: {MODEL_PATH}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
    model = tf.keras.models.load_model(str(MODEL_PATH), 
                                      custom_objects={
                                          'bce_dice_loss': bce_dice_loss,
                                          'dice_loss': dice_loss,
                                          'dice_coeff': dice_coeff
                                      })
    print("Model loaded successfully")
    print(f"Model input shape: {model.input_shape}")
    print(f"Model output shape: {model.output_shape}")
    logging.info("Model loaded successfully")
    logging.info(f"Model input shape: {model.input_shape}")
    logging.info(f"Model output shape: {model.output_shape}")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    logging.error(f"Error loading model: {str(e)}")
    model = None

def preprocess_full_image(img, target_size=(256, 256)):
    """
    Preprocesses the input image: converts to RGB, resizes, normalizes to [0, 1], and returns a Tensor.
    """
    if not isinstance(img, np.ndarray):
        raise ValueError("Input image must be a NumPy array.")
    
    img = Image.fromarray(img).convert("RGB").resize(target_size)
    img = np.array(img)  # Convert PIL image back to array
    img = tf.image.convert_image_dtype(img, dtype=tf.float32)  # Normalize to [0, 1]

    return img  # No batch dimension yet

def detect_wellpads(image, model, target_size=(256, 256), threshold=0.5):
    """
    Detects wellpads in the image using the model. Processes the entire image without tiling.
    
    Parameters:
        image (np.ndarray): Input image as a NumPy array.
        model (tf.keras.Model): Trained segmentation model.
        target_size (tuple): Size to which the image should be resized.
        threshold (float): Threshold to convert prediction to binary mask.

    Returns:
        np.ndarray: Binary mask with shape equal to original image, dtype=np.uint8.
    """
    original_size = image.shape[:2]  # (height, width)
    
    input_image = preprocess_full_image(image, target_size)
    input_tensor = tf.expand_dims(input_image, axis=0)  # Add batch dimension

    prediction = model.predict(input_tensor, verbose=0)[0]
    pred_mask = prediction[..., 0]  # Get the single-channel mask

    # Resize mask back to original image size
    pred_mask_resized = tf.image.resize(pred_mask[..., tf.newaxis], original_size, method='bilinear')
    pred_mask_resized = tf.squeeze(pred_mask_resized, axis=-1).numpy()

    # Apply threshold to get binary mask
    binary_mask = (pred_mask_resized > threshold).astype(np.uint8) * 255

    return binary_mask

@app.route('/api/detect', methods=['POST', 'OPTIONS'])
def detect():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        if 'image' not in request.files:
            logging.error("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
            
        file = request.files['image']
        logging.info(f"Received image file: {file.filename}")
        
        # Read image
        try:
            img_bytes = file.read()
            if not img_bytes:
                logging.error("Empty image file")
                return jsonify({'error': 'Empty image file'}), 400
                
            img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                logging.error("Failed to decode image")
                return jsonify({'error': 'Failed to decode image'}), 400
                
            logging.info(f"Image shape: {img.shape}")
        except Exception as e:
            logging.error(f"Error reading image: {str(e)}")
            return jsonify({'error': f'Failed to read image: {str(e)}'}), 400
            
        # Convert BGR to RGB
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            logging.error(f"Error converting image: {str(e)}")
            return jsonify({'error': f'Failed to convert image: {str(e)}'}), 400
        
        # Check if model is loaded
        if model is None:
            logging.error("Model is not loaded")
            return jsonify({'error': 'Model is not loaded. Please check the model path and try again.'}), 500
        
        # Run detection
        try:
            print("Starting detection...")
            mask = detect_wellpads(img_rgb, model)
            print(f"Detection completed. Mask shape: {mask.shape}")
            logging.info(f"Detection completed. Mask shape: {mask.shape}")
        except Exception as e:
            print(f"Error in detection: {str(e)}")
            logging.error(f"Error in detection: {str(e)}")
            return jsonify({'error': f'Detection failed: {str(e)}'}), 500
        
        # Create overlay
        try:
            overlay = img.copy()
            overlay[mask == 255] = [0, 255, 0]  # Highlight detected regions in green
        except Exception as e:
            logging.error(f"Error creating overlay: {str(e)}")
            return jsonify({'error': f'Failed to create overlay: {str(e)}'}), 500
        
        # Convert results to base64
        try:
            _, mask_buffer = cv2.imencode('.png', mask)
            _, overlay_buffer = cv2.imencode('.png', overlay)
            
            mask_base64 = base64.b64encode(mask_buffer).decode('utf-8')
            overlay_base64 = base64.b64encode(overlay_buffer).decode('utf-8')
            
            print("Successfully processed image")
            logging.info("Successfully processed image")
            
            response = jsonify({
                'mask': mask_base64,
                'overlay': overlay_base64
            })
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            return response
        except Exception as e:
            logging.error(f"Error encoding results: {str(e)}")
            return jsonify({'error': f'Failed to encode results: {str(e)}'}), 500
        
    except Exception as e:
        print(f"Unexpected error in detection: {str(e)}")
        logging.error(f"Unexpected error in detection: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    try:
        print(f"Starting Flask server on {HOST}:{PORT}...")
        if model is None:
            print("ERROR: Model failed to load. Server will not start.")
            exit(1)
        app.run(host=HOST, port=PORT, debug=True)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        logging.error(f"Error starting server: {str(e)}")
        exit(1)