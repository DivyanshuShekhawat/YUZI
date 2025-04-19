# Yuzi - AI Voice Assistant

A personal AI assistant that can open applications, play YouTube videos, and answer questions.

## Deploying to Render

### Prerequisites
1. A Render account (https://render.com)
2. HugChat cookies.json file (for AI functionality)

### Step 1: Prepare your environment files
1. The `cookies.json` file from HugChat is required and should be in the `engine` folder
2. Ensure you have all the required files:
   - requirements.txt
   - render.yaml
   - wsgi.py

### Step 2: Set up environment variables on Render
When creating your web service on Render, add the following environment variables:
- `PORT`: 8000 (or your preferred port)
- `ASSISTANT_NAME`: Y.U.Z.I (or your custom name)

### Step 3: Deploy on Render
1. Connect your repository to Render
2. Use the existing `render.yaml` configuration
3. Deploy the service

### Step 4: Configure secrets file
1. In Render dashboard, go to your service settings
2. Under "Secret Files", add:
   - Mount path: `/app/engine/cookies.json`
   - Contents: Copy the contents of your local `engine/cookies.json` file

## Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run with: `python run.py`

## API Endpoints
- `GET /`: Check if API is running
- `POST /api/command`: Send commands to the assistant
  - Body: `{"command": "open chrome"}` 