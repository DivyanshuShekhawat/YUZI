import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, jsonify

# Load environment variables
load_dotenv()

# Create Flask app for web deployment
app = Flask(__name__, static_folder='www')

# Root route serves index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Simple API endpoint to demonstrate functionality
@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "message": "YUZI backend is running"
    })

if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    
    # Start the application
    app.run(host=host, port=port) 