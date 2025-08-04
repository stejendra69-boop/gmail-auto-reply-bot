# Gmail Auto-Reply Bot

This project automates replies to your Gmail inbox and logs each response to a Google Sheet. Ideal for recruiters, job seekers, and support teams.

---

## ✨ Features

- Automatically replies to unread Gmail messages.
- Smart replies based on email subject (interview invites, selection, rejection, etc.)
- Logs replies to Google Sheets.
- Supports OAuth for Gmail and service account for Sheets.
- Easily customizable for keywords, replies, and more.

---

## 📦 Project Structure

gmail-auto-reply-bot/
├── scripts/
│ └── gmail_auto_reply_logger.py
├── authorize_gmail.py
├── requirements.txt
├── .gitignore
└── README.md


---

## ⚙️ Setup Instructions

### 1. Install dependencies:
pip install -r requirements.txt


2. Google Cloud Setup
Go to Google Cloud Console

Create OAuth 2.0 credentials (download as client_secret.json)
Create a service account with Sheets access (download as sheets_credentials.json)
Place both files in your project root folder.

3. Authorize Gmail Access
python authorize_gmail.py

This will open a browser window for you to authorize your Gmail account and generate token.json.

4. Setup Your Google Sheet
Create a sheet named Gmail Auto-Reply Log
Share it with the service account email from your sheets_credentials.json
Give it Editor access

5. Run the Bot
python scripts/gmail_auto_reply_logger.py

This will:
Scan for unread emails
Send appropriate auto-replies
Log each response to your sheet
Mark emails as read

Customization
You can modify the reply logic in gmail_auto_reply_logger.py to use your own keywords and message templates:
if "interview invite" in subject:
    reply = "Acknowledged..."
elif "selected" in subject:
    reply = "Thank you..."
# etc.

Security Notes
Do NOT upload your credentials (client_secret.json, sheets_credentials.json, token.json) to GitHub or anywhere public. Use .gitignore to keep them private.

Optional Add-ons (Available on Request)
Multi-account support
Cron job / scheduled execution
Advanced NLP-based reply filters
Slack or email notifications for certain types of emails

License
MIT License — Free for personal and commercial use.

Support
If you need help with setup or customization, contact me via Fiverr or GitHub.

---

### 📝 Also Include These in Your Git Project:

**`.gitignore`:**
```gitignore
client_secret.json
sheets_credentials.json
token.json
__pycache__/
*.pyc

requirements.txt:
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
gspread
oauth2client
