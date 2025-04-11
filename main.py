import os
import eel
from dotenv import load_dotenv

from engine.features import * 
from engine.command import *

# Load environment variables
load_dotenv()

def start():
    # Initialize Eel with the frontend directory
    eel.init("www")
    
    # Play assistant sound
    playAssistantSound()

    # Check if we're running in development mode
    if os.environ.get('ENVIRONMENT', 'development') == 'development':
        # Used as a pop up window to open the browser window in development
        os.system('start chrome.exe --app="http://localhost:8000/index.html"')
        # Start the Eel app in development mode
        eel.start('index.html', mode=None, host='localhost', port=8000, block=True)
    else:
        # In production, we'll use the host and port provided by the environment
        host = os.environ.get('HOST', '0.0.0.0')
        port = int(os.environ.get('PORT', 8000))
        eel.start('index.html', mode=None, host=host, port=port, block=True)