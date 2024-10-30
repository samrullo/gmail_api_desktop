from __future__ import print_function
import pathlib
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

if __name__ == '__main__':
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds_folder = pathlib.Path(r"C:\Users\amrul\programming\secret_keys")
    creds_filename = "credentials.json"
    tokens_filename = "tokens.json"
    creds_path = creds_folder / creds_filename
    creds_path_str = str(creds_path)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if (creds_folder / tokens_filename).exists():
        creds = Credentials.from_authorized_user_file(str(creds_folder / tokens_filename), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(creds_folder / creds_filename), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(creds_folder / tokens_filename, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
