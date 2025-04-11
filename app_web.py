import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, jsonify, request

# Load environment variables
load_dotenv()

# Create Flask app for web deployment
app = Flask(__name__, static_folder='www')

# Dummy Eel class for compatibility with frontend JavaScript
class DummyEel:
    @staticmethod
    def init(static_folder):
        pass
        
    @staticmethod
    def expose(func):
        return func

# Initialize dummy Eel
try:
    import eel
except ImportError:
    eel = DummyEel()
    
eel.init("www")

# Root route serves index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Serve eel.js if requested
@app.route('/eel.js')
def serve_eel_js():
    return """
    // Dummy eel implementation for web-only deployment
    var eel = {
        _websocket: null,
        set_host: function(host) { /* dummy function */ },
        expose: function(f, name) { /* dummy function */ },
        DisplayMessage: function(message) {
            console.log('Message:', message);
            // You might send this to a display element on the page
        },
        receiverText: function(text) {
            console.log('Received:', text);
            // Add to chat interface if needed
        }
    };
    """

# Simple API endpoint to demonstrate functionality
@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "message": "YUZI backend is running"
    })
    
# API endpoint to handle messages
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    
    # In a full implementation, this would process the message
    # and return an appropriate response
    return jsonify({
        "response": f"You said: {message}",
        "status": "success"
    })

if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    
    # Start the application
    app.run(host=host, port=port) 