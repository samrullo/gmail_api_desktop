# How to retrieve messages
Once we authorize ourselves to GMAIL API server, we can start calling APIs.
Here we explain how to get list of messages.

```python
msg_results=service.users().messages().list(userId='me').execute()
```

Above will return a dictionary with keys
 - messages : list of messages
 - nextPageToken : page token to access messages on the next page
 - resultSizeEstimate
 

Each message in ```messages``` has following structure : 
-  id : message id, can be used to retrieve the actual message
- threadId : thread id

## To retrieve message by id
Below is how we can retrieve a single message by id
 ```python
message = service.users().messages().get(userId='me',id='17991b155f25093f').execute()
```

The object message has following structure:
    
- id
- threadId
- labelIds
- snippet
- payload
- sizeEstimate
- historyId
- internalDate

The message ```payload``` :
    
- partId : One message consists of multiple parts. First part usually contains info like sender
- mimeType : MIME stands for Multipurpose Internet Mail extension which is a standard to send non ASCII type emails
- filename
- headers : headers contains info Subject, To, From, Date
- body
- parts
