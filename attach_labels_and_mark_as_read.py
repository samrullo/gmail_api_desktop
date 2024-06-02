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
from gmail_api_utils import get_labels
from utils import get_chunked_list

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "nohbus.veollurma@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = f"{gmail_username}_credentials.json"
token_file = f"{gmail_username}_token.json"
service = get_gmail_service(creds_folder="credentials", creds_file=creds_file, token_file=token_file)

folder = '/Users/samrullo/Documents/learning/programming/gmail_api_experiment'
all_messages_file = 'nohbus.veollurma_unread_gmail_messages_downloaded_on_2021-05-31.csv'
by_sender_domain_file = 'nohbus.veollurma_by_sender_domain.csv'

all_messages_df = pd.read_csv(os.path.join(folder, all_messages_file))
by_sender_domain_df = pd.read_csv(os.path.join(folder, by_sender_domain_file))
labels_sender_domain_df = by_sender_domain_df[by_sender_domain_df['message_id'] >= 10].copy()
logging.info(f"all messaged df : {len(all_messages_df)}")
logging.info(f"by sender domain df : {len(by_sender_domain_df)}")

existing_labels, existing_label_names = get_labels(service)

# let's create labels and filters
for i, row in labels_sender_domain_df.iterrows():
    if row['sender_domain'] not in existing_label_names:
        new_label_data = {'labelListVisibility': 'labelShow', 'messageListVisibility': 'show',
                          'name': row['sender_domain']}
        new_label_response = service.users().labels().create(userId='me', body=new_label_data).execute()
        logging.info(f"finished creating label : {new_label_data['name']}")
        new_filter = {"criteria":
                          {"from": f"*{new_label_data['name']}"},
                      "action":
                          {"addLabelIds": [new_label_response['id']]}
                      }
        service.users().settings().filters().create(userId='me', body=new_filter).execute()
        logging.info(f"finished creating filter to add label {new_label_data['name']}")

existing_labels, existing_label_names = get_labels(service)
sender_domains = by_sender_domain_df['sender_domain'].to_list()
sender_domain_labels = [label for label in existing_labels if label['name'] in sender_domains]
sender_domain_label_names = [label['name'] for label in sender_domain_labels]

# add corresponding labelIds to messages and mark them as read if unread
for label_idx,label in enumerate(sender_domain_labels):
    logging.info(f"{label_idx}/{len(sender_domain_labels)}label processing ")
    label_id = label['id']
    label_name = label['name']
    target_messages_df = all_messages_df[all_messages_df['sender_domain'] == label_name]
    target_message_ids = target_messages_df['message_id'].to_list()
    chunked_target_message_ids = get_chunked_list(target_message_ids, 1000)
    for chunk_idx, message_ids in enumerate(chunked_target_message_ids):
        logging.info(f"{chunk_idx}/{len(chunked_target_message_ids)} chunk messaged_ids processing")
        logging.info(f"about to add label {label_name} to {len(message_ids)} messages")
        batch_modify_body = {"ids": message_ids,
                             "addLabelIds": [label_id],
                             "removeLabelIds": ['UNREAD']}
        res = service.users().messages().batchModify(userId='me', body=batch_modify_body).execute()
        logging.info(
            f"finished adding label {label_name} and removing label UNREAD for {len(message_ids)} messages. returned response : {res}")
