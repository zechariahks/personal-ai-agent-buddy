#!/usr/bin/env python3
"""
Basic Intelligent Agent Implementation
Based on the complete agent building guide
"""

import openai
import requests
import os
import smtplib
import time
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class IntelligentAgent:
    """
    Basic intelligent AI agent with weather, email, calendar, and chat capabilities
    """
    
    def __init__(self, name="Buddy"):
        """Initialize the agent with basic configuration"""
        self.name = name
        self.memory = {}  # Store reminders, events, etc.
        self.services_status = {}  # Track which services are working
        
        print(f"🤖 Hello! I'm {self.name}, your intelligent AI assistant.")
        print("I can help with weather, emails, calendar events, and answer questions!")
        
        # Check which services are available
        self._check_services()
    
    def _check_services(self):
        """Check which external services are properly configured"""
        self.services_status = {
            "AI": os.getenv("OPENAI_API_KEY") is not None,
            "Weather": os.getenv("WEATHER_API_KEY") is not None,
            "Email": os.getenv("GMAIL_EMAIL") is not None and os.getenv("GMAIL_APP_PASSWORD") is not None
        }
        
        print("\n🔧 Service Status:")
        for service, available in self.services_status.items():
            status = "✅ Ready" if available else "❌ Not configured"
            print(f"   {service}: {status}")
        print()
    
    def think(self, user_request):
        """Use AI to understand and respond to requests"""
        if not self.services_status.get("AI", False):
            return "❌ AI service not configured. Please add OPENAI_API_KEY to your .env file."
        
        try:
            print(f"🤔 Thinking about: {user_request}")
            
            # Create OpenAI client
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a helpful personal assistant. Provide clear, 
                        friendly responses. If asked about weather, emails, or calendar events, 
                        suggest using the specific commands available."""
                    },
                    {
                        "role": "user", 
                        "content": user_request
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ AI thinking error: {str(e)}"
    
    def check_weather_basic(self, city):
        """Basic weather function with simulated data for testing"""
        try:
            weather_info = {
                "city": city.title(),
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "45%",
                "wind": "Light breeze"
            }
            
            return f"""
🌤️  Weather in {weather_info['city']}:
• Temperature: {weather_info['temperature']}
• Condition: {weather_info['condition']}
• Humidity: {weather_info['humidity']}
• Wind: {weather_info['wind']}
            """.strip()
            
        except Exception as e:
            return f"❌ Weather error: {str(e)}"
    
    def check_weather_real(self, city):
        """Get real weather data from OpenWeatherMap API"""
        if not self.services_status.get("Weather", False):
            return "❌ Weather service not configured. Please add WEATHER_API_KEY to .env file."
        
        try:
            api_key = os.getenv("WEATHER_API_KEY")
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}
            
            print(f"🌤️  Getting real weather for {city}...")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"]
                wind_speed = data["wind"]["speed"]
                
                weather_report = f"""
🌤️  Real Weather in {city.title()}:
• Temperature: {temp}°C (feels like {feels_like}°C)
• Condition: {description.title()}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s

{self._get_weather_advice(temp, description)}
                """.strip()
                
                return weather_report
                
            elif response.status_code == 404:
                return f"❌ Sorry, I couldn't find weather data for '{city}'. Please check the city name."
            else:
                return f"❌ Weather service error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "❌ Weather service is taking too long to respond. Please try again."
        except requests.exceptions.RequestException as e:
            return f"❌ Network error: Could not connect to weather service. {str(e)}"
        except Exception as e:
            return f"❌ Unexpected weather error: {str(e)}"
    
    def _get_weather_advice(self, temp, description):
        """Provide helpful advice based on weather conditions"""
        advice = ""
        
        if temp < 0:
            advice = "🧥 It's freezing! Bundle up and stay warm."
        elif temp < 10:
            advice = "🧥 Pretty cold - you'll want a warm jacket."
        elif temp > 30:
            advice = "☀️ It's hot! Stay hydrated and seek shade."
        
        if "rain" in description.lower():
            advice += " ☔ Don't forget an umbrella!"
        elif "snow" in description.lower():
            advice += " ❄️ Watch out for slippery conditions!"
        
        return advice
    
    def create_reminder_basic(self, message, recipient="yourself"):
        """Create and store reminders in memory"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            reminder = {
                "message": message,
                "recipient": recipient,
                "created": timestamp,
                "id": f"reminder_{len(self.memory.get('reminders', []))}"
            }
            
            if "reminders" not in self.memory:
                self.memory["reminders"] = []
            self.memory["reminders"].append(reminder)
            
            return f"📝 Reminder created: '{message}' for {recipient}"
            
        except Exception as e:
            return f"❌ Reminder error: {str(e)}"
    
    def list_reminders(self):
        """Show all stored reminders"""
        if "reminders" not in self.memory or not self.memory["reminders"]:
            return "📝 No reminders found."
        
        reminder_list = "📝 Your reminders:\n"
        for i, reminder in enumerate(self.memory["reminders"], 1):
            reminder_list += f"{i}. {reminder['message']} (created: {reminder['created']})\n"
        
        return reminder_list
    
    def create_calendar_event_basic(self, title, date, time, description=""):
        """Create and store calendar events in memory"""
        try:
            event = {
                "title": title,
                "date": date,
                "time": time,
                "description": description,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "id": f"event_{len(self.memory.get('events', []))}"
            }
            
            if "events" not in self.memory:
                self.memory["events"] = []
            self.memory["events"].append(event)
            
            return f"📅 Calendar event created: '{title}' on {date} at {time}"
            
        except Exception as e:
            return f"❌ Calendar error: {str(e)}"
    
    def list_events(self):
        """Show all stored events"""
        if "events" not in self.memory or not self.memory["events"]:
            return "📅 No events scheduled."
        
        event_list = "📅 Your upcoming events:\n"
        for event in self.memory["events"]:
            event_list += f"• {event['title']} - {event['date']} at {event['time']}\n"
            if event['description']:
                event_list += f"  Description: {event['description']}\n"
        
        return event_list
    
    def send_email_real(self, to_email, subject, message):
        """Send real emails using Gmail SMTP"""
        if not self.services_status.get("Email", False):
            return "❌ Email service not configured. Please add Gmail credentials to .env file."
        
        try:
            gmail_email = os.getenv("GMAIL_EMAIL")
            gmail_password = os.getenv("GMAIL_APP_PASSWORD")
            
            msg = MIMEMultipart()
            msg['From'] = gmail_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            body = f"""
Hello!

Your AI assistant ({self.name}) sent you this message:

{message}

---
Sent by your Personal AI Assistant
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            msg.attach(MIMEText(body, 'plain'))
            
            print(f"📧 Sending email to {to_email}...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_email, gmail_password)
            
            text = msg.as_string()
            server.sendmail(gmail_email, to_email, text)
            server.quit()
            
            self._store_sent_email(to_email, subject, message)
            
            return f"✅ Email sent successfully to {to_email}!"
            
        except smtplib.SMTPAuthenticationError:
            return "❌ Email authentication failed. Check your Gmail credentials and app password."
        except smtplib.SMTPException as e:
            return f"❌ Email sending failed: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected email error: {str(e)}"
    
    def _store_sent_email(self, to_email, subject, message):
        """Store sent email information in memory"""
        email_record = {
            "to": to_email,
            "subject": subject,
            "message": message,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if "sent_emails" not in self.memory:
            self.memory["sent_emails"] = []
        self.memory["sent_emails"].append(email_record)
    
    def show_help(self):
        """Show what the agent can do"""
        help_text = f"""
🤖 Hi! I'm {self.name}, your AI assistant. Here's what I can help you with:

🌤️  **Weather**: 
   • "What's the weather in Paris?"
   • "Check weather for Tokyo"

📝 **Reminders**: 
   • "Remind me to call mom tomorrow"
   • "Create a reminder to buy groceries"
   • "Show my reminders"

📅 **Calendar**: 
   • "Schedule a meeting tomorrow at 2 PM"
   • "Create event: Team lunch on Friday at noon"
   • "Show my events"

📧 **Email**: 
   • "Send email to friend@example.com"
   • (Requires Gmail configuration)

💬 **General Questions**: 
   • Ask me anything! I can help with information, explanations, and advice.

🔧 **System**: 
   • "Check services" - See which features are available
   • "Help" - Show this message

Just tell me what you need in natural language - I'll understand!
        """.strip()
        
        return help_text
    
    def extract_city(self, text):
        """Extract city name from user input"""
        words = text.split()
        
        # Look for common patterns like "in Paris" or "for Tokyo"
        for i, word in enumerate(words):
            if word.lower() in ['in', 'for', 'at'] and i + 1 < len(words):
                return words[i + 1].title().strip("?")
        
        # Look for capitalized words (likely city names)
        for word in words:
            if word.istitle() and len(word) > 2:
                return word
        
        return None
    
    def extract_reminder_message(self, text):
        """Extract the reminder message from user input"""
        message = text.lower()
        for phrase in ['remind me to', 'reminder to', 'remember to', 'remind me', 'create a reminder']:
            message = message.replace(phrase, '')
        
        return message.strip().capitalize()
    
    def extract_event_details(self, text):
        """Extract event details from user input (simplified)"""
        title = "Meeting"  # Default title
        date = "Tomorrow"  # Default date
        time = "10:00 AM"  # Default time
        
        # Look for time patterns
        words = text.split()
        for i, word in enumerate(words):
            if any(time_word in word.lower() for time_word in ['am', 'pm', ':']):
                if i > 0:
                    time = f"{words[i-1]} {word}"
                else:
                    time = word
                break
        
        # Look for date patterns
        for word in words:
            if word.lower() in ['today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                date = word.title()
                break
        
        return title, date, time
    
    def get_service_status(self):
        """Return detailed service status information"""
        status_report = "🔧 Service Status Report:\n\n"
        
        for service, available in self.services_status.items():
            if available:
                status_report += f"✅ {service}: Ready and configured\n"
            else:
                status_report += f"❌ {service}: Not configured\n"
                
                if service == "AI":
                    status_report += "   → Add OPENAI_API_KEY to .env file\n"
                elif service == "Weather":
                    status_report += "   → Add WEATHER_API_KEY to .env file\n"
                elif service == "Email":
                    status_report += "   → Add GMAIL_EMAIL and GMAIL_APP_PASSWORD to .env file\n"
        
        return status_report
    
    def process_request(self, user_request):
        """Main request processing logic"""
        request_lower = user_request.lower()
        
        # Help requests
        if any(word in request_lower for word in ['help', 'what can you do', 'commands']):
            return self.show_help()
        
        # Service status requests
        elif any(word in request_lower for word in ['check services', 'service status', 'status']):
            return self.get_service_status()
        
        # Weather requests
        elif any(word in request_lower for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny']):
            city = self.extract_city(user_request)
            if not city:
                return "🌤️  Which city would you like weather information for?"
            
            # Use real weather if available, otherwise basic version
            if self.services_status.get("Weather", False):
                return self.check_weather_real(city)
            else:
                return self.check_weather_basic(city) + "\n\n💡 Add WEATHER_API_KEY for real weather data!"
        
        # Reminder requests
        elif any(word in request_lower for word in ['remind', 'reminder', 'remember']):
            if 'show' in request_lower or 'list' in request_lower:
                return self.list_reminders()
            else:
                message = self.extract_reminder_message(user_request)
                return self.create_reminder_basic(message)
        
        # Calendar requests
        elif any(word in request_lower for word in ['calendar', 'schedule', 'meeting', 'appointment', 'event']):
            if 'show' in request_lower or 'list' in request_lower:
                return self.list_events()
            else:
                title, date, time = self.extract_event_details(user_request)
                return self.create_calendar_event_basic(title, date, time)
        
        # Email requests
        elif any(word in request_lower for word in ['email', 'send', 'mail']):
            if self.services_status.get("Email", False):
                # Extract email details
                match = re.search(r'to (.+?) with subject (.+?) and message (.+)', user_request, re.IGNORECASE)
                if match:
                    to_email = match.group(1).strip()
                    subject = match.group(2).strip()
                    message = match.group(3).strip()
                    
                    return self.send_email_real(to_email, subject, message)
                else:
                    return "📧 Please provide the email in the format: 'Send email to [email] with subject [subject] and message [message]'."
            else:
                return "📧 Email service not configured. Please add Gmail credentials to .env file."
        
        # General AI questions
        else:
            return self.think(user_request)
    
    def sanitize_input(self, user_input):
        """Clean and validate user input for security"""
        dangerous_chars = ['<', '>', '&', '"', "'", '`']
        cleaned_input = user_input
        
        for char in dangerous_chars:
            cleaned_input = cleaned_input.replace(char, '')
        
        if len(cleaned_input) > 1000:
            cleaned_input = cleaned_input[:1000] + "..."
        
        return cleaned_input.strip()
    
    def is_safe_request(self, user_request):
        """Check if the user request is safe to process"""
        harmful_patterns = [
            'delete', 'remove', 'destroy', 'hack', 'exploit',
            'password', 'secret', 'private', 'confidential'
        ]
        
        request_lower = user_request.lower()
        for pattern in harmful_patterns:
            if pattern in request_lower:
                return False, f"Request contains potentially harmful content: '{pattern}'"
        
        return True, "Request is safe"
    
    def chat(self):
        """Enhanced chat interface"""
        print(f"\n💬 Chat with {self.name} (type 'quit' to exit)")
        print("=" * 50)
        print("Try asking about weather, reminders, emails, or general questions!")
        print("Type 'help' to see all available commands.")
        print("=" * 50)
        
        conversation_count = 0
        
        while True:
            try:
                user_input = input(f"\n[{conversation_count + 1}] You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(f"\n{self.name}: Goodbye! It was great chatting with you! 👋")
                    print(f"We had {conversation_count} conversations. Come back anytime!")
                    break
                
                if not user_input:
                    print(f"{self.name}: I didn't catch that. Could you please say something?")
                    continue
                
                clean_input = self.sanitize_input(user_input)
                
                is_safe, safety_message = self.is_safe_request(clean_input)
                if not is_safe:
                    print(f"{self.name}: ⚠️  {safety_message}")
                    continue
                
                print(f"{self.name}: ", end="", flush=True)
                response = self.process_request(clean_input)
                print(response)
                
                conversation_count += 1
                
                if conversation_count % 5 == 0:
                    print(f"\n💡 Tip: Type 'help' to see everything I can do!")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Interrupted! Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n{self.name}: ❌ Sorry, something went wrong: {str(e)}")
                print("Let's try again!")
    
    def start_agent(self):
        """Start the agent with a welcome message"""
        print("🚀 Starting your Intelligent AI Assistant...")
        print("=" * 60)
        print(f"Agent Name: {self.name}")
        print(f"Status: Ready to help!")
        print("=" * 60)
        
        self._check_services()
        self.chat()


def main():
    """Main function to create and start the intelligent agent"""
    print("🤖 Intelligent AI Agent - Basic Version")
    print("=" * 50)
    
    # Create your agent
    agent = IntelligentAgent("Buddy")
    
    # Start the agent
    agent.start_agent()


if __name__ == "__main__":
    main()
