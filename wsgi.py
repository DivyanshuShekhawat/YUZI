import os
import eel
from flask import Flask, request, jsonify
import sys

# Initialize Flask app for Render
app = Flask(__name__)

# Configure Eel
eel.init("www")

# Create mock functions for modules that won't work in cloud environment
def initialize_mocks():
    # This function creates mock implementations for dependencies that
    # won't work in the cloud environment
    class MockPyAudio:
        def __init__(self):
            pass
            
        def open(self, *args, **kwargs):
            return None
            
    class MockAutogui:
        def keyDown(self, *args, **kwargs):
            pass
            
        def keyUp(self, *args, **kwargs):
            pass
            
        def press(self, *args, **kwargs):
            pass
            
        def hotkey(self, *args, **kwargs):
            pass
            
    # Insert mocks into sys.modules to prevent import errors
    sys.modules['pyaudio'] = type('', (), {'PyAudio': MockPyAudio})
    sys.modules['pyautogui'] = MockAutogui()

# Initialize mocks before importing the rest of the app
initialize_mocks()

# Now import the app modules
try:
    from engine.features import *
    from engine.command import *
except Exception as e:
    print(f"Error importing app modules: {str(e)}")
    
# Define a function to safely call allCommands
def safe_all_commands(query):
    try:
        # Check if allCommands is available
        if 'allCommands' in globals():
            return allCommands(query)
        else:
            return {"error": "Command handling not available in cloud environment"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return "Yuzi Backend API is running! Access web interface for full functionality."

@app.route('/api/command', methods=['POST'])
def process_command():
    query = request.json.get('command', '')
    # Process the command using allCommands
    try:
        result = safe_all_commands(query)
        return {"status": "success", "response": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 