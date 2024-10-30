import pathlib
import logging
from core import get_gmail_service, get_certain_name_value_from_headers, get_info_for_messages
import base64

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')

gmail_address = "amrulloev.subhon@gmail.com"
gmail_username = gmail_address.split('@')[0]
creds_file = "credentials.json"
token_file = "tokens.json"
service = get_gmail_service(creds_folder=pathlib.Path.cwd() / "credentials", creds_file=creds_file,
                            token_file=token_file)

# A message with subject Django and WebSockets, QR Codes, Ninja, and More
message = {'id': '183a498b6ba0b4ea', 'threadId': '183a498b6ba0b4ea'}

message_resource = service.users().messages().get(userId='me', id=message['id']).execute()
# Retrieve the payload and parts
payload = message_resource.get('payload', {})
parts = payload.get('parts', [])

# Look for the message body in the parts
message_body = None
for part in parts:
    if part.get('mimeType') == 'text/plain':  # Can also be 'text/html' if you prefer HTML format
        # Decode the message body
        data = part['body'].get('data')
        if data:
            message_body = base64.urlsafe_b64decode(data).decode('utf-8')
            break

if message_body:
    print("Message Body:")
    print(message_body)
else:
    print("No text body found.")
