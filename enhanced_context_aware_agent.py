#!/usr/bin/env python3
"""
Enhanced Context-Aware Agent with X Integration and AI-Powered Summaries
Focuses on X trends, news, and intelligent summaries (LinkedIn removed)
"""

from basic_agent import IntelligentAgent
from datetime import datetime
import os

# Import specialist agents
from context_aware_agent import WeatherAgent, CalendarAgent, EmailAgent, DecisionAgent
from x_agent import XAgent

class SocialMediaAgent:
    """Specialized agent for social media management (X only)"""
    
    def __init__(self, parent_agent):
        self.parent = parent_agent
        self.name = "SocialBot"
        
        # Initialize X agent only
        self.x_agent = XAgent(parent_agent)
    
    def get_x_trends_summary(self):
        """Get AI-powered X trending topics summary"""
        try:
            print("📱 Getting X trending topics with AI analysis...")
            summary = self.x_agent.get_intelligent_trends_summary()
            
            # Store in context memory
            self.parent.context_memory["x_trends"] = {
                "summary": summary,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return summary
            
        except Exception as e:
            return f"❌ X trends summary error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def get_x_news_summary(self):
        """Get AI-powered X news summary"""
        try:
            print("📱 Getting X news with AI analysis...")
            summary = self.x_agent.get_intelligent_news_summary()
            
            # Store in context memory
            self.parent.context_memory["x_news"] = {
                "summary": summary,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return summary
            
        except Exception as e:
            return f"❌ X news summary error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def get_combined_x_summary(self):
        """Get comprehensive X summary with trends and news"""
        try:
            print("📱 Getting comprehensive X summary...")
            summary = self.x_agent.get_combined_x_summary()
            
            # Store in context memory
            self.parent.context_memory["x_combined"] = {
                "summary": summary,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return summary
            
        except Exception as e:
            return f"❌ X combined summary error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def post_x_bible_verse(self):
        """Post daily Bible verse to X"""
        try:
            print("📱 Posting Bible verse to X...")
            result = self.x_agent.post_daily_bible_verse()
            
            # Store in context memory
            if "x_activity" not in self.parent.context_memory:
                self.parent.context_memory["x_activity"] = []
            
            self.parent.context_memory["x_activity"].append({
                "action": "bible_verse_posted",
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return result
            
        except Exception as e:
            return f"❌ X Bible verse posting error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def post_x_message(self, message):
        """Post custom message to X"""
        try:
            print(f"📱 Posting message to X...")
            result = self.x_agent.post_message(message)
            
            # Store in context memory
            if "x_activity" not in self.parent.context_memory:
                self.parent.context_memory["x_activity"] = []
            
            self.parent.context_memory["x_activity"].append({
                "action": "custom_message_posted",
                "message": message[:50] + "..." if len(message) > 50 else message,
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            return result
            
        except Exception as e:
            return f"❌ X message posting error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def get_x_status(self):
        """Get X account status"""
        try:
            return self.x_agent.get_x_status()
        except Exception as e:
            return f"❌ X status error: {str(e)}"
        finally:
            self.x_agent.cleanup()
    
    def cleanup(self):
        """Clean up social media agents"""
        try:
            self.x_agent.cleanup()
            print("✅ Social media agents cleaned up")
        except Exception as e:
            print(f"⚠️ Social media cleanup warning: {str(e)}")


class EnhancedContextAwareAgent(IntelligentAgent):
    """
    Enhanced context-aware agent with X integration and AI-powered summaries
    Removed LinkedIn functionality for better focus on working features
    """
    
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
            "decision": DecisionAgent(self),
            "social": SocialMediaAgent(self)
        }
        print(f"🤖 Initialized {len(self.agent_specialists)} specialist agents")
        print("   • Weather Agent - Weather analysis and impact assessment")
        print("   • Calendar Agent - Schedule management and conflict detection")
        print("   • Email Agent - Contextual email composition")
        print("   • Decision Agent - Cross-domain reasoning and recommendations")
        print("   • Social Media Agent - X trends, news, and posting")
    
    def process_request_enhanced(self, user_request):
        """Enhanced request processing with X integration and AI summaries"""
        request_lower = user_request.lower()
        
        # X requests with AI summaries - only when specifically requested
        if any(phrase in request_lower for phrase in [
            'x trends', 'x trending', 'trending topics', 'x news', 'news summary', 
            'x summary', 'post bible verse', 'daily bible verse', 'post to x', 'x post', 'x status',
            'get summary of news', 'summary of news', 'latest news summary'
        ]):
            social_agent = self.agent_specialists["social"]
            
            if any(phrase in request_lower for phrase in ['x trends', 'x trending', 'trending topics']):
                return social_agent.get_x_trends_summary()
            
            elif any(phrase in request_lower for phrase in ['x news', 'news summary', 'get summary of news', 'summary of news', 'latest news summary']):
                return social_agent.get_x_news_summary()
            
            elif any(phrase in request_lower for phrase in ['x summary', 'complete summary', 'comprehensive summary']):
                return social_agent.get_combined_x_summary()
            
            elif any(phrase in request_lower for phrase in ['post bible verse', 'daily bible verse', 'bible verse']):
                return social_agent.post_x_bible_verse()
            
            elif 'post to x' in request_lower or 'x post' in request_lower:
                # Extract message content
                message = self._extract_x_message(user_request)
                if message:
                    return social_agent.post_x_message(message)
                else:
                    return """
📱 To post to X, please specify the message:
• "Post to X: [your message]"
• "X post: [your content]"

Example: "Post to X: Excited about the latest AI developments!"
                    """.strip()
            
            elif 'x status' in request_lower:
                return social_agent.get_x_status()
            
            else:
                return """
📱 X Commands Available:
• "X trends" or "trending topics" - Get AI-powered trending topics summary
• "X news" or "get summary of news" - Get AI-powered news summary  
• "X summary" - Get comprehensive trends + news summary
• "Post Bible verse" - Post Bible verse to X
• "Post to X: [message]" - Post custom message
• "X status" - Check X account status

💡 All summaries are powered by AI for intelligent analysis!
                """.strip()
        
        # Weather requests (enhanced with context)
        elif any(word in request_lower for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy']):
            weather_agent = self.agent_specialists["weather"]
            calendar_agent = self.agent_specialists["calendar"]
            
            # Extract city from request or use default
            city = self._extract_city_from_request(user_request) or "New York"
            
            # Get weather info
            weather_info = weather_agent.analyze_weather_impact(city)
            
            if weather_info:
                # Check for calendar conflicts
                calendar_conflicts = calendar_agent.check_weather_conflicts(weather_info)
                
                # Get decision recommendations
                decision_agent = self.agent_specialists["decision"]
                recommendations = decision_agent.make_weather_decision(weather_info, calendar_conflicts)
                
                return f"{self._format_weather_response(weather_info)}\n\n{calendar_conflicts}\n\n{recommendations}"
            else:
                return "❌ Unable to get weather information. Please check your weather API configuration."
        
        # Email requests (check before calendar to avoid conflicts)
        elif any(phrase in request_lower for phrase in ['send email', 'email ', 'compose email', 'send message']):
            email_agent = self.agent_specialists["email"]
            return email_agent.process_email_request(user_request, self.context_memory)
        
        # Calendar requests
        elif any(word in request_lower for word in ['calendar', 'schedule', 'meeting', 'appointment', 'event', 'remind']):
            calendar_agent = self.agent_specialists["calendar"]
            return calendar_agent.process_calendar_request(user_request)
        
        # Daily routine summary
        elif any(phrase in request_lower for phrase in ['daily summary', 'daily routine', 'morning briefing']):
            return self._generate_daily_summary()
        
        # Social media summary (X only)
        elif any(phrase in request_lower for phrase in ['social media', 'social summary']):
            return self._generate_social_media_summary()
        
        # Context memory queries
        elif any(word in request_lower for word in ['remember', 'recall', 'context', 'history']):
            return self._query_context_memory(user_request)
        
        # Fall back to basic agent
        else:
            return super().process_request(user_request)
    
    def _extract_city_from_request(self, request):
        """Extract city name from weather request"""
        import re
        
        # Look for patterns like "weather in [city]" or "weather for [city]"
        patterns = [
            r'weather in ([a-zA-Z\s]+)',
            r'weather for ([a-zA-Z\s]+)',
            r'forecast for ([a-zA-Z\s]+)',
            r'temperature in ([a-zA-Z\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _format_weather_response(self, weather_info):
        """Format weather analysis response"""
        if not weather_info or not isinstance(weather_info, dict):
            return "❌ Weather information unavailable"
        
        weather_data = weather_info.get("weather_data", {})
        outdoor_suitability = weather_info.get("outdoor_suitability", {})
        
        response = f"""
🌤️ Weather Analysis for {weather_data.get('city', 'Unknown City')}:
• Temperature: {weather_data.get('temperature', 'Unknown')}°C
• Condition: {weather_data.get('description', 'Unknown').title()}
• Humidity: {weather_data.get('humidity', 'Unknown')}%
• Wind Speed: {weather_data.get('wind_speed', 'Unknown')} m/s
• Outdoor Suitability: {outdoor_suitability.get('rating', 'Unknown')} ({outdoor_suitability.get('suitability_score', 0)}%)
        """.strip()
        
        return response

    def _extract_x_message(self, text):
        """Extract message from X post requests"""
        # Look for patterns like "post to x: message" or "x post: message"
        import re
        
        patterns = [
            r'post to x:\s*(.+)',
            r'x post:\s*(.+)',
            r'post on x:\s*(.+)',
            r'share on x:\s*(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _generate_daily_summary(self):
        """Generate comprehensive daily summary (without automatic X API calls)"""
        try:
            # Get weather for default location (can be configured)
            weather_agent = self.agent_specialists["weather"]
            city = os.getenv("DEFAULT_CITY", "New York")
            weather_info = weather_agent.analyze_weather_impact(city)
            
            # Check if we have recent X summaries in context memory
            recent_x_summary = self.context_memory.get("x_combined", {}).get("summary", "")
            x_timestamp = self.context_memory.get("x_combined", {}).get("timestamp", "")
            
            daily_summary = f"""
🌅 Daily Routine Summary - {datetime.now().strftime('%A, %B %d, %Y')}

🌤️ Weather Update:
{self._format_weather_response(weather_info) if weather_info else "Weather information unavailable"}

---

📱 Social Media Status:
{f"Last X summary: {x_timestamp}" if x_timestamp else "No recent X summaries"}
{recent_x_summary[:200] + "..." if len(recent_x_summary) > 200 else recent_x_summary if recent_x_summary else "💡 Use 'X summary' to get latest trends and news"}

---

💡 Available Commands:
• "X trends" - Get trending topics
• "X news" - Get news summary
• "Post Bible verse" - Share daily verse
• "Weather in [city]" - Check weather

📊 Summary generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """.strip()
            
            return daily_summary
            
        except Exception as e:
            return f"❌ Error generating daily summary: {str(e)}"
    
    def _generate_social_media_summary(self):
        """Generate social media summary (without automatic X API calls)"""
        try:
            # Check if we have recent X summaries in context memory
            recent_x_trends = self.context_memory.get("x_trends", {})
            recent_x_news = self.context_memory.get("x_news", {})
            recent_x_combined = self.context_memory.get("x_combined", {})
            recent_x_activity = self.context_memory.get("x_activity", [])
            
            social_summary = f"""
📱 Social Media Summary:

🔥 Recent X Activity:
• Trends summaries: {len([s for s in [recent_x_trends] if s])} generated
• News summaries: {len([s for s in [recent_x_news] if s])} generated
• Combined summaries: {len([s for s in [recent_x_combined] if s])} generated
• Posts made: {len(recent_x_activity)} activities

📊 Last Activity Timestamps:
• Trends: {recent_x_trends.get('timestamp', 'None')}
• News: {recent_x_news.get('timestamp', 'None')}
• Combined: {recent_x_combined.get('timestamp', 'None')}

💡 Available Commands:
• "X trends" - Get latest trending topics
• "X news" - Get latest news summary
• "X summary" - Get comprehensive analysis
• "Post Bible verse" - Share daily spiritual content

📊 Summary generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """.strip()
            
            return social_summary
            
        except Exception as e:
            return f"❌ Error generating social media summary: {str(e)}"
    
    def _query_context_memory(self, query):
        """Query the context memory for relevant information"""
        try:
            relevant_info = []
            query_lower = query.lower()
            
            # Search through context memory
            for key, value in self.context_memory.items():
                if any(word in key.lower() for word in ['x', 'social', 'weather', 'calendar']):
                    if isinstance(value, dict):
                        relevant_info.append(f"{key}: {value.get('timestamp', 'Unknown time')}")
                    else:
                        relevant_info.append(f"{key}: {str(value)[:100]}...")
            
            if relevant_info:
                return f"""
🧠 Context Memory Query Results:

{chr(10).join(relevant_info)}

💡 This information has been stored from your recent interactions.
                """.strip()
            else:
                return "🧠 No relevant information found in context memory."
                
        except Exception as e:
            return f"❌ Error querying context memory: {str(e)}"
    
    def cleanup(self):
        """Clean up all specialist agents"""
        try:
            for agent_name, agent in self.agent_specialists.items():
                if hasattr(agent, 'cleanup'):
                    agent.cleanup()
            print("✅ Enhanced agent cleaned up")
        except Exception as e:
            print(f"⚠️ Enhanced agent cleanup warning: {str(e)}")
    
    def process_request(self, user_request):
        """Override to use enhanced processing"""
        return self.process_request_enhanced(user_request)


def main():
    """Interactive demo of the enhanced context-aware agent"""
    print("🤖 Enhanced Context-Aware Agent - Interactive Demo")
    print("=" * 60)
    
    agent = EnhancedContextAwareAgent("Buddy")
    
    try:
        print("\n💡 Available Commands:")
        print("• 'X trends' - Get AI-powered trending topics")
        print("• 'get summary of news' - Get AI-powered news summary")
        print("• 'X summary' - Get comprehensive analysis")
        print("• 'post bible verse' - Post Bible verse to X")
        print("• 'post to X: [message]' - Post custom message")
        print("• 'daily summary' - Get daily routine overview")
        print("• 'weather in [city]' - Get weather analysis")
        print("• 'quit' - Exit the demo")
        
        print("\n🎯 Interactive Mode - Enter commands or 'quit' to exit:")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print(f"Buddy: ", end="")
                result = agent.process_request(user_input)
                print(result)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        agent.cleanup()


if __name__ == "__main__":
    main()
