# YUZI - Personal AI Assistant

YUZI is a personal AI assistant that can help with various tasks like opening applications, playing YouTube videos, answering questions, and more.

## Features

- Voice commands recognition
- Opening applications and websites
- Playing YouTube videos
- WhatsApp messaging integration
- AI chat bot capabilities

## Project Structure

- `www/`: Frontend files (HTML, CSS, JS)
- `engine/`: Backend Python modules
- `app.py`: Entry point for production deployment
- `main.py`: Main application logic
- `run.py`: Development entry point

## Local Development Setup

1. Clone the repository
   ```
   git clone https://github.com/yourusername/yuzi.git
   cd yuzi
   ```

2. Create a virtual environment
   ```
   python -m venv envyuzi
   source envyuzi/bin/activate  # On Windows: envyuzi\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`
   ```
   cp .env.example .env
   ```

5. Run the application
   ```
   python run.py
   ```

## Deployment

### Backend on Render

1. Create a new Web Service on Render
2. Link it to your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app`
5. Add environment variables:
   - `ENVIRONMENT`: Set to `production`
   - `DATABASE_URL`: Your PostgreSQL URL (if using a database)
   - `PORT`: Default is 8000

### Frontend on Netlify

1. Configure your Netlify site to deploy from the `www/` directory
2. Update the WebSocket connection URL in `www/controller.js` to point to your Render backend

## Environment Variables

See `.env.example` for required environment variables.

## Technologies Used

- Python with Eel for backend-frontend communication
- HTML/CSS/JS for frontend
- Flask for web server in production
- SQLite for local development, PostgreSQL for production 