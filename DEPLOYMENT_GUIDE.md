# Yuzi Deployment Guide

This guide walks through the steps to push your code to GitHub and deploy it on Render.

## 1. Push Code to GitHub

### If you don't have a GitHub repository yet:

1. Create a new repository on GitHub
2. Initialize your local repository and push:

```bash
# Initialize Git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/yuzi.git

# Push to GitHub
git push -u origin main  # or master, depending on your branch name
```

### If you already have a GitHub repository:

```bash
# Add all files
git add .

# Commit changes
git commit -m "Prepare for Render deployment"

# Push to GitHub
git push
```

## 2. Deploy on Render

1. Sign in to [Render](https://render.com)
2. Click "New" and select "Web Service"
3. Connect your GitHub account if not already connected
4. Find and select your Yuzi repository
5. Render will automatically detect the `render.yaml` configuration
6. Click "Create Web Service"

## 3. Set Up Secret Files

After deployment starts:

1. Go to your service's "Settings" tab
2. Scroll down to "Secret Files"
3. Click "Add Secret File"
4. Use the following settings:
   - Filename: `/app/engine/cookies.json`
   - Contents: Copy and paste the contents of your local `engine/cookies.json` file
5. Click "Save Changes"
6. Restart your service to apply the changes

## 4. Verify Deployment

1. Once deployment completes, click on your service's URL
2. You should see the message: "Yuzi Backend API is running! Access web interface for full functionality."
3. Test the API with a tool like Postman or curl:

```bash
curl -X POST https://your-service-url.onrender.com/api/command \
  -H "Content-Type: application/json" \
  -d '{"command":"tell me a joke"}'
```

## Troubleshooting

- **Build Failure**: Check build logs for specific errors
- **Runtime Errors**: Check service logs in Render dashboard
- **Missing Dependencies**: Update `requirements.txt` if needed
- **Secret File Issues**: Verify the path is exactly `/app/engine/cookies.json` 