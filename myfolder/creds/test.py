import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]
our_email = "yourgmail@gmail.com"


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret_511858825626-leijpd5hb6bkc3j1unigj5f3s3jk3i4v.apps.googleusercontent.com.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


# get the Gmail API service
service = gmail_authenticate()


def build_message(destination, obj, body):
    message = MIMEText(body)
    message["to"] = destination
    message["from"] = our_email
    message["subject"] = obj
    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, destination, obj, body):
    return (
        service.users()
        .messages()
        .send(userId="me", body=build_message(destination, obj, body))
        .execute()
    )


send_message(
    service,
    "dinesh.hicet@gmail.com",
    "This is a subject",
    "This is the body of the email",
)
