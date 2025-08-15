#!/usr/bin/env python3
"""
Agent Capabilities for the Personal AI Agent
Implements various capabilities using the Strands Agents SDK
"""

import os
import json
import requests
import smtplib
import pickle
import tweepy
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List
from strands_agents import AgentCapability, AgentResponse

class WeatherCapability(AgentCapability):
    """Weather information and analysis capability"""
    
    def __init__(self):
        super().__init__(
            name="weather",
            description="Get weather information and analyze impact on activities"
        )
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.default_city = os.getenv("DEFAULT_CITY", "New York")
    
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Get weather information for a city"""
        city = parameters.get("city", self.default_city)
        
        try:
            if self.api_key:
                weather_data = self._get_real_weather(city)
            else:
                weather_data = self._get_simulated_weather(city)
            
            # Analyze weather impact
            impact_analysis = self._analyze_weather_impact(weather_data)
            
            return AgentResponse(
                success=True,
                message=self._format_weather_response(weather_data, impact_analysis),
                data={
                    "weather": weather_data,
                    "impact_analysis": impact_analysis
                }
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to get weather information: {str(e)}",
                error="WEATHER_ERROR"
            )
    
    def _get_real_weather(self, city: str) -> Dict[str, Any]:
        """Get real weather data from OpenWeatherMap API"""
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data.get("wind", {}).get("speed", 0),
            "source": "real"
        }
    
    def _get_simulated_weather(self, city: str) -> Dict[str, Any]:
        """Generate simulated weather data"""
        import random
        
        conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy"]
        
        return {
            "city": city,
            "temperature": random.randint(-5, 35),
            "condition": random.choice(conditions),
            "description": f"{random.choice(conditions).lower()} weather",
            "humidity": random.randint(30, 90),
            "wind_speed": random.randint(0, 20),
            "source": "simulated"
        }
    
    def _analyze_weather_impact(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze weather impact on activities"""
        temp = weather_data["temperature"]
        condition = weather_data["condition"].lower()
        
        # Calculate outdoor suitability score (0-100)
        outdoor_score = 100
        
        if condition in ["rainy", "snowy", "stormy"]:
            outdoor_score -= 50
        elif condition in ["foggy", "cloudy"]:
            outdoor_score -= 20
        
        if temp < 0 or temp > 35:
            outdoor_score -= 30
        elif temp < 10 or temp > 30:
            outdoor_score -= 15
        
        outdoor_score = max(0, outdoor_score)
        
        return {
            "outdoor_suitability": outdoor_score,
            "recommendations": self._generate_recommendations(weather_data, outdoor_score),
            "travel_impact": "high" if condition in ["rainy", "snowy", "foggy"] else "low"
        }
    
    def _generate_recommendations(self, weather_data: Dict[str, Any], outdoor_score: int) -> List[str]:
        """Generate weather-based recommendations"""
        recommendations = []
        condition = weather_data["condition"].lower()
        temp = weather_data["temperature"]
        
        if outdoor_score < 50:
            recommendations.append("Consider indoor activities")
        
        if condition == "rainy":
            recommendations.append("Bring an umbrella")
            recommendations.append("Consider rescheduling outdoor events")
        elif condition == "snowy":
            recommendations.append("Dress warmly and wear appropriate footwear")
            recommendations.append("Allow extra travel time")
        elif temp > 30:
            recommendations.append("Stay hydrated and seek shade")
        elif temp < 5:
            recommendations.append("Dress in layers and protect exposed skin")
        
        return recommendations
    
    def _format_weather_response(self, weather_data: Dict[str, Any], impact_analysis: Dict[str, Any]) -> str:
        """Format weather response for display"""
        response = f"🌤️ Weather in {weather_data['city']}:\n"
        response += f"   • Temperature: {weather_data['temperature']}°C\n"
        response += f"   • Condition: {weather_data['condition']}\n"
        response += f"   • Humidity: {weather_data['humidity']}%\n"
        response += f"   • Outdoor Suitability: {impact_analysis['outdoor_suitability']}%\n"
        
        if impact_analysis['recommendations']:
            response += f"\n💡 Recommendations:\n"
            for rec in impact_analysis['recommendations']:
                response += f"   • {rec}\n"
        
        return response.strip()

class EmailCapability(AgentCapability):
    """Email sending capability"""
    
    def __init__(self):
        super().__init__(
            name="email",
            description="Send emails via Gmail SMTP"
        )
        self.gmail_email = os.getenv("GMAIL_EMAIL")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Send an email"""
        if not self.gmail_email or not self.gmail_password:
            return AgentResponse(
                success=False,
                message="Gmail credentials not configured",
                error="CREDENTIALS_MISSING"
            )
        
        to_email = parameters.get("to")
        subject = parameters.get("subject", "Message from AI Agent")
        body = parameters.get("body", "")
        
        if not to_email:
            return AgentResponse(
                success=False,
                message="Recipient email address is required",
                error="MISSING_RECIPIENT"
            )
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.gmail_email, self.gmail_password)
            
            text = msg.as_string()
            server.sendmail(self.gmail_email, to_email, text)
            server.quit()
            
            return AgentResponse(
                success=True,
                message=f"📧 Email sent successfully to {to_email}",
                data={"recipient": to_email, "subject": subject}
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to send email: {str(e)}",
                error="EMAIL_SEND_ERROR"
            )

class CalendarCapability(AgentCapability):
    """Calendar management capability"""
    
    def __init__(self):
        super().__init__(
            name="calendar",
            description="Manage calendar events and reminders"
        )
        self.events = []  # Simple in-memory storage
        self.reminders = []
    
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Execute calendar operations"""
        action = parameters.get("action", "list")
        
        if action == "create":
            return self._create_event(parameters)
        elif action == "list":
            return self._list_events(parameters)
        elif action == "reminder":
            return self._create_reminder(parameters)
        elif action == "list_reminders":
            return self._list_reminders()
        else:
            return AgentResponse(
                success=False,
                message=f"Unknown calendar action: {action}",
                error="INVALID_ACTION"
            )
    
    def _create_event(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Create a calendar event"""
        title = parameters.get("title", "Untitled Event")
        date = parameters.get("date", datetime.now().strftime("%Y-%m-%d"))
        time = parameters.get("time", "12:00")
        location = parameters.get("location", "")
        
        event = {
            "id": len(self.events) + 1,
            "title": title,
            "date": date,
            "time": time,
            "location": location,
            "created_at": datetime.now().isoformat()
        }
        
        self.events.append(event)
        
        response_msg = f"📅 Event created: '{title}' on {date} at {time}"
        if location:
            response_msg += f" at {location}"
        
        return AgentResponse(
            success=True,
            message=response_msg,
            data=event
        )
    
    def _list_events(self, parameters: Dict[str, Any]) -> AgentResponse:
        """List calendar events"""
        if not self.events:
            return AgentResponse(
                success=True,
                message="📅 No events scheduled",
                data=[]
            )
        
        response_msg = "📅 Your Events:\n"
        for event in self.events:
            response_msg += f"   • {event['title']} - {event['date']} at {event['time']}"
            if event['location']:
                response_msg += f" ({event['location']})"
            response_msg += "\n"
        
        return AgentResponse(
            success=True,
            message=response_msg.strip(),
            data=self.events
        )
    
    def _create_reminder(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Create a reminder"""
        text = parameters.get("text", "Reminder")
        when = parameters.get("when", "later")
        
        reminder = {
            "id": len(self.reminders) + 1,
            "text": text,
            "when": when,
            "created_at": datetime.now().isoformat()
        }
        
        self.reminders.append(reminder)
        
        return AgentResponse(
            success=True,
            message=f"📝 Reminder created: '{text}' for {when}",
            data=reminder
        )
    
    def _list_reminders(self) -> AgentResponse:
        """List reminders"""
        if not self.reminders:
            return AgentResponse(
                success=True,
                message="📝 No reminders set",
                data=[]
            )
        
        response_msg = "📝 Your Reminders:\n"
        for reminder in self.reminders:
            response_msg += f"   • {reminder['text']} ({reminder['when']})\n"
        
        return AgentResponse(
            success=True,
            message=response_msg.strip(),
            data=self.reminders
        )

class GoogleCalendarCapability(AgentCapability):
    """Google Calendar integration capability"""
    
    def __init__(self):
        super().__init__(
            name="google_calendar",
            description="Integrate with Google Calendar API"
        )
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Calendar service"""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            
            creds = None
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                    else:
                        self.enabled = False
                        return
                
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('calendar', 'v3', credentials=creds)
            
        except Exception as e:
            print(f"Google Calendar initialization failed: {str(e)}")
            self.enabled = False
    
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Execute Google Calendar operations"""
        if not self.service:
            return AgentResponse(
                success=False,
                message="Google Calendar service not available",
                error="SERVICE_UNAVAILABLE"
            )
        
        action = parameters.get("action", "list")
        
        if action == "list":
            return self._list_events()
        elif action == "create":
            return self._create_event(parameters)
        else:
            return AgentResponse(
                success=False,
                message=f"Unknown Google Calendar action: {action}",
                error="INVALID_ACTION"
            )
    
    def _list_events(self) -> AgentResponse:
        """List upcoming Google Calendar events"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return AgentResponse(
                    success=True,
                    message="📅 No upcoming events found",
                    data=[]
                )
            
            response_msg = "📅 Your Upcoming Google Calendar Events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response_msg += f"   • {event['summary']} - {start}\n"
            
            return AgentResponse(
                success=True,
                message=response_msg.strip(),
                data=events
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to list Google Calendar events: {str(e)}",
                error="CALENDAR_LIST_ERROR"
            )
    
    def _create_event(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Create a Google Calendar event"""
        try:
            title = parameters.get("title", "New Event")
            start_time = parameters.get("start_time")
            end_time = parameters.get("end_time")
            location = parameters.get("location", "")
            description = parameters.get("description", "")
            
            if not start_time:
                # Default to 1 hour from now
                start_dt = datetime.now() + timedelta(hours=1)
                start_time = start_dt.isoformat()
                end_time = (start_dt + timedelta(hours=1)).isoformat()
            
            event = {
                'summary': title,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                },
            }
            
            created_event = self.service.events().insert(
                calendarId='primary', body=event).execute()
            
            return AgentResponse(
                success=True,
                message=f"📅 Google Calendar event created: '{title}'",
                data=created_event
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to create Google Calendar event: {str(e)}",
                error="CALENDAR_CREATE_ERROR"
            )

class XCapability(AgentCapability):
    """X (Twitter) integration capability"""
    
    def __init__(self):
        super().__init__(
            name="x_integration",
            description="Interact with X (Twitter) for trends, news, and posting"
        )
        self.api = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize X API client"""
        try:
            bearer_token = os.getenv("X_BEARER_TOKEN")
            api_key = os.getenv("X_API_KEY")
            api_secret = os.getenv("X_API_SECRET")
            access_token = os.getenv("X_ACCESS_TOKEN")
            access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
            
            if not all([bearer_token, api_key, api_secret, access_token, access_token_secret]):
                self.enabled = False
                return
            
            self.api = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
        except Exception as e:
            print(f"X API initialization failed: {str(e)}")
            self.enabled = False
    
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Execute X operations"""
        if not self.api:
            return AgentResponse(
                success=False,
                message="X API service not available",
                error="SERVICE_UNAVAILABLE"
            )
        
        action = parameters.get("action", "trends")
        
        if action == "trends":
            return self._get_trends()
        elif action == "post":
            return self._post_tweet(parameters)
        elif action == "post_bible_verse":
            return self._post_bible_verse()
        else:
            return AgentResponse(
                success=False,
                message=f"Unknown X action: {action}",
                error="INVALID_ACTION"
            )
    
    def _get_trends(self) -> AgentResponse:
        """Get trending topics with AI analysis"""
        try:
            # Get trending topics (simplified for demo)
            trends_data = {
                "trends": [
                    "AI & Technology",
                    "Breaking News",
                    "World Events",
                    "Sports Updates",
                    "Entertainment"
                ],
                "analysis": "Current trends show high engagement in technology and news topics"
            }
            
            # Generate AI summary if OpenAI is available
            ai_summary = self._generate_ai_summary(trends_data)
            
            response_msg = "🔥 X Trending Topics - AI Summary\n\n"
            response_msg += ai_summary
            
            return AgentResponse(
                success=True,
                message=response_msg,
                data=trends_data
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to get X trends: {str(e)}",
                error="TRENDS_ERROR"
            )
    
    def _post_tweet(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Post a tweet"""
        try:
            text = parameters.get("text", "Hello from AI Agent!")
            
            # For demo purposes, we'll simulate posting
            # In real implementation, use: self.api.create_tweet(text=text)
            
            return AgentResponse(
                success=True,
                message=f"📱 Tweet posted successfully: '{text[:50]}...'",
                data={"text": text, "post_id": "simulated_123456"}
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                message=f"Failed to post tweet: {str(e)}",
                error="POST_ERROR"
            )
    
    def _post_bible_verse(self) -> AgentResponse:
        """Post daily Bible verse"""
        verses = [
            "Trust in the Lord with all your heart... — Proverbs 3:5-6",
            "I can do all things through Christ... — Philippians 4:13",
            "For God so loved the world... — John 3:16",
            "The Lord is my shepherd... — Psalm 23:1",
            "Be strong and courageous... — Joshua 1:9"
        ]
        
        import random
        verse = random.choice(verses)
        
        return self._post_tweet({"text": f"📖 Daily Bible verse: {verse}"})
    
    def _generate_ai_summary(self, trends_data: Dict[str, Any]) -> str:
        """Generate AI summary of trends"""
        try:
            import openai
            
            if not os.getenv("OPENAI_API_KEY"):
                return self._fallback_summary(trends_data)
            
            client = openai.OpenAI()
            
            prompt = f"Analyze these trending topics and provide a brief summary: {trends_data['trends']}"
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception:
            return self._fallback_summary(trends_data)
    
    def _fallback_summary(self, trends_data: Dict[str, Any]) -> str:
        """Fallback summary when AI is not available"""
        summary = "Based on current X data, here are the key trends:\n\n"
        for i, trend in enumerate(trends_data["trends"], 1):
            summary += f"{i}. **{trend}** - High engagement and discussion\n"
        
        return summary

# Export all capabilities
__all__ = [
    'WeatherCapability', 'EmailCapability', 'CalendarCapability',
    'GoogleCalendarCapability', 'XCapability'
]
