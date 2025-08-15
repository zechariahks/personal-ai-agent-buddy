#!/usr/bin/env python3
"""
Basic Intelligent Agent Implementation using Strands Agents SDK
Modern, modular framework for building intelligent agents
"""

import os
import re
from strands_agents import SmartAgent, create_agent
from agent_capabilities import (
    WeatherCapability, EmailCapability, CalendarCapability,
    GoogleCalendarCapability, XCapability
)

class PersonalAIAgent(SmartAgent):
    """Personal AI Agent using Strands Agents SDK"""
    
    def __init__(self, name="Buddy"):
        super().__init__(
            name=name,
            description="Personal AI assistant that can help with weather, emails, calendar, and more"
        )
        
        # Initialize and add capabilities
        self._setup_capabilities()
        
        print(f"🤖 Hello! I'm {self.name}, your intelligent AI assistant built with Strands Agents SDK.")
        print("I can help with weather, emails, calendar events, X integration, and answer questions!")
        
        # Check service status
        self._check_services()
    
    def _setup_capabilities(self):
        """Setup all agent capabilities"""
        # Core capabilities
        self.add_capability(WeatherCapability())
        self.add_capability(EmailCapability())
        self.add_capability(CalendarCapability())
        self.add_capability(GoogleCalendarCapability())
        self.add_capability(XCapability())
        
        print(f"✅ Loaded {len(self.capabilities)} capabilities")
    
    def _check_services(self):
        """Check which external services are properly configured"""
        services_status = {
            "AI (OpenAI)": os.getenv("OPENAI_API_KEY") is not None,
            "Weather API": os.getenv("WEATHER_API_KEY") is not None,
            "Gmail": os.getenv("GMAIL_EMAIL") is not None and os.getenv("GMAIL_APP_PASSWORD") is not None,
            "Google Calendar": os.path.exists("credentials.json") and os.path.exists("token.pickle"),
            "X (Twitter)": all([
                os.getenv("X_BEARER_TOKEN"),
                os.getenv("X_API_KEY"),
                os.getenv("X_API_SECRET"),
                os.getenv("X_ACCESS_TOKEN"),
                os.getenv("X_ACCESS_TOKEN_SECRET")
            ])
        }
        
        print("\n🔧 Service Status:")
        for service, available in services_status.items():
            status = "✅ Ready" if available else "❌ Not configured"
            print(f"   {service}: {status}")
        print()
    
    def process_message(self, message):
        """Process incoming messages and route to appropriate capabilities"""
        content = message.content.lower()
        
        # Route to appropriate capability based on message content
        if any(word in content for word in ["weather", "temperature", "rain", "sunny", "cloudy"]):
            return self._handle_weather_request(message.content)
        elif any(word in content for word in ["email", "send", "mail"]):
            return self._handle_email_request(message.content)
        elif any(word in content for word in ["calendar", "event", "schedule", "meeting", "appointment"]):
            return self._handle_calendar_request(message.content)
        elif any(word in content for word in ["reminder", "remind", "remember"]):
            return self._handle_reminder_request(message.content)
        elif any(word in content for word in ["x", "twitter", "tweet", "trends", "post"]):
            return self._handle_x_request(message.content)
        else:
            # Use AI thinking for general queries
            return self.think(message.content)
    
    def _handle_weather_request(self, request: str) -> str:
        """Handle weather-related requests"""
        # Extract city from request
        city = self._extract_city(request)
        
        result = self.execute_capability("weather", {"city": city})
        
        if result.success:
            return result.message
        else:
            return f"❌ {result.message}"
    
    def _handle_email_request(self, request: str) -> str:
        """Handle email-related requests"""
        # For demo purposes, we'll use a simple email format
        # In a real implementation, you'd parse the request more thoroughly
        
        result = self.execute_capability("email", {
            "to": "example@example.com",
            "subject": "Message from AI Agent",
            "body": "This is a test email from your AI agent."
        })
        
        if result.success:
            return result.message
        else:
            return f"❌ {result.message}"
    
    def _handle_calendar_request(self, request: str) -> str:
        """Handle calendar-related requests"""
        if "list" in request.lower() or "show" in request.lower():
            # Try Google Calendar first, fallback to basic calendar
            google_result = self.execute_capability("google_calendar", {"action": "list"})
            if google_result.success:
                return google_result.message
            else:
                basic_result = self.execute_capability("calendar", {"action": "list"})
                return basic_result.message
        
        elif "create" in request.lower() or "schedule" in request.lower():
            # Extract event details (simplified)
            title = self._extract_event_title(request)
            
            # Try Google Calendar first
            google_result = self.execute_capability("google_calendar", {
                "action": "create",
                "title": title
            })
            
            if google_result.success:
                return google_result.message
            else:
                # Fallback to basic calendar
                basic_result = self.execute_capability("calendar", {
                    "action": "create",
                    "title": title
                })
                return basic_result.message
        
        else:
            return "I can help you list events or create new ones. Try 'list my events' or 'schedule a meeting'."
    
    def _handle_reminder_request(self, request: str) -> str:
        """Handle reminder requests"""
        # Extract reminder text
        reminder_text = self._extract_reminder_text(request)
        
        result = self.execute_capability("calendar", {
            "action": "reminder",
            "text": reminder_text,
            "when": "later"
        })
        
        return result.message
    
    def _handle_x_request(self, request: str) -> str:
        """Handle X (Twitter) related requests"""
        if "trends" in request.lower():
            result = self.execute_capability("x_integration", {"action": "trends"})
            return result.message
        
        elif "post" in request.lower():
            if "bible" in request.lower() or "verse" in request.lower():
                result = self.execute_capability("x_integration", {"action": "post_bible_verse"})
            else:
                # Extract post content
                post_text = self._extract_post_text(request)
                result = self.execute_capability("x_integration", {
                    "action": "post",
                    "text": post_text
                })
            return result.message
        
        else:
            return "I can help you get X trends or post tweets. Try 'X trends' or 'post to X: your message'."
    
    def _extract_city(self, text: str) -> str:
        """Extract city name from text"""
        # Simple city extraction - in a real implementation, use NLP
        words = text.split()
        
        # Look for "in [city]" pattern
        for i, word in enumerate(words):
            if word.lower() == "in" and i + 1 < len(words):
                return words[i + 1].title()
        
        # Default city
        return os.getenv("DEFAULT_CITY", "New York")
    
    def _extract_event_title(self, text: str) -> str:
        """Extract event title from text"""
        # Simple extraction - look for text after "schedule" or "create"
        text = text.lower()
        
        for trigger in ["schedule", "create", "add"]:
            if trigger in text:
                parts = text.split(trigger, 1)
                if len(parts) > 1:
                    return parts[1].strip().title()
        
        return "New Event"
    
    def _extract_reminder_text(self, text: str) -> str:
        """Extract reminder text"""
        # Look for text after "remind me to" or similar patterns
        patterns = [
            r"remind me to (.+)",
            r"reminder to (.+)",
            r"remember to (.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip()
        
        return "General reminder"
    
    def _extract_post_text(self, text: str) -> str:
        """Extract post text from request"""
        # Look for text after "post:" or similar
        patterns = [
            r"post to x[:\s]+(.+)",
            r"tweet[:\s]+(.+)",
            r"post[:\s]+(.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip()
        
        return "Hello from AI Agent!"
    
    def chat(self):
        """Interactive chat interface"""
        print("\n💬 Chat with me! (Type 'quit' to exit)")
        print("Try asking about weather, scheduling events, sending emails, or X trends!")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n👋 Goodbye! Thanks for chatting with {self.name}!")
                    break
                
                if not user_input:
                    continue
                
                # Create a message and process it
                from strands_agents import AgentMessage
                message = AgentMessage(
                    sender="User",
                    recipient=self.name,
                    content=user_input
                )
                
                response = self.process_message(message)
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! Thanks for chatting with {self.name}!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function to run the basic agent"""
    print("🚀 Starting Personal AI Agent with Strands Agents SDK...")
    
    # Create and run the agent
    agent = PersonalAIAgent("Buddy")
    
    # Start interactive chat
    agent.chat()

if __name__ == "__main__":
    main()
