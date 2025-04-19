import os
import eel
from engine.features import *
from engine.command import *
from flask import Flask

# Initialize Flask app for Render
app = Flask(__name__)

# Configure Eel
eel.init("www")

@app.route('/')
def index():
    return "Yuzi Backend API is running! Access web interface for full functionality."

@app.route('/api/command', methods=['POST'])
def process_command():
    from flask import request
    query = request.json.get('command', '')
    # Process the command using allCommands
    try:
        return {"status": "success", "response": allCommands(query)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 