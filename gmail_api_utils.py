import datetime


def get_labels(service):
    existing_labels_response = service.users().labels().list(userId='me').execute()
    existing_labels = existing_labels_response['labels']
    existing_label_names = [label['name'] for label in existing_labels]
    return existing_labels, existing_label_names


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
