from __future__ import print_function
from tqdm import tqdm
import pathlib
import logging
import re

from core import get_gmail_service, get_info_for_messages, get_message_attributes, get_message_body_from_resource
from core import get_labels
from datetime_utils import to_yyyymmdd
import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "amrulloev.subhon@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = "credentials.json"
token_file = "tokens.json"
service = get_gmail_service(creds_folder=pathlib.Path.cwd() / "credentials", creds_file=creds_file,
                            token_file=token_file)

label_name_to_label_ids = get_labels(service)
label_name = "pycoders.com"
label_id = label_name_to_label_ids[label_name]

wfolder = pathlib.Path.cwd() / "data" / label_name
wfolder.mkdir(parents=True, exist_ok=True)

counter = 0

messages_df_list = []
nextPageToken = None
no_of_messages_to_fetch = 300
max_iter = no_of_messages_to_fetch / 100
reached_last_page = False

while counter < max_iter and not reached_last_page:
    if not nextPageToken:
        messages_list_resource = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
    else:
        messages_list_resource = service.users().messages().list(userId='me', pageToken=nextPageToken,
                                                                 labelIds=[label_id]).execute()
    messages = messages_list_resource['messages']

    if "nextPageToken" in messages_list_resource:
        nextPageToken = messages_list_resource['nextPageToken']
    else:
        reached_last_page = True

    messages_df = pd.DataFrame(columns=["from", "date", "subject", "snippet"])

    # read body of each message and save them
    for message in tqdm(messages, desc="Download messages"):
        message_resource = service.users().messages().get(userId='me', id=message['id']).execute()
        message_attributes = get_message_attributes(message_resource)
        message_body = get_message_body_from_resource(message_resource)
        message_attributes_str = "\n".join([f"{key.upper()} : {val}" for key, val in message_attributes.items()])
        message_body = f"{message_attributes_str}\n{message_body}"
        subject_str = "_".join([token.lower() for token in re.findall(r"\w+", message_attributes["subject"])])
        filename = f"{message['id']}_{subject_str}_{to_yyyymmdd(message_attributes['date'])}.txt"
        (wfolder / filename).write_text(message_body, encoding="utf-8")
        messages_df.loc[message['id'], "from"] = message_attributes["from"]
        messages_df.loc[message['id'], "date"] = message_attributes["date"]
        messages_df.loc[message['id'], "subject"] = message_attributes["subject"]
        messages_df.loc[message['id'], "snippet"] = message_attributes["snippet"]

    logging.info(
        f"{counter+1}/{max_iter} : retrieved {len(messages)} messages, earliest date is {messages_df['date'].min()}, latest date : {messages_df['date'].max()}")
    messages_df_list.append(messages_df)
    counter += 1

all_messages_df = pd.concat(messages_df_list)
all_messages_df.index = range(len(all_messages_df))

folder = pathlib.Path.cwd() / "data"
all_messages_file = f'{gmail_username}_{label_name}_gmail_messages_downloaded_on_{datetime.date.today()}.csv'
all_messages_df.to_csv(folder / all_messages_file)
logging.info(f"saved {len(all_messages_df)} messages to the folder")
