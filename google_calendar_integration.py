#!/usr/bin/env python3
"""
Google Calendar Integration for AI Agent
Provides real Google Calendar functionality instead of memory-based events
"""

import os
import json
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendarManager:
    """Manages Google Calendar integration for the AI Agent"""
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.service = None
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.pickle'
        self.setup_calendar_service()
    
    def setup_calendar_service(self):
        """Set up Google Calendar API service"""
        try:
            creds = None
            
            # Load existing token
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    print("🔄 Refreshing Google Calendar credentials...")
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        print("❌ Google Calendar credentials.json not found")
                        print("💡 Please download credentials.json from Google Cloud Console")
                        return False
                    
                    print("🔐 Setting up Google Calendar authentication...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('calendar', 'v3', credentials=creds)
            print("✅ Google Calendar service initialized")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup Google Calendar: {str(e)}")
            return False
    
    def is_configured(self):
        """Check if Google Calendar is properly configured"""
        return self.service is not None
    
    def create_event(self, title, start_time, end_time=None, description="", location=""):
        """Create an event in Google Calendar"""
        try:
            if not self.service:
                return "❌ Google Calendar not configured"
            
            # Parse start time
            start_datetime = self._parse_datetime(start_time)
            if not start_datetime:
                return f"❌ Could not parse start time: {start_time}"
            
            # Set end time (default to 1 hour later)
            if end_time:
                end_datetime = self._parse_datetime(end_time)
            else:
                end_datetime = start_datetime + timedelta(hours=1)
            
            # Create event object
            event = {
                'summary': title,
                'location': location,
                'description': f"{description}\n\nCreated by AI Assistant",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'America/New_York',  # Adjust timezone as needed
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 10},       # 10 minutes before
                    ],
                },
            }
            
            # Insert event
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return f"✅ Event created: {title} on {start_datetime.strftime('%Y-%m-%d at %H:%M')}\n📅 Google Calendar link: {event.get('htmlLink')}"
            
        except HttpError as error:
            return f"❌ Google Calendar API error: {error}"
        except Exception as e:
            return f"❌ Error creating event: {str(e)}"
    
    def list_upcoming_events(self, max_results=10):
        """List upcoming events from Google Calendar"""
        try:
            if not self.service:
                return "❌ Google Calendar not configured"
            
            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            
            events_result = self.service.events().list(
                calendarId='primary', 
                timeMin=now,
                maxResults=max_results, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "📅 No upcoming events found in your Google Calendar"
            
            event_list = "📅 Your Upcoming Google Calendar Events:\n\n"
            
            for i, event in enumerate(events, 1):
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                # Parse datetime
                if 'T' in start:
                    event_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    time_str = event_time.strftime('%Y-%m-%d at %H:%M')
                else:
                    time_str = start + " (All day)"
                
                title = event.get('summary', 'No title')
                location = event.get('location', '')
                
                event_list += f"{i}. {title}\n"
                event_list += f"   📅 {time_str}\n"
                if location:
                    event_list += f"   📍 {location}\n"
                event_list += "\n"
            
            return event_list.strip()
            
        except HttpError as error:
            return f"❌ Google Calendar API error: {error}"
        except Exception as e:
            return f"❌ Error listing events: {str(e)}"
    
    def search_events(self, query, max_results=10):
        """Search for events in Google Calendar"""
        try:
            if not self.service:
                return "❌ Google Calendar not configured"
            
            # Search events
            events_result = self.service.events().list(
                calendarId='primary',
                q=query,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return f"📅 No events found matching '{query}'"
            
            event_list = f"📅 Events matching '{query}':\n\n"
            
            for i, event in enumerate(events, 1):
                start = event['start'].get('dateTime', event['start'].get('date'))
                
                if 'T' in start:
                    event_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    time_str = event_time.strftime('%Y-%m-%d at %H:%M')
                else:
                    time_str = start + " (All day)"
                
                title = event.get('summary', 'No title')
                event_list += f"{i}. {title} - {time_str}\n"
            
            return event_list.strip()
            
        except HttpError as error:
            return f"❌ Google Calendar API error: {error}"
        except Exception as e:
            return f"❌ Error searching events: {str(e)}"
    
    def delete_event(self, event_id):
        """Delete an event from Google Calendar"""
        try:
            if not self.service:
                return "❌ Google Calendar not configured"
            
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            return "✅ Event deleted from Google Calendar"
            
        except HttpError as error:
            if error.resp.status == 404:
                return "❌ Event not found"
            return f"❌ Google Calendar API error: {error}"
        except Exception as e:
            return f"❌ Error deleting event: {str(e)}"
    
    def _parse_datetime(self, time_str):
        """Parse various datetime formats"""
        try:
            # Handle common formats
            formats = [
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d %H:%M:%S',
                '%m/%d/%Y %H:%M',
                '%m/%d/%Y %I:%M %p',
                '%Y-%m-%d',
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
            
            # Handle relative times
            now = datetime.now()
            time_lower = time_str.lower()
            
            if 'tomorrow' in time_lower:
                base_date = now + timedelta(days=1)
                if 'at' in time_lower:
                    time_part = time_lower.split('at')[1].strip()
                    try:
                        time_obj = datetime.strptime(time_part, '%H:%M').time()
                        return datetime.combine(base_date.date(), time_obj)
                    except:
                        try:
                            time_obj = datetime.strptime(time_part, '%I:%M %p').time()
                            return datetime.combine(base_date.date(), time_obj)
                        except:
                            pass
                return base_date.replace(hour=9, minute=0, second=0, microsecond=0)
            
            elif 'today' in time_lower:
                if 'at' in time_lower:
                    time_part = time_lower.split('at')[1].strip()
                    try:
                        time_obj = datetime.strptime(time_part, '%H:%M').time()
                        return datetime.combine(now.date(), time_obj)
                    except:
                        try:
                            time_obj = datetime.strptime(time_part, '%I:%M %p').time()
                            return datetime.combine(now.date(), time_obj)
                        except:
                            pass
                return now.replace(hour=9, minute=0, second=0, microsecond=0)
            
            elif 'next week' in time_lower:
                return now + timedelta(weeks=1)
            
            # Try to parse as time only (assume today)
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
                return datetime.combine(now.date(), time_obj)
            except:
                try:
                    time_obj = datetime.strptime(time_str, '%I:%M %p').time()
                    return datetime.combine(now.date(), time_obj)
                except:
                    pass
            
            return None
            
        except Exception as e:
            print(f"Error parsing datetime '{time_str}': {e}")
            return None
    
    def get_calendar_status(self):
        """Get Google Calendar integration status"""
        if not self.service:
            return """
📅 Google Calendar Status: ❌ Not configured

💡 To set up Google Calendar integration:
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create credentials (OAuth 2.0 client ID)
5. Download credentials.json to this directory
6. Run the agent - it will guide you through authentication

📋 Required files:
• credentials.json (from Google Cloud Console)
• token.pickle (generated after first authentication)
            """.strip()
        
        try:
            # Test API access
            calendar_list = self.service.calendarList().list().execute()
            calendars = calendar_list.get('items', [])
            
            status = """
📅 Google Calendar Status: ✅ Connected

📊 Available Calendars:
            """.strip()
            
            for calendar in calendars[:5]:  # Show first 5 calendars
                name = calendar.get('summary', 'Unknown')
                primary = " (Primary)" if calendar.get('primary') else ""
                status += f"\n• {name}{primary}"
            
            return status
            
        except Exception as e:
            return f"📅 Google Calendar Status: ⚠️ Connected but error: {str(e)}"


def main():
    """Test Google Calendar integration"""
    print("📅 Testing Google Calendar Integration")
    print("=" * 50)
    
    calendar_manager = GoogleCalendarManager()
    
    if calendar_manager.is_configured():
        print("✅ Google Calendar configured successfully")
        
        # Test listing events
        print("\n📋 Testing event listing...")
        events = calendar_manager.list_upcoming_events(5)
        print(events)
        
        # Test creating an event
        print("\n📝 Testing event creation...")
        result = calendar_manager.create_event(
            "AI Agent Test Event",
            "tomorrow at 2:00 PM",
            description="This is a test event created by the AI Agent"
        )
        print(result)
        
    else:
        print("❌ Google Calendar not configured")
        print(calendar_manager.get_calendar_status())


if __name__ == "__main__":
    main()
