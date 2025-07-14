# Deploying to PythonAnywhere 🚀

## Step-by-step Guide

### 1. Project Preparation

1. Upload all project files to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/kittybot.git
   git push -u origin main
   ```

### 2. PythonAnywhere Setup

1. **Register on PythonAnywhere** (https://www.pythonanywhere.com/)
2. **Log in** and go to the "Web" section

### 3. Create a Web App

1. **Click "Add a new web app"**
2. **Select "Flask"** as the framework
3. **Choose Python 3.9** (or newer)
4. **Set the project path**: `/home/yourusername/kittybot`

### 4. Upload the Code

1. **Open a Bash console** on PythonAnywhere
2. **Clone the repository**:
   ```bash
   cd /home/yourusername
   git clone https://github.com/yourusername/kittybot.git
   cd kittybot
   ```

### 5. Install Dependencies

1. **Create a virtual environment**:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 6. Set Environment Variables

1. **Create a `.env` file**:
   ```bash
   echo "TOKEN=8080191792:AAGsMYDNl4qkCA6DrV--kxap-DKYFS4Ndic" > .env
   echo "PYTHONANYWHERE_SITE=yourusername.pythonanywhere.com" >> .env
   ```

### 7. Configure the WSGI File

1. **Open the WSGI file** in the "Web" → "Code" → "WSGI configuration file" section
2. **Replace its contents** with:

```python
import sys
import os

# Add project path
path = '/home/yourusername/kittybot'
if path not in sys.path:
    sys.path.append(path)

# Activate virtual environment
activate_this = '/home/yourusername/kittybot/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import the app
from app import app as application
```

### 8. Web App Settings

1. **In the "Web" → "Code" section**:
   - **Source code**: `/home/yourusername/kittybot`
   - **Working directory**: `/home/yourusername/kittybot`
   - **WSGI configuration file**: leave as is

2. **In the "Web" → "Files" section**:
   - Make sure all files are uploaded

### 9. Set the Webhook

1. **Go to your site**: `https://yourusername.pythonanywhere.com/set_webhook`
2. **You should see a message**: "Webhook set: https://yourusername.pythonanywhere.com/webhook"

### 10. Restart the App

1. **Click "Reload"** in the "Web" section
2. **Check the logs** in "Web" → "Log files" → "Error log"

## Testing the Bot

1. **Open the site**: `https://yourusername.pythonanywhere.com`
2. **You should see a page** with information about the bot
3. **Find the bot in Telegram**: `@CatSuperpositionBot`
4. **Send the command** `/start`

## Troubleshooting

### "Module not found" Error
- Make sure the virtual environment is activated in the WSGI file
- Check that all dependencies are installed

### "Token not found" Error
- Check the `.env` file in the project root
- Make sure the token is correct

### Bot not responding
- Check the webhook: `https://yourusername.pythonanywhere.com/set_webhook`
- Check the error logs in the "Web" section

### 500 Error
- Check the logs in "Web" → "Log files"
- Make sure all imports are correct

## Useful Commands

```bash
# Check app status
curl https://yourusername.pythonanywhere.com

# Set webhook
curl https://yourusername.pythonanywhere.com/set_webhook

# Remove webhook
curl https://yourusername.pythonanywhere.com/remove_webhook

# View logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Monitoring

- **Error logs**: Web → Log files → Error log
- **Access logs**: Web → Log files → Access log
- **App status**: Web → Status

## Updating the Bot

1. **Push changes to GitHub**
2. **On PythonAnywhere**:
   ```bash
   cd /home/yourusername/kittybot
   git pull
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Restart the app** (Reload)

## Important Notes

- **Free accounts** have CPU time limits
- **The bot will only work when there are active requests**
- **For persistent operation**, consider paid plans
- **Regularly check the logs** for errors 