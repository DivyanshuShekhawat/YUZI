#!/bin/bash

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
  git init
  echo "Git repository initialized"
fi

# Add all files to git (except those in .gitignore)
git add .

# Initial commit
git commit -m "Initial commit for Yuzi project deployment"

echo "Enter your GitHub username:"
read username

echo "Enter your GitHub repository name (e.g. yuzi):"
read repo_name

# Add GitHub remote
git remote add origin https://github.com/$username/$repo_name.git

echo "Remote added. Now you can push your code with:"
echo "git push -u origin main"

echo "Remember to create the repository on GitHub first at: https://github.com/new" 