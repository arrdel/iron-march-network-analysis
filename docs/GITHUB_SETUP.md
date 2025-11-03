# GitHub Setup Guide

This guide will help you push your restructured project to GitHub.

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and log in to your account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `iron-march-network-analysis` (or your preferred name)
   - **Description**: Network analysis toolkit for studying far-right forum interactions
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Configure Git User (if not already done)

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"
```

## Step 3: Add Remote Repository

After creating the repository on GitHub, you'll see a page with commands. Use these commands:

```bash
# Navigate to your project directory
cd /home/adelechinda/home/semester_projects/knowledge_graph

# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/iron-march-network-analysis.git

# Verify the remote was added
git remote -v
```

## Step 4: Push to GitHub

```bash
# Push your code to GitHub
git push -u origin main
```

If you're using HTTPS and need to authenticate:
- GitHub no longer accepts passwords for git operations
- You'll need to use a **Personal Access Token (PAT)**

### Creating a Personal Access Token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Iron March Project")
4. Set expiration (recommended: 90 days)
5. Select scopes: Check "repo" for full repository access
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)
8. Use this token as your password when git asks for authentication

## Step 5: Alternative - Using SSH (Recommended)

SSH is more secure and convenient:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start the ssh-agent
eval "$(ssh-agent -s)"

# Add your SSH key
ssh-add ~/.ssh/id_ed25519

# Copy your public key
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to GitHub Settings → SSH and GPG keys → New SSH key
2. Paste your public key
3. Save

Update your remote to use SSH:
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/iron-march-network-analysis.git
git push -u origin main
```

## Step 6: Verify Your Push

After pushing, visit your GitHub repository page to verify all files are there:
- Source code in `src/`
- Notebooks in `notebooks/`
- README.md is displayed on the main page
- All documentation files are present

## Step 7: Update Repository Settings (Optional)

On GitHub, you can:
1. Add topics/tags for better discoverability
2. Set up branch protection rules
3. Enable GitHub Pages for documentation
4. Configure GitHub Actions for CI/CD

## Common Issues and Solutions

### Issue: "Support for password authentication was removed"
**Solution**: Use a Personal Access Token or SSH key instead of password

### Issue: "Remote origin already exists"
**Solution**: Remove and re-add the remote:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/repository-name.git
```

### Issue: "Failed to push some refs"
**Solution**: Pull first if there are changes on GitHub:
```bash
git pull origin main --rebase
git push -u origin main
```

## Updating Your Repository

For future changes:

```bash
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Best Practices

1. **Commit often**: Make small, logical commits
2. **Write clear commit messages**: Explain what and why
3. **Use branches**: Create feature branches for new work
4. **Pull before push**: Keep your local repo updated
5. **Don't commit sensitive data**: Use .gitignore properly

## Next Steps

After pushing to GitHub:

1. Update the repository URL in `README.md`
2. Update the repository URL in `setup.py`
3. Add a project description and topics on GitHub
4. Consider adding GitHub Actions for automated testing
5. Share the repository link with collaborators

---

Need help? Open an issue on GitHub or refer to [GitHub's documentation](https://docs.github.com/).
