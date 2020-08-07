from __future__ import print_function
from datetime import datetime, timedelta, time, date
from bcolors import bcolors
import pickle
import os.path
from task import Task
from setup import setup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

MAX_EVENTS = 100
# Update for your events
COLORS = {
    '#a4bdfc': '',    # Lavender
    '#5484ed': '',    # Blueberry
    '#46d6db': '',    # Peacock
    '#7ae7bf': '',    # Sage
    '#51b749': '',    # Basil
    '#ffb878': '',    # Tangerine
    '#fbd75b': '',    # Banana
    '#ff887c': '',    # Flamingo
    '#dc2127': '',    # Tomato
    '#fa573c': '',    # Mandarine
    '#dbadff': '',    # Grape
    '#e1e1e1': ''     # Graphite
}

def format_time(time):
    try:
        obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        obj = datetime.strptime(time, '%Y-%m-%d')
    
    return obj

def format_timedelta(timedelta):
    hours = timedelta.total_seconds() / 3600
    return("%.2f" % hours)

def main():
    service = setup()

    current_day = datetime.utcnow()
    first_day = (current_day - timedelta(current_day.weekday())).isoformat() + 'Z'

    print(bcolors.OKBLUE + '[+] Pulling this weeks events [+]' + bcolors.ENDC)
    events_result = service.events().list(calendarId='primary', timeMin=first_day,
                                        maxResults=MAX_EVENTS, singleEvents=True,
                                        orderBy='startTime').execute()
    colors = service.colors().get(fields='event').execute()
    events = events_result.get('items', [])
    total = []

    if not events:
        print(bcolors.FAIL + '[!] No upcoming events found [!]' + bcolors.ENDC)
    
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        event_name = event['summary']

        try:
            color = colors['event'][event['colorId']]['background']
        except KeyError:
            # Default color
            color = (service.calendarList().get(calendarId="primary").execute())['backgroundColor']
        
        e = Task(event_name, format_time(start_time), format_time(end_time), color)
        e.date = format_time(start_time)
        e.get_time()
        total.append(e)
    
    for color, task in COLORS.items():
        if len(task) > 1:
            total_time = timedelta(hours=0)
            for t in total:
                if t.color == color:
                    total_time += t.total_time
            
            text = "You plan to spend "
            string_length=len(text)
            string_revised=text.ljust(string_length)
            print(string_revised + format_timedelta(total_time) + "hrs this week on " + task)
    

if __name__ == '__main__':
    main()