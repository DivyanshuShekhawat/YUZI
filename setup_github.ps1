# Initialize git repository if not already initialized
if (-not (Test-Path .git)) {
  git init
  Write-Host "Git repository initialized"
}

# Add all files to git (except those in .gitignore)
git add .

# Initial commit
git commit -m "Initial commit for Yuzi project deployment"

$username = Read-Host -Prompt "Enter your GitHub username"
$repo_name = Read-Host -Prompt "Enter your GitHub repository name (e.g. yuzi)"

# Add GitHub remote
git remote add origin "https://github.com/$username/$repo_name.git"

Write-Host "Remote added. Now you can push your code with:"
Write-Host "git push -u origin main"

Write-Host "Remember to create the repository on GitHub first at: https://github.com/new" 