import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__, static_folder='www')

@app.route('/')
def index():
    return "Yuzi Backend API is running! Access web interface for full functionality."

@app.route('/static/<path:path>')
def serve_static(path):
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
        response = f"Received command: {query}"
    
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
    # For local development
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 