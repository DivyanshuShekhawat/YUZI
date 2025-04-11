"""
This file exists only for compatibility.
The actual application is in app_web.py.
This file just imports from there to make the Render deployment work.
"""

# Import the app from app_web
from app_web import app

# This file is not meant to be run directly,
# but if it is, it will just run the real app
if __name__ == "__main__":
    app.run() 