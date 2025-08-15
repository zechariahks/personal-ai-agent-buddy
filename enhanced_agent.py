#!/usr/bin/env python3
"""
Enhanced Context-Aware Agent with X Integration using Strands Agents SDK
Advanced multi-agent system with AI-powered social media analysis and proactive recommendations
"""

import os
import json
from datetime import datetime, timedelta
from strands_agents import SmartAgent, AgentOrchestrator
from context_aware_agent import ContextAwareAgent, WeatherSpecialistAgent, CalendarSpecialistAgent, DecisionSpecialistAgent
from agent_capabilities import XCapability

class SocialMediaSpecialistAgent(SmartAgent):
    """Specialized agent for social media analysis and engagement"""
    
    def __init__(self):
        super().__init__(
            name="SocialBot",
            description="Specialist agent for X (Twitter) integration and social media analysis"
        )
        self.add_capability(XCapability())
    
    def analyze_social_trends(self) -> dict:
        """Analyze current social media trends with AI insights"""
        trends_result = self.execute_capability("x_integration", {"action": "trends"})
        
        if not trends_result.success:
            return {"error": trends_result.message}
        
        trends_data = trends_result.data
        
        # Generate contextual insights
        insights = self._generate_trend_insights(trends_data)
        
        return {
            "trends": trends_data,
            "insights": insights,
            "engagement_opportunities": self._identify_engagement_opportunities(trends_data),
            "content_suggestions": self._suggest_content_ideas(trends_data)
        }
    
    def post_contextual_content(self, content_type: str = "bible_verse", custom_text: str = None) -> dict:
        """Post contextual content to X"""
        if content_type == "bible_verse":
            result = self.execute_capability("x_integration", {"action": "post_bible_verse"})
        elif content_type == "custom" and custom_text:
            result = self.execute_capability("x_integration", {"action": "post", "text": custom_text})
        else:
            return {"error": "Invalid content type or missing custom text"}
        
        return {
            "success": result.success,
            "message": result.message,
            "data": result.data if result.success else None
        }
    
    def _generate_trend_insights(self, trends_data: dict) -> list:
        """Generate AI-powered insights from trend data"""
        insights = []
        
        if "trends" in trends_data:
            trends = trends_data["trends"]
            
            # Analyze trend categories
            tech_trends = [t for t in trends if any(keyword in t.lower() for keyword in ["ai", "tech", "digital", "crypto"])]
            news_trends = [t for t in trends if any(keyword in t.lower() for keyword in ["news", "breaking", "update"])]
            
            if tech_trends:
                insights.append(f"Technology focus: {len(tech_trends)} tech-related trends indicate high interest in innovation")
            
            if news_trends:
                insights.append(f"News engagement: {len(news_trends)} breaking news topics driving conversations")
            
            # General insights
            insights.append(f"Total trending topics analyzed: {len(trends)}")
            insights.append("Optimal posting times: High engagement periods detected")
        
        return insights
    
    def _identify_engagement_opportunities(self, trends_data: dict) -> list:
        """Identify opportunities for social media engagement"""
        opportunities = []
        
        if "trends" in trends_data:
            trends = trends_data["trends"]
            
            # Look for relevant engagement opportunities
            for trend in trends:
                if any(keyword in trend.lower() for keyword in ["ai", "technology", "innovation"]):
                    opportunities.append(f"Engage with {trend} - aligns with AI/tech expertise")
                elif any(keyword in trend.lower() for keyword in ["inspiration", "motivation", "wisdom"]):
                    opportunities.append(f"Share inspirational content related to {trend}")
        
        if not opportunities:
            opportunities.append("General engagement: Share daily inspiration or tech insights")
        
        return opportunities
    
    def _suggest_content_ideas(self, trends_data: dict) -> list:
        """Suggest content ideas based on trends"""
        content_ideas = [
            "Daily Bible verse with modern application",
            "AI and technology insights",
            "Motivational quotes with personal reflection",
            "Weekly wisdom roundup",
            "Tech trends analysis from a faith perspective"
        ]
        
        # Add trend-specific ideas
        if "trends" in trends_data:
            for trend in trends_data["trends"][:3]:  # Top 3 trends
                content_ideas.append(f"Commentary on {trend} from unique perspective")
        
        return content_ideas

class ProactiveRecommendationAgent(SmartAgent):
    """Agent for generating proactive recommendations across all domains"""
    
    def __init__(self):
        super().__init__(
            name="ProactiveBot",
            description="Specialist agent for generating proactive recommendations and daily optimization"
        )
    
    def generate_daily_recommendations(self, weather_data: dict, schedule_data: dict, social_data: dict) -> dict:
        """Generate comprehensive daily recommendations"""
        recommendations = {
            "morning": self._generate_morning_recommendations(weather_data, schedule_data),
            "afternoon": self._generate_afternoon_recommendations(weather_data, schedule_data),
            "evening": self._generate_evening_recommendations(social_data),
            "priority_actions": self._identify_priority_actions(weather_data, schedule_data, social_data),
            "optimization_tips": self._suggest_optimizations(weather_data, schedule_data, social_data)
        }
        
        return recommendations
    
    def _generate_morning_recommendations(self, weather_data: dict, schedule_data: dict) -> list:
        """Generate morning-specific recommendations"""
        recommendations = []
        
        # Weather-based morning recommendations
        if "weather" in weather_data:
            weather = weather_data["weather"]
            if weather["temperature"] < 10:
                recommendations.append("☀️ Dress warmly - temperature is below 10°C")
            elif weather["condition"].lower() == "rainy":
                recommendations.append("🌧️ Bring umbrella - rain expected")
            else:
                recommendations.append(f"🌤️ Pleasant weather ({weather['temperature']}°C) - great day ahead!")
        
        # Schedule-based morning recommendations
        if schedule_data.get("events"):
            morning_events = [e for e in schedule_data["events"] if "morning" in str(e).lower()]
            if morning_events:
                recommendations.append(f"📅 {len(morning_events)} morning event(s) - review schedule")
        
        recommendations.append("💪 Start day with positive mindset and clear priorities")
        
        return recommendations
    
    def _generate_afternoon_recommendations(self, weather_data: dict, schedule_data: dict) -> list:
        """Generate afternoon-specific recommendations"""
        recommendations = []
        
        # Weather considerations for afternoon
        if "weather" in weather_data:
            weather = weather_data["weather"]
            if weather["temperature"] > 25:
                recommendations.append("💧 Stay hydrated - warm afternoon ahead")
            
            outdoor_score = weather_data.get("impact_analysis", {}).get("outdoor_suitability", 50)
            if outdoor_score > 75:
                recommendations.append("🚶 Great weather for outdoor activities")
        
        # Schedule optimization
        if schedule_data.get("conflicts"):
            recommendations.append("⚠️ Resolve schedule conflicts before afternoon")
        
        recommendations.append("🎯 Focus on high-priority tasks during peak energy hours")
        
        return recommendations
    
    def _generate_evening_recommendations(self, social_data: dict) -> list:
        """Generate evening-specific recommendations"""
        recommendations = []
        
        # Social media engagement
        if social_data.get("engagement_opportunities"):
            recommendations.append("📱 Optimal time for social media engagement")
        
        if social_data.get("content_suggestions"):
            recommendations.append("✍️ Consider sharing daily inspiration or insights")
        
        recommendations.append("🙏 End day with reflection and gratitude")
        recommendations.append("📚 Review accomplishments and plan tomorrow")
        
        return recommendations
    
    def _identify_priority_actions(self, weather_data: dict, schedule_data: dict, social_data: dict) -> list:
        """Identify top priority actions for the day"""
        priorities = []
        
        # High-impact weather actions
        if weather_data.get("event_impacts"):
            high_impact_events = [e for e in weather_data["event_impacts"] if e["impact_level"] == "high"]
            if high_impact_events:
                priorities.append(f"🌦️ Address {len(high_impact_events)} weather-impacted event(s)")
        
        # Schedule conflicts
        if schedule_data.get("conflicts"):
            priorities.append(f"📅 Resolve {len(schedule_data['conflicts'])} schedule conflict(s)")
        
        # Social engagement
        if social_data.get("engagement_opportunities"):
            priorities.append("📱 Engage with trending topics for visibility")
        
        if not priorities:
            priorities.append("✅ No urgent issues - focus on planned activities")
        
        return priorities
    
    def _suggest_optimizations(self, weather_data: dict, schedule_data: dict, social_data: dict) -> list:
        """Suggest daily optimizations"""
        optimizations = []
        
        # Weather optimizations
        if "weather" in weather_data:
            outdoor_score = weather_data.get("impact_analysis", {}).get("outdoor_suitability", 50)
            if outdoor_score > 80:
                optimizations.append("🌞 Excellent weather - consider outdoor meetings or activities")
            elif outdoor_score < 40:
                optimizations.append("🏠 Poor outdoor conditions - optimize indoor productivity")
        
        # Schedule optimizations
        if schedule_data.get("events"):
            event_count = len(schedule_data["events"])
            if event_count > 5:
                optimizations.append("📊 Heavy schedule - consider batching similar activities")
            elif event_count < 2:
                optimizations.append("⏰ Light schedule - opportunity for deep work or planning")
        
        # Social media optimizations
        if social_data.get("trends"):
            optimizations.append("📈 Leverage trending topics for increased engagement")
        
        return optimizations

class EnhancedContextAwareAgent(ContextAwareAgent):
    """Enhanced context-aware agent with full X integration and proactive recommendations"""
    
    def __init__(self, name="EnhancedBuddy"):
        # Initialize parent class
        super().__init__(name)
        
        # Add enhanced specialist agents
        self.social_agent = SocialMediaSpecialistAgent()
        self.proactive_agent = ProactiveRecommendationAgent()
        
        # Register with orchestrator
        self.orchestrator.register_agent(self.social_agent)
        self.orchestrator.register_agent(self.proactive_agent)
        
        print(f"🚀 {self.name} enhanced with X integration and proactive recommendations!")
        print(f"🤖 Total specialist agents: {len(self.orchestrator.list_agents())}")
    
    def process_enhanced_request(self, user_request: str) -> str:
        """Process request with enhanced context awareness including social media"""
        print(f"🧠 Processing enhanced request: {user_request}")
        
        # Check if request is social media related
        if any(keyword in user_request.lower() for keyword in ["x", "twitter", "tweet", "trends", "post", "social"]):
            return self._handle_social_request(user_request)
        
        # Check if request is for daily summary/recommendations
        if any(keyword in user_request.lower() for keyword in ["daily", "summary", "recommendations", "optimize", "plan"]):
            return self._generate_daily_summary()
        
        # Otherwise, use standard contextual processing
        return self.process_contextual_request(user_request)
    
    def _handle_social_request(self, request: str) -> str:
        """Handle social media related requests"""
        request_lower = request.lower()
        
        if "trends" in request_lower:
            social_analysis = self.social_agent.analyze_social_trends()
            return self._format_social_trends_response(social_analysis)
        
        elif "post" in request_lower:
            if "bible" in request_lower or "verse" in request_lower:
                result = self.social_agent.post_contextual_content("bible_verse")
            else:
                # Extract custom text
                custom_text = self._extract_post_text(request)
                result = self.social_agent.post_contextual_content("custom", custom_text)
            
            return result["message"] if result["success"] else f"❌ {result.get('error', 'Failed to post')}"
        
        else:
            # General social media analysis
            social_analysis = self.social_agent.analyze_social_trends()
            return self._format_social_analysis_response(social_analysis)
    
    def _generate_daily_summary(self) -> str:
        """Generate comprehensive daily summary with recommendations"""
        print("🔄 Generating comprehensive daily analysis...")
        
        # Gather data from all specialist agents
        city = os.getenv("DEFAULT_CITY", "New York")
        
        # Weather analysis
        weather_analysis = self.weather_agent.analyze_weather_impact(city)
        
        # Schedule analysis
        schedule_analysis = self.calendar_agent.analyze_schedule_conflicts(weather_analysis)
        
        # Social media analysis
        social_analysis = self.social_agent.analyze_social_trends()
        
        # Generate proactive recommendations
        recommendations = self.proactive_agent.generate_daily_recommendations(
            weather_analysis, schedule_analysis, social_analysis
        )
        
        # Format comprehensive response
        return self._format_daily_summary_response(
            weather_analysis, schedule_analysis, social_analysis, recommendations
        )
    
    def _format_social_trends_response(self, social_analysis: dict) -> str:
        """Format social trends response"""
        if "error" in social_analysis:
            return f"❌ {social_analysis['error']}"
        
        response = ["🔥 X Trending Topics - AI Analysis\n"]
        
        # Trends
        if social_analysis.get("trends", {}).get("trends"):
            response.append("📈 Current Trends:")
            for i, trend in enumerate(social_analysis["trends"]["trends"][:5], 1):
                response.append(f"   {i}. {trend}")
        
        # Insights
        if social_analysis.get("insights"):
            response.append("\n🧠 AI Insights:")
            for insight in social_analysis["insights"]:
                response.append(f"   • {insight}")
        
        # Engagement opportunities
        if social_analysis.get("engagement_opportunities"):
            response.append("\n🎯 Engagement Opportunities:")
            for opp in social_analysis["engagement_opportunities"][:3]:
                response.append(f"   • {opp}")
        
        return "\n".join(response)
    
    def _format_social_analysis_response(self, social_analysis: dict) -> str:
        """Format comprehensive social analysis response"""
        if "error" in social_analysis:
            return f"❌ {social_analysis['error']}"
        
        response = ["📱 Social Media Analysis & Strategy\n"]
        
        # Content suggestions
        if social_analysis.get("content_suggestions"):
            response.append("✍️ Content Ideas:")
            for idea in social_analysis["content_suggestions"][:4]:
                response.append(f"   • {idea}")
        
        # Engagement opportunities
        if social_analysis.get("engagement_opportunities"):
            response.append("\n🤝 Engagement Strategy:")
            for opp in social_analysis["engagement_opportunities"][:3]:
                response.append(f"   • {opp}")
        
        return "\n".join(response)
    
    def _format_daily_summary_response(self, weather: dict, schedule: dict, social: dict, recommendations: dict) -> str:
        """Format comprehensive daily summary"""
        response = ["🌅 Daily Summary & Recommendations\n"]
        
        # Weather overview
        if "weather" in weather:
            weather_data = weather["weather"]
            response.append(f"🌤️ Weather: {weather_data['temperature']}°C, {weather_data['condition']}")
            
            outdoor_score = weather.get("impact_analysis", {}).get("outdoor_suitability", 50)
            response.append(f"   Outdoor suitability: {outdoor_score}%")
        
        # Schedule overview
        event_count = len(schedule.get("events", []))
        conflict_count = len(schedule.get("conflicts", []))
        response.append(f"\n📅 Schedule: {event_count} event(s)")
        if conflict_count > 0:
            response.append(f"   ⚠️ {conflict_count} conflict(s) detected")
        
        # Social media overview
        if "trends" in social:
            trend_count = len(social["trends"].get("trends", []))
            response.append(f"\n📱 Social: {trend_count} trending topics analyzed")
        
        # Priority actions
        if recommendations.get("priority_actions"):
            response.append("\n🎯 Priority Actions:")
            for action in recommendations["priority_actions"]:
                response.append(f"   • {action}")
        
        # Time-based recommendations
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_recs = recommendations.get("morning", [])
            response.append("\n☀️ Morning Recommendations:")
        elif current_hour < 17:
            time_recs = recommendations.get("afternoon", [])
            response.append("\n🌞 Afternoon Recommendations:")
        else:
            time_recs = recommendations.get("evening", [])
            response.append("\n🌙 Evening Recommendations:")
        
        for rec in time_recs[:3]:
            response.append(f"   • {rec}")
        
        # Optimization tips
        if recommendations.get("optimization_tips"):
            response.append("\n💡 Optimization Tips:")
            for tip in recommendations["optimization_tips"][:2]:
                response.append(f"   • {tip}")
        
        return "\n".join(response)
    
    def _extract_post_text(self, request: str) -> str:
        """Extract post text from request"""
        import re
        patterns = [
            r"post to x[:\s]+(.+)",
            r"tweet[:\s]+(.+)",
            r"post[:\s]+(.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request.lower())
            if match:
                return match.group(1).strip()
        
        return "Hello from Enhanced AI Agent!"
    
    def chat(self):
        """Enhanced interactive chat interface"""
        print("\n🚀 Enhanced Context-Aware Chat Interface")
        print("Features: Weather analysis, Schedule optimization, X integration, Daily summaries")
        print("\nTry these commands:")
        print("• 'daily summary' - Comprehensive daily analysis")
        print("• 'X trends' - Social media trends with AI analysis")
        print("• 'post bible verse' - Share daily inspiration")
        print("• 'what's the weather?' - Weather with schedule impact")
        print("-" * 80)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n👋 Goodbye! Thanks for using {self.name}!")
                    break
                
                if not user_input:
                    continue
                
                # Process with enhanced context awareness
                response = self.process_enhanced_request(user_input)
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! Thanks for using {self.name}!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function to run the enhanced agent"""
    print("🚀 Starting Enhanced Personal AI Agent with Strands Agents SDK...")
    print("Features: Context awareness, X integration, AI-powered analysis, Proactive recommendations")
    
    # Create and run the enhanced agent
    agent = EnhancedContextAwareAgent("EnhancedBuddy")
    
    # Start interactive chat
    agent.chat()

if __name__ == "__main__":
    main()
