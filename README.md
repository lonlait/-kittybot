# CatSuperpositionBot 🐱

A Telegram bot for sending random cat images to users.

## Description

CatSuperpositionBot is a simple and cute Telegram bot that sends users random cat images on request. The bot uses The Cat API to fetch images.

## Features

- 🐱 Sends random cat images
- 📱 Convenient keyboard with buttons
- 🔄 Backup API (The Dog API) if the main one is unavailable
- 📝 Logging of all actions
- ❓ Built-in help

## Bot Commands

- `/start` - Start interacting with the bot
- `/newcat` - Get a new cat image
- `/help` - Show help

## Installation and Usage

### Local Development

#### 1. Clone the repository
```bash
git clone <repository-url>
cd kittybot
```

#### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up the token
Create a `.env` file in the root directory of the project:
```
TOKEN=your_bot_token
```

#### 5. Run the bot
```bash
python kittybot.py
```

### Deploy to PythonAnywhere (for persistent operation)

See detailed deployment instructions in [DEPLOY.md](DEPLOY.md).

**Quick guide:**
1. Upload the project to GitHub
2. Create an account on PythonAnywhere
3. Create a Flask web app
4. Clone the repository
5. Install dependencies
6. Set up the webhook
7. Restart the app

**Deployment files:**
- `app.py` - Flask app for webhook
- `run_bot.py` - script for running via cron
- `DEPLOY.md` - detailed instructions

## Project Structure

```
kittybot/
├── kittybot.py          # Main bot file (local development)
├── app.py               # Flask app for PythonAnywhere
├── run_bot.py           # Script for running via cron
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (token)
├── .gitignore           # Git ignore file
├── bot.log              # Bot logs (created automatically)
├── README.md            # This file
└── DEPLOY.md            # Deployment instructions
```

## Technologies

- **Python 3.8+**
- **pyTelegramBotAPI** - library for working with Telegram Bot API
- **requests** - HTTP client for API requests
- **python-dotenv** - loading environment variables
- **logging** - logging system

## APIs

The bot uses the following APIs:
- **The Cat API** (https://api.thecatapi.com/) - main image source
- **The Dog API** (https://api.thedogapi.com/) - backup source

## Logging

The bot logs to the `bot.log` file and outputs logs to the console. Logs include:
- Bot startup information
- Errors when fetching images
- Warnings about API unavailability

## Security

- The bot token is stored in the `.env` file (not committed to Git)
- All dependencies are pinned in `requirements.txt`
- Error handling to prevent bot crashes

## Development

For development, it is recommended to:
1. Use a virtual environment
2. Follow PEP 8 for code style
3. Add logging for debugging
4. Test the bot in a private chat

## License

MIT License
