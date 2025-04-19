import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__, static_folder='www')
# Enable CORS for all routes
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

@app.route('/<path:path>')
def serve_any_file(path):
    return app.send_static_file(path)

@app.route('/api/command', methods=['POST'])
def process_command():
    query = request.json.get('command', '') if request.json else ''
    
    # Process based on command type
    if query.lower().startswith('open'):
        app_name = query.lower().replace('open', '').strip()
        response = f"The command to open {app_name} was received, but cannot be executed in cloud environment."
    elif "on youtube" in query.lower():
        search_term = query.lower().replace('play', '').replace('on youtube', '').strip()
        response = f"The command to play '{search_term}' on YouTube was received."
    else:
        # Try to get a more meaningful response
        try:
            from engine.features import simple_fallback_response
            response = simple_fallback_response(query)
        except:
            response = f"I received your message: {query}"
    
    return jsonify({
        "status": "success", 
        "response": response,
        "environment": "cloud"
    })

@app.route('/healthcheck')
def healthcheck():
    """Health check endpoint for Render"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # For local development, use the PORT environment variable or default to 10000
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 