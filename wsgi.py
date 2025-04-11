"""
WSGI entry point for Render deployment.
This file is needed because Render may look for wsgi.py by default.
"""

import os
from app_web import app

# For Gunicorn
application = app

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 