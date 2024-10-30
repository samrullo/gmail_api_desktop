from __future__ import print_function
import pathlib
import logging
from core import get_gmail_service
import json
import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "amrulloev.subhon@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = "credentials.json"
token_file = "tokens.json"
service = get_gmail_service(creds_folder=pathlib.Path.cwd() / "credentials", creds_file=creds_file,
                            token_file=token_file)

labels = service.users().labels().list(userId="me").execute().get("labels", [])
wfolder = pathlib.Path.cwd() / "data"
filename = f"{gmail_username}_labels.json"
with open(wfolder / filename, "w") as fh:
    json.dump(labels, fh)
for label in labels:
    print(f"{label['name']} : {label['id']}")
