import pathlib
import logging
import datetime
import base64
import pandas as pd
import google.auth.exceptions
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.settings.basic']


def get_gmail_service(creds_folder: pathlib.Path = pathlib.Path.cwd() / "credentials",
                      creds_file: str = "credentials.json",
                      token_file: str = "token.json"):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds_path = creds_folder / creds_file
    token_path = creds_folder / token_file
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except google.auth.exceptions.RefreshError as e:
                logging.info(f"Faced RefreshError exception : {e}")
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_certain_name_value_from_headers(headers, header_name):
    header_name_list = [header for header in headers if header['name'] == header_name]
    if len(header_name_list) > 0:
        header = header_name_list[0]
        return header['value']
    else:
        return None


from typing import List


def get_info_for_messages(messages: List[dict], service):
    # append tuple ('message_id', 'internal_date', 'from', 'subject', 'snippet', 'labels')
    messages_data_list = []
    for message in messages:
        message_resource = service.users().messages().get(userId='me', id=message['id']).execute()
        internal_date = datetime.datetime.fromtimestamp(int(message_resource['internalDate']) / 1000)
        snippet = message_resource['snippet']
        labels = ",".join(message_resource['labelIds'])
        headers = message_resource['payload']['headers']
        from_address = get_certain_name_value_from_headers(headers, 'From')
        subject = get_certain_name_value_from_headers(headers, 'Subject')
        messages_data_list.append((message['id'], internal_date, from_address, subject, snippet, labels))
    messages_df = pd.DataFrame(messages_data_list)
    messages_df.columns = ['message_id', 'internal_date', 'from', 'subject', 'snippet', 'labels']
    return messages_df


def get_message_attributes(message_resource:dict):
    """
    Get attributes from, subject,received date and snippet
    :param message_resource: message resource dictionary
    :return: dictionary with attribute values
    """
    internal_date = datetime.datetime.fromtimestamp(int(message_resource['internalDate']) / 1000)
    snippet = message_resource['snippet']
    headers = message_resource['payload']['headers']
    from_address = get_certain_name_value_from_headers(headers, 'From')
    subject = get_certain_name_value_from_headers(headers, 'Subject')
    return {"from": from_address, "subject": subject, "date": internal_date, "snippet": snippet}


def get_message_body_from_resource(message_resource: dict, mime_type: str = "text/plain"):
    """
    Get message body from message resource
    :param message_resource: message_resource dictionary
    :param mime_type: can be either text/plain or text/html
    :return:
    """
    payload = message_resource.get('payload', {})
    parts = payload.get('parts', [])

    # Look for the message body in the parts
    message_body = None
    for part in parts:
        if part.get('mimeType') == mime_type:  # Can also be 'text/html' if you prefer HTML format
            # Decode the message body
            data = part['body'].get('data')
            if data:
                message_body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    return message_body


def get_labels(service: googleapiclient.discovery.Resource):
    """
    Get all defined labels
    :param service: gmail API Resource service
    :return: label name to label ids dictionary
    """
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    label_name_to_label_id = {label['name']: label['id'] for label in labels}
    return label_name_to_label_id
