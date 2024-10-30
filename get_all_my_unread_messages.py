from __future__ import print_function
import os.path
import pathlib
import re
from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import pandas as pd
import logging
from core import get_gmail_service
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "amrulloev.subhon@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = "credentials.json"
token_file = "tokens.json"
service = get_gmail_service(creds_folder=pathlib.Path.cwd() / "credentials", creds_file=creds_file,
                            token_file=token_file)

messages_df = pd.DataFrame(columns=['message_id', 'internal_date', 'from', 'subject', 'snippet', 'labels'])


def get_certain_name_value_from_headers(headers, header_name):
    header_name_list = [header for header in headers if header['name'] == header_name]
    if len(header_name_list) > 0:
        header = header_name_list[0]
        return header['value']
    else:
        return None


def get_info_for_messages(messages, service):
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


counter = 0

messages_df_list = []
nextPageToken = None
max_iter = 200 / 100
while counter < max_iter:
    if not nextPageToken:
        messages_list_resource = service.users().messages().list(userId='me', q='is:unread').execute()
    else:
        messages_list_resource = service.users().messages().list(userId='me', pageToken=nextPageToken).execute()
    messages = messages_list_resource['messages']
    messages_df = get_info_for_messages(messages, service)
    messages_df_list.append(messages_df)
    nextPageToken = messages_list_resource['nextPageToken']
    logging.info(
        f"{counter}/{max_iter} : retrieved {len(messages)} messages, earliest date is {messages_df['internal_date'].min()}")
    counter += 1

all_messages_df = pd.concat(messages_df_list)
all_messages_df.index = range(len(all_messages_df))

# retrieve sender email address and sender domain
for i, row in all_messages_df.iterrows():
    if row['from']:
        from_addr_list = re.findall('<.*>', row['from'])
        if len(from_addr_list) > 0:
            from_addr = from_addr_list[0]
            from_addr = from_addr.replace('<', '').replace('>', '')
            from_addr_domain_list = from_addr.split('@')
            if len(from_addr_domain_list) > 0:
                sender_domain = from_addr_domain_list[1]
            else:
                sender_domain = ""
            all_messages_df.loc[i, 'sender_mail_addr'] = from_addr
            all_messages_df.loc[i, 'sender_domain'] = sender_domain
            logging.info(f"{i}/{len(all_messages_df)} finished retrieving mail address")

folder = pathlib.Path.cwd() / "data"
all_messages_file = f'{gmail_username}_unread_gmail_messages_downloaded_on_{datetime.date.today()}.csv'
all_messages_df.to_csv(folder / all_messages_file)
logging.info(f"saved {len(all_messages_df)} messages to the folder")
by_sender_domain_df = all_messages_df.groupby('sender_domain')[['message_id']].count()
by_sender_domain_df.to_csv(folder / f"{gmail_username}_by_sender_domain.csv")
