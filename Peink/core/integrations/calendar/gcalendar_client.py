from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def flatmap(items, f):
    return [result for item in items for result in f(item)]


class GCalendarClient:

    def __init__(
            self,
            credentials_file,
            pickle_file,
            users,
            calendars
    ):
        self.users = users
        self.calendars = calendars

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(pickle_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def list_calendars(self):
        return self.service.calendarList().list().execute()

    def get_events(self):
        events = flatmap(
            self.calendars,
            lambda id: self._get_events(id)
        )
        return sorted(events, key=lambda event: event['start'].get('dateTime', event['start'].get('date')))

    def get_my_next_accepted_event(self):
        events = self.get_events()
        events = [event for event in events if not self._is_declined(event)]
        return events[0] if len(events) > 0 else None

    def _get_user_response_status(self, event):
        for attendee in event.get('attendees', []):
            if attendee.get('email') in self.users:
                return attendee.get('responseStatus')
        return None

    def _is_declined(self, event):
        return self._get_user_response_status(event) == 'declined'

    def _get_events(self, calendar_id, limit=10):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
        ).execute()
        return events_result.get('items', [])
