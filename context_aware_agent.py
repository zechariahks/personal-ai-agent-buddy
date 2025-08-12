#!/usr/bin/env python3
"""
Context-Aware Agent Implementation
Advanced agent with specialist sub-agents for cross-domain reasoning
"""

import os
import requests
import time
from datetime import datetime
from basic_agent import IntelligentAgent

class WeatherAgent:
    """Specialized agent for weather-related tasks and insights"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.name = "WeatherBot"
    
    def analyze_weather_impact(self, city, date=None):
        """Analyze weather and its potential impact on activities"""
        try:
            weather_data = self.get_detailed_weather(city)
            if not weather_data:
                return None
            
            impact_analysis = {
                "weather_data": weather_data,
                "outdoor_suitability": self._assess_outdoor_conditions(weather_data),
                "travel_impact": self._assess_travel_conditions(weather_data),
                "recommendations": self._generate_weather_recommendations(weather_data),
                "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Store in context memory
            self.parent.context_memory["weather_analysis"] = impact_analysis
            
            return impact_analysis
            
        except Exception as e:
            print(f"❌ Weather analysis error: {str(e)}")
            return None
    
    def get_detailed_weather(self, city):
        """Get comprehensive weather data with impact analysis"""
        if not self.parent.services_status.get("Weather", False):
            return None
        
        try:
            api_key = os.getenv("WEATHER_API_KEY")
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                weather_data = {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "visibility": data.get("visibility", 10000) / 1000,
                    "pressure": data["main"]["pressure"],
                    "rain": data.get("rain", {}).get("1h", 0),
                    "clouds": data["clouds"]["all"]
                }
                
                return weather_data
            
        except Exception as e:
            print(f"❌ Weather data error: {str(e)}")
            return None
    
    def _assess_outdoor_conditions(self, weather_data):
        """Assess how suitable conditions are for outdoor activities"""
        score = 100
        issues = []
        
        temp = weather_data["temperature"]
        if temp < 0:
            score -= 40
            issues.append("freezing temperatures")
        elif temp < 5:
            score -= 20
            issues.append("very cold")
        elif temp > 35:
            score -= 30
            issues.append("extremely hot")
        elif temp > 30:
            score -= 15
            issues.append("very hot")
        
        if "rain" in weather_data["description"].lower():
            score -= 35
            issues.append("rain expected")
        if "snow" in weather_data["description"].lower():
            score -= 40
            issues.append("snow expected")
        
        if weather_data["wind_speed"] > 10:
            score -= 20
            issues.append("strong winds")
        
        if weather_data["visibility"] < 5:
            score -= 25
            issues.append("poor visibility")
        
        return {
            "suitability_score": max(0, score),
            "rating": self._get_suitability_rating(max(0, score)),
            "issues": issues,
            "recommendation": self._get_outdoor_recommendation(max(0, score))
        }
    
    def _assess_travel_conditions(self, weather_data):
        """Assess travel conditions and safety"""
        conditions = {
            "driving": "good",
            "walking": "good",
            "public_transport": "good",
            "warnings": []
        }
        
        description = weather_data["description"].lower()
        
        if "rain" in description:
            conditions["driving"] = "caution"
            conditions["walking"] = "poor"
            conditions["warnings"].append("Wet roads and sidewalks")
        
        if "snow" in description or "ice" in description:
            conditions["driving"] = "dangerous"
            conditions["walking"] = "dangerous"
            conditions["warnings"].append("Icy conditions - high risk")
        
        if weather_data["wind_speed"] > 15:
            conditions["walking"] = "difficult"
            conditions["warnings"].append("Strong winds")
        
        if weather_data["visibility"] < 3:
            conditions["driving"] = "dangerous"
            conditions["warnings"].append("Very poor visibility")
        
        return conditions
    
    def _generate_weather_recommendations(self, weather_data):
        """Generate actionable recommendations based on weather"""
        recommendations = []
        
        temp = weather_data["temperature"]
        if temp < 5:
            recommendations.append("Dress warmly with layers")
            recommendations.append("Consider indoor alternatives for outdoor activities")
        elif temp > 30:
            recommendations.append("Stay hydrated and seek shade")
            recommendations.append("Avoid strenuous outdoor activities during peak hours")
        
        if "rain" in weather_data["description"].lower():
            recommendations.append("Bring an umbrella or raincoat")
            recommendations.append("Consider rescheduling outdoor events")
            recommendations.append("Allow extra travel time")
        
        if weather_data["wind_speed"] > 10:
            recommendations.append("Secure loose items if outdoors")
            recommendations.append("Be cautious with umbrellas")
        
        return recommendations
    
    def _get_suitability_rating(self, score):
        """Convert numeric score to rating"""
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        elif score >= 20:
            return "poor"
        else:
            return "unsuitable"
    
    def _get_outdoor_recommendation(self, score):
        """Get recommendation based on score"""
        if score >= 70:
            return "Great conditions for outdoor activities!"
        elif score >= 50:
            return "Decent conditions, but be prepared for some challenges"
        elif score >= 30:
            return "Consider indoor alternatives or postponing outdoor activities"
        else:
            return "Strongly recommend avoiding outdoor activities"


class CalendarAgent:
    """Specialized agent for calendar management and scheduling intelligence"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.name = "CalendarBot"
        
        # Initialize Google Calendar integration
        try:
            from google_calendar_integration import GoogleCalendarManager
            self.calendar_manager = GoogleCalendarManager()
            self.google_calendar_enabled = self.calendar_manager.is_configured()
        except ImportError:
            print("⚠️ Google Calendar dependencies not installed. Run: pip install -r requirements.txt")
            self.calendar_manager = None
            self.google_calendar_enabled = False
        except Exception as e:
            print(f"⚠️ Google Calendar setup error: {str(e)}")
            self.calendar_manager = None
            self.google_calendar_enabled = False
    
    def process_calendar_request(self, user_request):
        """Process general calendar requests from user input"""
        try:
            request_lower = user_request.lower()
            
            # Handle different types of calendar requests
            if any(word in request_lower for word in ['schedule', 'create event', 'add event']):
                return self._handle_schedule_request(user_request)
            elif any(word in request_lower for word in ['remind', 'reminder']):
                return self._handle_reminder_request(user_request)
            elif any(word in request_lower for word in ['list', 'show', 'events', 'calendar']):
                return self._handle_list_request()
            elif any(word in request_lower for word in ['search', 'find']):
                return self._handle_search_request(user_request)
            elif 'status' in request_lower:
                return self._handle_status_request()
            else:
                return """
📅 Calendar Commands Available:
• "Schedule [event] at [time]" - Create new event in Google Calendar
• "Remind me to [task]" - Create reminder
• "List my events" - Show upcoming Google Calendar events
• "Search events [query]" - Find specific events
• "Calendar status" - Check Google Calendar connection

Example: "Schedule team meeting tomorrow at 2 PM"
                """.strip()
                
        except Exception as e:
            return f"❌ Calendar processing error: {str(e)}"
    
    def _handle_schedule_request(self, request):
        """Handle event scheduling requests using Google Calendar"""
        try:
            # Extract event details from request
            event_details = self._parse_schedule_request(request)
            
            if not event_details:
                return "❌ Could not parse event details. Please specify: 'Schedule [event] at [time]'"
            
            # Use Google Calendar if available
            if self.google_calendar_enabled and self.calendar_manager:
                result = self.calendar_manager.create_event(
                    event_details.get('title', 'New Event'),
                    event_details.get('time', 'tomorrow at 9:00 AM'),
                    description=f"Created by AI Assistant from request: {request}"
                )
                return result
            else:
                # Fallback to basic agent's calendar functionality
                if hasattr(self.parent, 'create_event'):
                    result = self.parent.create_event(
                        event_details.get('title', 'New Event'),
                        event_details.get('time', 'tomorrow')
                    )
                    return result + "\n💡 For Google Calendar integration, set up credentials.json"
                else:
                    # Fallback to memory storage
                    if not hasattr(self.parent, 'memory'):
                        self.parent.memory = {}
                    if 'events' not in self.parent.memory:
                        self.parent.memory['events'] = []
                    
                    self.parent.memory['events'].append({
                        'title': event_details.get('title', 'New Event'),
                        'time': event_details.get('time', 'tomorrow'),
                        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    return f"📅 Event scheduled in memory: {event_details.get('title')} at {event_details.get('time')}\n💡 For Google Calendar integration, set up credentials.json"
                
        except Exception as e:
            return f"❌ Error scheduling event: {str(e)}"
    
    def _handle_reminder_request(self, request):
        """Handle reminder creation requests"""
        try:
            # Extract reminder details
            reminder_details = self._parse_reminder_request(request)
            
            if not reminder_details:
                return "❌ Could not parse reminder. Please specify: 'Remind me to [task]'"
            
            # Create as calendar event if Google Calendar is available
            if self.google_calendar_enabled and self.calendar_manager:
                title = f"Reminder: {reminder_details.get('task', 'New Task')}"
                time_str = reminder_details.get('time', 'tomorrow at 9:00 AM')
                
                result = self.calendar_manager.create_event(
                    title,
                    time_str,
                    description=f"Reminder created by AI Assistant: {reminder_details.get('task')}"
                )
                return result
            else:
                # Use parent agent's reminder functionality
                if hasattr(self.parent, 'create_reminder'):
                    result = self.parent.create_reminder(
                        reminder_details.get('task', 'New Task'),
                        reminder_details.get('time', 'later')
                    )
                    return result + "\n💡 For Google Calendar integration, set up credentials.json"
                else:
                    # Fallback to memory storage
                    if not hasattr(self.parent, 'memory'):
                        self.parent.memory = {}
                    if 'reminders' not in self.parent.memory:
                        self.parent.memory['reminders'] = []
                    
                    self.parent.memory['reminders'].append({
                        'task': reminder_details.get('task', 'New Task'),
                        'time': reminder_details.get('time', 'later'),
                        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    return f"📝 Reminder created in memory: {reminder_details.get('task')}\n💡 For Google Calendar integration, set up credentials.json"
                
        except Exception as e:
            return f"❌ Error creating reminder: {str(e)}"
    
    def _handle_list_request(self):
        """Handle requests to list events/reminders"""
        try:
            # Use Google Calendar if available
            if self.google_calendar_enabled and self.calendar_manager:
                return self.calendar_manager.list_upcoming_events(10)
            else:
                # Fallback to memory/basic agent
                events = getattr(self.parent, 'memory', {}).get('events', [])
                reminders = getattr(self.parent, 'memory', {}).get('reminders', [])
                
                response = "📅 Your Calendar (Memory-based):\n\n"
                
                if events:
                    response += "📅 Upcoming Events:\n"
                    for i, event in enumerate(events[-5:], 1):  # Show last 5 events
                        response += f"  {i}. {event.get('title', 'Untitled')} - {event.get('time', 'No time')}\n"
                    response += "\n"
                
                if reminders:
                    response += "📝 Reminders:\n"
                    for i, reminder in enumerate(reminders[-5:], 1):  # Show last 5 reminders
                        response += f"  {i}. {reminder.get('task', 'No task')} - {reminder.get('time', 'No time')}\n"
                    response += "\n"
                
                if not events and not reminders:
                    response += "No events or reminders found.\n"
                    response += "💡 Try: 'Schedule meeting tomorrow' or 'Remind me to call mom'\n"
                
                response += "\n💡 For Google Calendar integration, set up credentials.json"
                return response.strip()
            
        except Exception as e:
            return f"❌ Error listing calendar items: {str(e)}"
    
    def _handle_search_request(self, request):
        """Handle event search requests"""
        try:
            # Extract search query
            query = self._extract_search_query(request)
            if not query:
                return "❌ Please specify what to search for. Example: 'Search events meeting'"
            
            # Use Google Calendar if available
            if self.google_calendar_enabled and self.calendar_manager:
                return self.calendar_manager.search_events(query, 10)
            else:
                return "❌ Event search requires Google Calendar integration. Please set up credentials.json"
                
        except Exception as e:
            return f"❌ Error searching events: {str(e)}"
    
    def _handle_status_request(self):
        """Handle calendar status requests"""
        try:
            if self.google_calendar_enabled and self.calendar_manager:
                return self.calendar_manager.get_calendar_status()
            else:
                return """
📅 Calendar Status: ⚠️ Using memory-based storage

💡 To enable Google Calendar integration:
1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create/select a project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Download credentials.json to this directory
6. Install dependencies: pip install -r requirements.txt
7. Restart the agent

🔧 Current functionality:
• ✅ Memory-based events and reminders
• ❌ Real Google Calendar integration
• ❌ Cross-device synchronization
                """.strip()
                
        except Exception as e:
            return f"❌ Error checking calendar status: {str(e)}"
    
    def _extract_search_query(self, request):
        """Extract search query from request"""
        import re
        
        patterns = [
            r'search events? (.+)',
            r'find events? (.+)',
            r'search (.+)',
            r'find (.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                return match.group(1).strip()
        
        return None
    
    def _parse_schedule_request(self, request):
        """Parse scheduling request to extract event details"""
        import re
        
        # Pattern: "schedule [event] at/on [time]"
        pattern = r'schedule (.+?) (?:at|on) (.+)'
        match = re.search(pattern, request.lower())
        
        if match:
            return {
                'title': match.group(1).strip(),
                'time': match.group(2).strip()
            }
        
        # Fallback pattern: "schedule [event]"
        pattern2 = r'schedule (.+)'
        match2 = re.search(pattern2, request.lower())
        
        if match2:
            return {
                'title': match2.group(1).strip(),
                'time': 'tomorrow'
            }
        
        return None
    
    def _parse_reminder_request(self, request):
        """Parse reminder request to extract task details"""
        import re
        
        # Pattern: "remind me to [task] [time]"
        pattern = r'remind me to (.+?) (?:at|on|in|tomorrow|today|later) (.+)'
        match = re.search(pattern, request.lower())
        
        if match:
            return {
                'task': match.group(1).strip(),
                'time': match.group(2).strip()
            }
        
        # Fallback pattern: "remind me to [task]"
        pattern2 = r'remind me to (.+)'
        match2 = re.search(pattern2, request.lower())
        
        if match2:
            return {
                'task': match2.group(1).strip(),
                'time': 'later'
            }
        
        return None
    
    def analyze_schedule_conflicts(self, weather_analysis=None):
        """Analyze calendar events for potential weather-related conflicts"""
        events = self.parent.memory.get("events", [])
        if not events:
            return {"conflicts": [], "recommendations": []}
        
        conflicts = []
        recommendations = []
        
        if weather_analysis:
            outdoor_suitability = weather_analysis.get("outdoor_suitability", {})
            travel_conditions = weather_analysis.get("travel_impact", {})
            
            for event in events:
                conflict_analysis = self._analyze_event_weather_conflict(
                    event, outdoor_suitability, travel_conditions
                )
                
                if conflict_analysis["has_conflict"]:
                    conflicts.append(conflict_analysis)
                    recommendations.extend(conflict_analysis["recommendations"])
        
        return {
            "conflicts": conflicts,
            "recommendations": recommendations,
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _analyze_event_weather_conflict(self, event, outdoor_suitability, travel_conditions):
        """Analyze a specific event for weather conflicts"""
        conflict_analysis = {
            "event": event,
            "has_conflict": False,
            "conflict_type": [],
            "severity": "low",
            "recommendations": []
        }
        
        # Check if event seems outdoor-related
        outdoor_keywords = ["park", "outdoor", "picnic", "sports", "garden", "beach", "hiking", "walk"]
        event_text = f"{event['title']} {event.get('description', '')}".lower()
        
        is_outdoor_event = any(keyword in event_text for keyword in outdoor_keywords)
        
        if is_outdoor_event and outdoor_suitability["suitability_score"] < 50:
            conflict_analysis["has_conflict"] = True
            conflict_analysis["conflict_type"].append("outdoor_weather_conflict")
            conflict_analysis["severity"] = "high" if outdoor_suitability["suitability_score"] < 30 else "medium"
            conflict_analysis["recommendations"].append(
                f"Consider moving '{event['title']}' indoors or rescheduling due to {', '.join(outdoor_suitability['issues'])}"
            )
        
        # Check travel-related conflicts
        if any(condition in ["dangerous", "poor"] for condition in travel_conditions.values()):
            conflict_analysis["has_conflict"] = True
            conflict_analysis["conflict_type"].append("travel_safety_conflict")
            conflict_analysis["recommendations"].append(
                f"Travel to '{event['title']}' may be hazardous. Consider virtual meeting or rescheduling."
            )
        
        return conflict_analysis

    def check_weather_conflicts(self, weather_info):
        """Check for weather-related calendar conflicts (wrapper for analyze_schedule_conflicts)"""
        try:
            # This method is called by the enhanced agent
            conflict_analysis = self.analyze_schedule_conflicts(weather_info)
            
            if not conflict_analysis["conflicts"]:
                return "✅ No schedule conflicts detected with current weather conditions."
            
            response = f"\n📅 **Schedule Impact Analysis:**\n"
            response += f"Found {len(conflict_analysis['conflicts'])} potential conflicts:\n\n"
            
            for conflict in conflict_analysis["conflicts"]:
                event = conflict["event"]
                response += f"• **{event['title']}** ({event.get('date', 'TBD')} at {event.get('time', 'TBD')})\n"
                response += f"  Severity: {conflict['severity'].title()}\n"
                response += f"  Issues: {', '.join(conflict['conflict_type'])}\n"
                
                for rec in conflict['recommendations']:
                    response += f"  💡 {rec}\n"
                response += "\n"
            
            return response.strip()
            
        except Exception as e:
            return f"❌ Error checking weather conflicts: {str(e)}"


class EmailAgent:
    """Specialized agent for email communication and notifications"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.name = "EmailBot"
    
    def process_email_request(self, user_request, context_memory):
        """Process general email requests from user input"""
        try:
            # Extract email details from user request
            email_details = self._parse_email_request(user_request)
            
            if not email_details:
                return """
📧 To send an email, please specify:
• "Send email to [recipient] about [subject]"
• "Email [recipient]: [message]"
• "Compose email to [recipient] with subject [subject] and message [content]"

Example: "Send email to john@example.com about meeting tomorrow"
                """.strip()
            
            recipient = email_details.get("recipient")
            subject = email_details.get("subject", "Message from AI Assistant")
            content = email_details.get("content", "")
            
            if not recipient:
                return "❌ Please specify a recipient email address"
            
            # Generate email content
            if not content:
                content = f"Hello,\n\n{subject}\n\nBest regards,\nYour AI Assistant"
            
            # Send email
            if hasattr(self.parent, 'services_status') and self.parent.services_status.get("Email", False):
                result = self.parent.send_email_real(recipient, subject, content)
                return result
            else:
                return f"""
📧 Email Preview (Email service not configured):

To: {recipient}
Subject: {subject}

{content}

💡 To actually send emails, configure Gmail credentials:
• Set GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables
• Restart the agent
                """.strip()
                
        except Exception as e:
            return f"❌ Email processing error: {str(e)}"
    
    def _parse_email_request(self, request):
        """Parse email request to extract recipient, subject, and content"""
        import re
        
        request_lower = request.lower()
        
        # Pattern 1: "send email to [email] about [subject]"
        pattern1 = r'send email to ([^\s]+@[^\s]+) about (.+)'
        match1 = re.search(pattern1, request_lower)
        if match1:
            return {
                "recipient": match1.group(1),
                "subject": match1.group(2),
                "content": f"Hello,\n\nRegarding: {match1.group(2)}\n\nBest regards,\nYour AI Assistant"
            }
        
        # Pattern 2: "email [email]: [message]"
        pattern2 = r'email ([^\s]+@[^\s]+):\s*(.+)'
        match2 = re.search(pattern2, request_lower)
        if match2:
            return {
                "recipient": match2.group(1),
                "subject": "Message from AI Assistant",
                "content": match2.group(2)
            }
        
        # Pattern 3: "compose email to [email] with subject [subject] and message [content]"
        pattern3 = r'compose email to ([^\s]+@[^\s]+) with subject (.+?) and message (.+)'
        match3 = re.search(pattern3, request_lower)
        if match3:
            return {
                "recipient": match3.group(1),
                "subject": match3.group(2),
                "content": match3.group(3)
            }
        
        # Pattern 4: Simple "send email" - return None to show help
        if any(phrase in request_lower for phrase in ['send email', 'compose email', 'email']):
            return None
        
        return None
    
    def compose_contextual_email(self, recipient, subject_template, context_data):
        """Compose emails based on contextual information"""
        try:
            email_content = self._generate_contextual_content(subject_template, context_data)
            
            if self.parent.services_status.get("Email", False):
                result = self.parent.send_email_real(
                    recipient, 
                    email_content["subject"], 
                    email_content["body"]
                )
                return result
            else:
                return f"📧 Email preview:\nTo: {recipient}\nSubject: {email_content['subject']}\n\n{email_content['body']}"
                
        except Exception as e:
            return f"❌ Email composition error: {str(e)}"
    
    def _generate_contextual_content(self, template_type, context_data):
        """Generate email content based on context"""
        if template_type == "weather_event_conflict":
            return self._create_weather_conflict_email(context_data)
        elif template_type == "schedule_update":
            return self._create_schedule_update_email(context_data)
        else:
            return self._create_generic_notification_email(context_data)
    
    def _create_weather_conflict_email(self, context_data):
        """Create email about weather-related schedule conflicts"""
        weather_info = context_data.get("weather_analysis", {})
        conflicts = context_data.get("conflicts", [])
        
        subject = "Weather Alert: Schedule Adjustments Recommended"
        
        body = f"""Hello!

Your AI assistant has detected potential weather-related conflicts with your upcoming events.

Weather Update:
• Current conditions: {weather_info.get('weather_data', {}).get('description', 'N/A')}
• Temperature: {weather_info.get('weather_data', {}).get('temperature', 'N/A')}°C
• Outdoor suitability: {weather_info.get('outdoor_suitability', {}).get('rating', 'N/A')}

Affected Events:
"""
        
        for conflict in conflicts:
            event = conflict["event"]
            body += f"""
• {event['title']} ({event.get('date', 'TBD')} at {event.get('time', 'TBD')})
  Issue: {', '.join(conflict['conflict_type'])}
  Recommendation: {', '.join(conflict['recommendations'])}
"""
        
        body += f"""
Please review these recommendations and let me know if you'd like me to help reschedule any events.

Best regards,
Your AI Assistant
"""
        
        return {"subject": subject, "body": body}
    
    def _create_schedule_update_email(self, context_data):
        """Create email about general schedule updates"""
        subject = "Schedule Update from Your AI Assistant"
        body = f"""Hello!

Your AI assistant has some schedule updates for you:

{context_data.get('message', 'Schedule changes detected.')}

Please review and let me know if you need any adjustments.

Best regards,
Your AI Assistant
"""
        return {"subject": subject, "body": body}


class DecisionAgent:
    """Specialized agent for making contextual decisions across domains"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.name = "DecisionBot"
    
    def make_contextual_decision(self, trigger_event, available_context):
        """Make intelligent decisions based on multiple context sources"""
        decision = {
            "trigger": trigger_event,
            "context_used": list(available_context.keys()),
            "decision": None,
            "confidence": 0,
            "actions": [],
            "reasoning": [],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if trigger_event == "weather_check_completed":
            decision = self._decide_on_weather_impact(available_context, decision)
        elif trigger_event == "calendar_conflict_detected":
            decision = self._decide_on_schedule_conflict(available_context, decision)
        
        self.parent.decision_history.append(decision)
        
        return decision
    
    def _decide_on_weather_impact(self, context, decision):
        """Decide what actions to take based on weather analysis"""
        weather_analysis = context.get("weather_analysis", {})
        outdoor_suitability = weather_analysis.get("outdoor_suitability", {})
        
        if outdoor_suitability.get("suitability_score", 100) < 50:
            decision["decision"] = "recommend_schedule_adjustments"
            decision["confidence"] = 85
            decision["reasoning"].append(f"Weather suitability score is {outdoor_suitability.get('suitability_score')}%")
            decision["reasoning"].append(f"Issues identified: {', '.join(outdoor_suitability.get('issues', []))}")
            
            calendar_agent = self.parent.agent_specialists["calendar"]
            conflict_analysis = calendar_agent.analyze_schedule_conflicts(weather_analysis)
            
            if conflict_analysis["conflicts"]:
                decision["actions"].append("analyze_calendar_conflicts")
                decision["actions"].append("compose_notification_email")
                decision["reasoning"].append(f"Found {len(conflict_analysis['conflicts'])} potential schedule conflicts")
                
                self.parent.context_memory["schedule_conflicts"] = conflict_analysis
        else:
            decision["decision"] = "no_action_needed"
            decision["confidence"] = 90
            decision["reasoning"].append("Weather conditions are suitable for planned activities")
        
        return decision
    
    def _decide_on_schedule_conflict(self, context, decision):
        """Decide how to handle schedule conflicts"""
        conflicts = context.get("schedule_conflicts", {}).get("conflicts", [])
        
        if conflicts:
            high_severity_conflicts = [c for c in conflicts if c.get("severity") == "high"]
            
            if high_severity_conflicts:
                decision["decision"] = "immediate_action_required"
                decision["confidence"] = 95
                decision["actions"].extend(["send_urgent_notification", "suggest_rescheduling"])
                decision["reasoning"].append(f"Found {len(high_severity_conflicts)} high-severity conflicts")
            else:
                decision["decision"] = "suggest_review"
                decision["confidence"] = 75
                decision["actions"].append("send_advisory_notification")
                decision["reasoning"].append("Found moderate schedule conflicts requiring review")
        
        return decision

    def make_weather_decision(self, weather_info, calendar_conflicts):
        """Make weather-related decisions (wrapper for enhanced agent compatibility)"""
        try:
            # Format the response for weather decisions
            if not weather_info:
                return "❌ No weather information available for decision making."
            
            outdoor_suitability = weather_info.get("outdoor_suitability", {})
            suitability_score = outdoor_suitability.get("suitability_score", 100)
            
            response = "\n🧠 **AI Decision Analysis:**\n"
            
            if suitability_score < 30:
                response += "🚨 **High Priority**: Weather conditions are unsuitable for outdoor activities.\n"
                response += "💡 **Recommendation**: Strongly consider rescheduling or moving events indoors.\n"
            elif suitability_score < 60:
                response += "⚠️ **Medium Priority**: Weather conditions may impact outdoor activities.\n"
                response += "💡 **Recommendation**: Review outdoor events and prepare contingency plans.\n"
            else:
                response += "✅ **Low Priority**: Weather conditions are generally suitable.\n"
                response += "💡 **Recommendation**: Proceed with planned activities, monitor conditions.\n"
            
            # Add specific recommendations based on weather issues
            issues = outdoor_suitability.get("issues", [])
            if issues:
                response += f"\n🔍 **Specific Issues**: {', '.join(issues)}\n"
            
            recommendations = weather_info.get("recommendations", [])
            if recommendations:
                response += "\n📋 **Weather Recommendations**:\n"
                for rec in recommendations[:3]:  # Limit to top 3
                    response += f"• {rec}\n"
            
            return response.strip()
            
        except Exception as e:
            return f"❌ Error making weather decision: {str(e)}"


class ContextAwareAgent(IntelligentAgent):
    """Enhanced agent that can make contextual decisions across different domains"""
    
    def __init__(self, name="Buddy"):
        super().__init__(name)
        self.context_memory = {}
        self.decision_history = []
        self.agent_specialists = {}
        self.setup_specialist_agents()
    
    def setup_specialist_agents(self):
        """Create specialized sub-agents for different domains"""
        self.agent_specialists = {
            "weather": WeatherAgent(self),
            "calendar": CalendarAgent(self),
            "email": EmailAgent(self),
            "decision": DecisionAgent(self)
        }
        print(f"🤖 Initialized {len(self.agent_specialists)} specialist agents")
    
    def process_request_with_context(self, user_request):
        """Enhanced request processing that considers context across domains"""
        request_lower = user_request.lower()
        
        # Weather requests with contextual analysis
        if any(word in request_lower for word in ['weather', 'temperature', 'forecast']):
            city = self.extract_city(user_request)
            if not city:
                return "🌤️  Which city would you like weather information for?"
            
            # Get weather analysis from specialist agent
            weather_agent = self.agent_specialists["weather"]
            weather_analysis = weather_agent.analyze_weather_impact(city)
            
            if weather_analysis:
                # Make contextual decision
                decision_agent = self.agent_specialists["decision"]
                decision = decision_agent.make_contextual_decision(
                    "weather_check_completed", 
                    {"weather_analysis": weather_analysis}
                )
                
                # Execute recommended actions
                response = self._format_weather_response(weather_analysis)
                
                if "analyze_calendar_conflicts" in decision.get("actions", []):
                    response += "\n\n" + self._handle_schedule_conflicts(weather_analysis)
                
                return response
            else:
                # Fallback to basic weather
                return self.check_weather_basic(city)
        
        # Handle other requests with existing logic
        else:
            return super().process_request(user_request)
    
    def _format_weather_response(self, weather_analysis):
        """Format comprehensive weather response with contextual insights"""
        weather_data = weather_analysis["weather_data"]
        outdoor_suitability = weather_analysis["outdoor_suitability"]
        travel_impact = weather_analysis["travel_impact"]
        recommendations = weather_analysis["recommendations"]
        
        response = f"""
🌤️  Weather Analysis for {weather_data['city']}:

**Current Conditions:**
• Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
• Condition: {weather_data['description'].title()}
• Humidity: {weather_data['humidity']}%
• Wind: {weather_data['wind_speed']} m/s
• Visibility: {weather_data['visibility']} km

**Outdoor Activity Assessment:**
• Suitability: {outdoor_suitability['rating'].title()} ({outdoor_suitability['suitability_score']}%)
• {outdoor_suitability['recommendation']}
"""
        
        if outdoor_suitability['issues']:
            response += f"• Issues: {', '.join(outdoor_suitability['issues'])}\n"
        
        response += f"""
**Travel Conditions:**
• Driving: {travel_impact['driving'].title()}
• Walking: {travel_impact['walking'].title()}
• Public Transport: {travel_impact['public_transport'].title()}
"""
        
        if travel_impact['warnings']:
            response += f"• ⚠️  Warnings: {', '.join(travel_impact['warnings'])}\n"
        
        if recommendations:
            response += f"\n**Recommendations:**\n"
            for rec in recommendations:
                response += f"• {rec}\n"
        
        return response.strip()
    
    def _handle_schedule_conflicts(self, weather_analysis):
        """Handle detected schedule conflicts"""
        calendar_agent = self.agent_specialists["calendar"]
        conflict_analysis = calendar_agent.analyze_schedule_conflicts(weather_analysis)
        
        if not conflict_analysis["conflicts"]:
            return "✅ No schedule conflicts detected with current weather conditions."
        
        response = f"\n📅 **Schedule Impact Analysis:**\n"
        response += f"Found {len(conflict_analysis['conflicts'])} potential conflicts:\n\n"
        
        for conflict in conflict_analysis["conflicts"]:
            event = conflict["event"]
            response += f"• **{event['title']}** ({event.get('date', 'TBD')} at {event.get('time', 'TBD')})\n"
            response += f"  Severity: {conflict['severity'].title()}\n"
            response += f"  Issues: {', '.join(conflict['conflict_type'])}\n"
            
            for rec in conflict['recommendations']:
                response += f"  💡 {rec}\n"
            response += "\n"
        
        response += "Would you like me to:\n"
        response += "• Send email notifications about these conflicts?\n"
        response += "• Suggest specific rescheduling options?\n"
        response += "• Help you find alternative venues?\n"
        
        return response
    
    def demonstrate_agent_communication(self):
        """Demonstrate how agents communicate and make contextual decisions"""
        print("🤖 Demonstrating Agent-to-Agent Communication\n")
        
        # Create some test events first
        self.create_calendar_event_basic("Team Picnic", "Tomorrow", "2:00 PM", "Outdoor team building event in the park")
        self.create_calendar_event_basic("Morning Jog", "Today", "7:00 AM", "Daily exercise routine")
        
        print("1. Weather Agent analyzes conditions...")
        weather_analysis = self.agent_specialists["weather"].analyze_weather_impact("New York")
        
        if weather_analysis:
            print(f"   Weather suitability: {weather_analysis['outdoor_suitability']['rating']}")
            print(f"   Issues found: {weather_analysis['outdoor_suitability']['issues']}")
            
            print("\n2. Decision Agent evaluates the situation...")
            decision = self.agent_specialists["decision"].make_contextual_decision(
                "weather_check_completed",
                {"weather_analysis": weather_analysis}
            )
            
            print(f"   Decision: {decision['decision']}")
            print(f"   Confidence: {decision['confidence']}%")
            print(f"   Recommended actions: {decision['actions']}")
            
            print("\n3. Calendar Agent checks for conflicts...")
            conflicts = self.agent_specialists["calendar"].analyze_schedule_conflicts(weather_analysis)
            
            if conflicts["conflicts"]:
                print(f"   Found {len(conflicts['conflicts'])} schedule conflicts")
                
                print("\n4. Email Agent prepares notifications...")
                email_agent = self.agent_specialists["email"]
                email_preview = email_agent.compose_contextual_email(
                    "user@example.com",
                    "weather_event_conflict",
                    {"weather_analysis": weather_analysis, "conflicts": conflicts["conflicts"]}
                )
                
                print("   Email notification prepared")
                print(f"   Preview: {email_preview[:100]}...")
            else:
                print("   No schedule conflicts detected")
        
        print("\n✅ Agent communication demonstration complete!")
    
    def process_request(self, user_request):
        """Override to use context-aware processing"""
        return self.process_request_with_context(user_request)


def main():
    """Main function to create and start the context-aware agent"""
    print("🤖 Context-Aware AI Agent - Advanced Version")
    print("=" * 50)
    
    # Create context-aware agent
    agent = ContextAwareAgent("Buddy")
    
    # Demonstrate agent communication
    print("\n🔄 Would you like to see a demonstration of agent communication? (y/n)")
    demo_choice = input().lower().strip()
    
    if demo_choice in ['y', 'yes']:
        agent.demonstrate_agent_communication()
        print("\n" + "="*50)
    
    # Start the agent
    agent.start_agent()


if __name__ == "__main__":
    main()
