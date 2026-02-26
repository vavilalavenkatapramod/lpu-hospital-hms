# 🚀 LPU Hospital Management System - Deployment Guide

## Quick Deploy to Render.com (Free)

Your website is ready to be deployed permanently on the internet! Follow these steps:

### Step 1: Create GitHub Repository
1. Go to https://github.com and sign in
2. Click "New repository" 
3. Name it "lpu-hospital-hms"
4. Make it Public
5. Click "Create repository"

### Step 2: Push Your Code
Run these commands in your project folder (in Git Bash or PowerShell):

```
bash
# Initialize git if not done
git init

# Add all files (except unwanted ones)
git add .

# Commit your changes
git commit -m "Initial commit - LPU Hospital Management System"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/lpu-hospital-hms.git

# Push to GitHub
git push -u origin main
```

### Step 3: Deploy to Render
1. Go to https://render.com and sign up (use your GitHub account)
2. Click "New +" and select "Web Service"
3. Connect your GitHub and select your repository
4. Fill in these settings:
   - **Name:** lpu-hospital-hms
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn hms.wsgi:application --bind 0.0.0.0:$PORT`
5. Click "Create Web Service"

### Step 4: Set Environment Variables
In Render dashboard, go to "Environment" tab and add:
- `SECRET_KEY` = any random string (generate at https://djecrety.ir)
- `DEBUG` = `False`
- `DATABASE_URL` = will be auto-created by Render (PostgreSQL)

### 🎉 Your website will be live at something like: `https://lpu-hospital-hms.onrender.com`

---

## Alternative: Deploy to Railway.com
1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables
5. Deploy!

---

## Alternative: Deploy to Cyclic.sh (Easiest!)
1. Go to https://app.cyclic.io and sign up with GitHub
2. Click "Connect Repo" and select your repository
3. Click "Connect"
4. Your app will be deployed automatically!

---

## Need Help?
- Website will be live 24/7 on the cloud
- No need to keep your laptop on
- Anyone can access from anywhere in the world
