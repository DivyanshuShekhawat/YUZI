# Step-by-Step Render Deployment Guide

## Step 1: Prepare Your Repository
1. Make sure your repository contains these files:
   - requirements.txt
   - render.yaml
   - wsgi.py
   - .env.sample (rename to .env for local use)

2. Don't commit sensitive files:
   - Keep engine/cookies.json locally
   - Keep .env locally (if you created one)

## Step 2: Push to GitHub
1. Create a new repository on GitHub.com
2. Open command prompt in your project folder
3. Run the following commands:
   ```
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Step 3: Set Up Render Service
1. Go to https://render.com/ and sign up/sign in
2. Click on "New" and select "Web Service"
3. Connect your GitHub account if not already done
4. Select your Yuzi repository
5. Render should auto-detect the render.yaml configuration
6. Click "Create Web Service"

## Step 4: Add Secret Files on Render
1. After creating the service, go to the "Settings" tab
2. Scroll down to "Secret Files" section
3. Click "Add Secret File"
4. For cookies.json:
   - File Path: `/app/engine/cookies.json`
   - Contents: Copy and paste the content of your local engine/cookies.json file
5. Click "Save Changes"

## Step 5: Add Environment Variables on Render
1. In the same Settings page, go to "Environment" section
2. Click "Add Environment Variable"
3. Add these variables:
   - Key: `ASSISTANT_NAME` | Value: `Y.U.Z.I`
   - Key: `PORT` | Value: `8000`
   - Add any other variables from your .env file if needed
4. Click "Save Changes"

## Step 6: Deploy your Service
1. Go to the "Manual Deploy" tab
2. Select "Clear build cache & deploy"
3. Click "Deploy"
4. Wait for the deployment to complete

## Step 7: Verify Deployment
1. Once deployment is complete, click on the URL provided
2. You should see: "Yuzi Backend API is running! Access web interface for full functionality."
3. Test the API with a REST client like Postman or using curl:
   ```
   curl -X POST https://your-service-url.onrender.com/api/command -H "Content-Type: application/json" -d '{"command":"tell me a joke"}'
   ```

## Notes About Environment Files
- The `.env` file is for local development only - do not upload to GitHub
- On Render, use the "Environment Variables" section instead
- The cookies.json file contains authentication info for HugChat - upload it via "Secret Files" 