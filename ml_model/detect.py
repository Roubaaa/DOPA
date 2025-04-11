import tensorflow as tf
import numpy as np
from PIL import Image
import logging
from pathlib import Path
import cv2
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Initialize model as None
model = None

def load_model():
    """
    Load the model with proper error handling and logging.
    """
    global model
    if model is not None:
        logger.info("Model already loaded")
        return model
        
    try:
        # Get configuration from environment variables
        MODEL_PATH = Path(os.getenv('MODEL_PATH', str(Path(__file__).parent / 'results' / '2025-04-09_wellpad_model_.keras')))
        
        logger.info(f"Attempting to load model from: {MODEL_PATH}")
        if not MODEL_PATH.exists():
            logger.warning(f"Model file not found at {MODEL_PATH}")
            # Try alternative paths
            alternative_paths = [
                Path('/app/ml_model/results/2025-04-09_wellpad_model_.keras'),  # Docker container path
                Path(__file__).parent / 'results' / '2025-04-09_wellpad_model_.keras',  # Local development path
                Path('ml_model/results/2025-04-09_wellpad_model_.keras'),  # Relative path
                Path('/app/ml_model/results/2025-04-09_wellpad_model_.keras')  # Absolute Docker path
            ]
            for path in alternative_paths:
                if path.exists():
                    MODEL_PATH = path
                    logger.info(f"Found model at alternative path: {MODEL_PATH}")
                    break
            
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at any of the checked paths")
            
        # Verify file is readable
        if not os.access(str(MODEL_PATH), os.R_OK):
            raise PermissionError(f"No read permissions for model file at {MODEL_PATH}")
            
        # Log file details
        logger.info(f"Model file size: {MODEL_PATH.stat().st_size} bytes")
        logger.info(f"Model file permissions: {oct(MODEL_PATH.stat().st_mode)[-3:]}")
        
        # Try to read a small portion of the file to verify it's not corrupted
        try:
            with open(str(MODEL_PATH), 'rb') as f:
                header = f.read(100)  # Read first 100 bytes
                if not header:
                    raise ValueError("Model file appears to be empty")
        except Exception as e:
            raise ValueError(f"Error reading model file: {str(e)}")
            
        # Load the model with custom objects
        custom_objects = {
            'bce_dice_loss': bce_dice_loss,
            'dice_loss': dice_loss,
            'dice_coeff': dice_coeff
        }
        
        logger.info("Loading model with custom objects...")
        model = tf.keras.models.load_model(str(MODEL_PATH), custom_objects=custom_objects)
        
        # Verify model was loaded correctly
        if model is None:
            raise ValueError("Model loaded but is None")
            
        logger.info("Model loaded successfully")
        logger.info(f"Model input shape: {model.input_shape}")
        logger.info(f"Model output shape: {model.output_shape}")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        model = None
        raise

# Try to load the model on import
try:
    load_model()
except Exception as e:
    logger.error(f"Failed to load model during import: {e}")
    # Don't raise here, let the application handle it

def preprocess_full_image(img, target_size=(256, 256)):
    """
    Preprocesses the input image: converts to RGB, resizes, normalizes to [0, 1], and returns a Tensor.
    """
    if not isinstance(img, np.ndarray):
        raise ValueError("Input image must be a NumPy array.")
    
    try:
        img = Image.fromarray(img).convert("RGB").resize(target_size)
        img = np.array(img)  # Convert PIL image back to array
        img = tf.image.convert_image_dtype(img, dtype=tf.float32)  # Normalize to [0, 1]
        return img
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def detect_wellpads(image_path, target_size=(256, 256), threshold=0.5):
    """
    Detects wellpads in the image using the model. Processes the entire image without tiling.
    
    Parameters:
        image_path (str): Path to the input image.
        target_size (tuple): Size to which the image should be resized.
        threshold (float): Threshold to convert prediction to binary mask.

    Returns:
        dict: Dictionary containing the mask and overlay images as bytes.
    """
    try:
        # Ensure model is loaded
        if model is None:
            load_model()
        
        # Read the image
        logger.info(f"Reading image from {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Preprocess the image
        img_processed = preprocess_full_image(img, target_size)
        
        # Add batch dimension and predict
        img_batch = tf.expand_dims(img_processed, axis=0)
        logger.info("Running model prediction")
        pred = model.predict(img_batch)
        
        # Remove batch dimension and threshold
        pred = pred[0, :, :, 0]  # Remove batch and channel dimensions
        mask = (pred > threshold).astype(np.uint8) * 255
        
        # Resize mask to original image size
        mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
        
        # Create overlay
        overlay = img.copy()
        overlay[mask > 0] = [255, 0, 0]  # Mark detected areas in red
        
        # Convert to bytes
        _, mask_bytes = cv2.imencode('.png', mask)
        _, overlay_bytes = cv2.imencode('.png', overlay)
        
        logger.info("Detection completed successfully")
        return {
            'mask': mask_bytes.tobytes(),
            'overlay': overlay_bytes.tobytes()
        }
    except Exception as e:
        logger.error(f"Error in detect_wellpads: {e}")
        raise