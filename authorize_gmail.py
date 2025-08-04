
from __future__ import print_function
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    if os.path.exists('token.json'):
        print("Token already exists.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    print("token.json generated successfully!")

if __name__ == '__main__':
    main()
