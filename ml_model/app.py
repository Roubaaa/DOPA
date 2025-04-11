from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import base64
import sys
from pathlib import Path
from flask_cors import CORS
import logging
import time
import stat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
from ml_model.detect import detect_wellpads, load_model

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure environment variables with defaults
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(Path(__file__).parent / 'uploads'))
MODEL_PATH = os.getenv('MODEL_PATH', str(Path(__file__).parent / 'results' / '2025-04-09_wellpad_model_.keras'))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Initialize directories
def initialize_directories():
    try:
        # Create upload directory if it doesn't exist
        upload_path = Path(UPLOAD_FOLDER)
        upload_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Upload directory {upload_path} created or exists")
        
        # Verify model file exists and is readable
        model_path = Path(MODEL_PATH)
        if not model_path.exists():
            logger.error(f"Model file not found at {model_path}")
            # Try alternative paths
            alt_paths = [
                Path(__file__).parent / 'results' / '2025-04-09_wellpad_model_.keras',
                Path(__file__).parent.parent / 'ml_model' / 'results' / '2025-04-09_wellpad_model_.keras'
            ]
            
            for alt_path in alt_paths:
                if alt_path.exists():
                    logger.info(f"Found model at alternative path: {alt_path}")
                    model_path = alt_path
                    break
            else:
                raise FileNotFoundError(f"Model file not found at any of: {[str(p) for p in [model_path] + alt_paths]}")
        
        logger.info(f"Model file found at {model_path}")
        return True
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return False

# Initialize on startup
if not initialize_directories():
    logger.error("Failed to initialize directories")
    sys.exit(1)

app.config.update(
    UPLOAD_FOLDER=str(UPLOAD_FOLDER),
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max file size
    MODEL_PATH=str(MODEL_PATH)
)

@app.route('/health', methods=['GET'])
def health_check():
    start_time = time.time()
    health_status = {
        "status": "healthy",
        "checks": {
            "upload_directory": False,
            "model_loading": False,
            "environment": FLASK_ENV,
            "model_path": str(MODEL_PATH)
        },
        "timestamp": start_time
    }
    
    try:
        # Check upload directory
        upload_path = Path(UPLOAD_FOLDER)
        if upload_path.exists():
            health_status["checks"]["upload_directory"] = True
        else:
            raise Exception(f"Upload directory not found at {upload_path}")
        
        # Check model loading
        try:
            model = load_model()
            if model is not None:
                health_status["checks"]["model_loading"] = True
            else:
                raise Exception("Model loaded but returned None")
        except Exception as e:
            logger.error(f"Model loading check failed: {e}")
            raise Exception(f"Model loading failed: {str(e)}")
        
        # Calculate response time
        health_status["response_time"] = time.time() - start_time
        return jsonify(health_status), 200
        
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
        health_status["response_time"] = time.time() - start_time
        logger.error(f"Health check failed: {e}")
        return jsonify(health_status), 500

@app.route('/api/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        logger.info(f"File saved to {filepath}")
        
        results = detect_wellpads(filepath)
        logger.info("Detection completed successfully")
        
        # Convert results to base64
        mask_base64 = base64.b64encode(results['mask']).decode('utf-8')
        overlay_base64 = base64.b64encode(results['overlay']).decode('utf-8')
        
        # Clean up the uploaded file
        os.remove(filepath)
        logger.info(f"Temporary file {filepath} removed")
        
        return jsonify({
            "mask": mask_base64,
            "overlay": overlay_base64
        }), 200
    except Exception as e:
        logger.error(f"Detection failed: {e}")
        # Clean up the uploaded file in case of error
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up temporary file {filepath} after error")
            except Exception as cleanup_error:
                logger.error(f"Failed to clean up temporary file: {cleanup_error}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get host from environment variable or default to 0.0.0.0
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    
    # Log the configuration
    logger.info(f"Starting Flask server on {host}:{port}")
    logger.info(f"Environment: {FLASK_ENV}")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    
    app.run(host=host, port=port, debug=(FLASK_ENV == 'development')) 