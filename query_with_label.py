from __future__ import print_function
import pathlib
import re
import pandas as pd
import logging
from core import get_gmail_service, get_certain_name_value_from_headers, get_info_for_messages
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

counter = 0

messages_df_list = []
nextPageToken = None
no_of_messages_to_fetch = 300
max_iter = no_of_messages_to_fetch / 100

label_name="pycoders.com"
label_id = "Label_82"
while counter < max_iter:
    if not nextPageToken:
        messages_list_resource = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
    else:
        messages_list_resource = service.users().messages().list(userId='me', pageToken=nextPageToken,labelIds=[label_id]).execute()
    messages = messages_list_resource['messages']
    messages_df = get_info_for_messages(messages, service)
    messages_df_list.append(messages_df)
    nextPageToken = messages_list_resource['nextPageToken']
    logging.info(
        f"{counter}/{max_iter} : retrieved {len(messages)} messages, earliest date is {messages_df['internal_date'].min()}")
    counter += 1

all_messages_df = pd.concat(messages_df_list)
all_messages_df.index = range(len(all_messages_df))

folder = pathlib.Path.cwd() / "data"
all_messages_file = f'{gmail_username}_{label_id}_gmail_messages_downloaded_on_{datetime.date.today()}.csv'
all_messages_df.to_csv(folder / all_messages_file)
logging.info(f"saved {len(all_messages_df)} messages to the folder")

