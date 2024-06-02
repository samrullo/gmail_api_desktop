# Authorization
To be able to use gmail api, we have to authorize ourselves.
The instructions in https://developers.google.com/gmail/api/quickstart/python
were enough to get started.
For a desktop application you will have to download ```credentials.json```

- A Google Cloud Platform project with the API enabled. 
 To create a project and enable an API, refer to <a href="https://developers.google.com/workspace/guides/create-project">Create a project and enable the API</a>
- Authorization credentials for a desktop application. 
To learn how to create credentials for a desktop application, refer to <a href="https://developers.google.com/workspace/guides/create-credentials">Create credentials</a>

Then you'll use it to get the authorization token.
Below code explains how we authorize ourselves to GMAIL API eventually.
It first tries to open an existing ```token.json``` file which contains authorization token as well as refresh token.
If the file doesn't exist yet, then it will use ```credentials.json``` to receive 
authorization token from Google server.

```python
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
```