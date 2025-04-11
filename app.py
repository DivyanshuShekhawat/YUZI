import os
import eel
from dotenv import load_dotenv
from flask import Flask, send_from_directory

# Load environment variables
load_dotenv()

# Set environment to production
os.environ["ENVIRONMENT"] = "production"

# Initialize Eel with the frontend directory
eel.init("www")

# Create Flask app for gunicorn
app = Flask(__name__, static_folder='www')

# Root route serves index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Add Eel's websocket route
@app.route('/eel.js')
def serve_eel():
    return send_from_directory(app.static_folder, 'eel.js')

if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    
    # Start the application
    app.run(host=host, port=port) 