from __future__ import print_function
import os.path
import re
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import pandas as pd
import logging
from core import get_gmail_service

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "nohbus.veollurma@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = f"{gmail_username}_credentials.json"
token_file = f"{gmail_username}_token.json"
service = get_gmail_service(creds_folder="credentials", creds_file=creds_file, token_file=token_file)


counter = 0

nextPageToken = None
max_iter = 10000 / 100
while counter < max_iter:
    if not nextPageToken and counter == 0:
        messages_list_resource = service.users().messages().list(userId='me', q='is:unread').execute()
    elif not nextPageToken:
        break
    else:
        messages_list_resource = service.users().messages().list(userId='me', pageToken=nextPageToken,
                                                                 q='is:unread').execute()
    messages = messages_list_resource['messages']
    message_ids = [message['id'] for message in messages]

    if 'nextPageToken' in messages_list_resource.keys():
        nextPageToken = messages_list_resource['nextPageToken']
    else:
        logging.info(f"nextPageToken key doesn't exist in keys of returned messages resource")
        nextPageToken=None
    logging.info(
        f"{counter}/{max_iter} : retrieved {len(messages)} messages")

    batch_modify_body = {"ids": message_ids,
                         "removeLabelIds": ['UNREAD']}
    res = service.users().messages().batchModify(userId='me', body=batch_modify_body).execute()
    logging.info(
        f"finished removing label UNREAD for {len(message_ids)} messages. returned response : {res}")
    counter += 1
