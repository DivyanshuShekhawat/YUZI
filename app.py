"""
This file exists only for compatibility.
The actual application is in app_web.py.
This file just imports from there to make the Render deployment work.
"""

import os
from app_web import app

# This file is not meant to be run directly,
# but if it is, it will just run the real app
if __name__ == "__main__":
    # Get the PORT from environment variable (important for Render)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 