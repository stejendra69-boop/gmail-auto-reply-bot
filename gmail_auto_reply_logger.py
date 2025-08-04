
from __future__ import print_function
import base64
import os.path
import time
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Gmail and Sheets API scopes
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
SHEETS_SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Load Gmail credentials
creds = Credentials.from_authorized_user_file('token.json', GMAIL_SCOPES)
gmail_service = build('gmail', 'v1', credentials=creds)

# Load Sheets credentials
sheet_creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_credentials.json', SHEETS_SCOPES)
gc = gspread.authorize(sheet_creds)
sheet = gc.open("Gmail Auto-Reply Log").sheet1  # Make sure the sheet and tab exist

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_reply(to_email, subject, body):
    msg = create_message(to_email, subject, body)
    gmail_service.users().messages().send(userId='me', body=msg).execute()

def log_to_sheet(sender, subject, reply_text):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        sheet.append_row([timestamp, sender, subject, reply_text])
        print("✅ Logged to Google Sheet.")
    except Exception as e:
        print(f"❌ Failed to log to sheet: {e}")

def auto_reply_to_emails():
    results = gmail_service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])

    if not messages:
        print("📭 No unread emails found.")
        return

    for message in messages:
        msg = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "(No Subject)")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "(No Sender)")

        subject_l = subject.lower()

        if "interview invite" in subject_l or "interview scheduled" in subject_l:
            reply_body = "Acknowledged your interview invite. Looking forward to it!"
        elif "selected" in subject_l or "congratulations" in subject_l:
            reply_body = "Thank you for selecting me. I'm excited to join the next steps!"
        elif "rejected" in subject_l or "not selected" in subject_l:
            reply_body = "Thank you for the update. I appreciate the opportunity to interview."
        else:
            reply_body = "Thank you for your email. We have received your message and will respond shortly."

        print(f"✉️ From: {sender}")
        print(f"🔎 Subject: {subject}")
        print(f"🟢 Reply: {reply_body}")

        send_reply(sender, "Re: " + subject, reply_body)
        log_to_sheet(sender, subject, reply_body)

        # Mark the email as read to avoid duplicate replies
        gmail_service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    auto_reply_to_emails()
