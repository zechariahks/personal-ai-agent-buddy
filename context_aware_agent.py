#!/usr/bin/env python3
"""
Context-Aware Agent Implementation using Strands Agents SDK
Advanced multi-agent system with specialist sub-agents for cross-domain reasoning
"""

import os
import json
from datetime import datetime, timedelta
from strands_agents import SmartAgent, AgentOrchestrator, create_agent
from agent_capabilities import (
    WeatherCapability, EmailCapability, CalendarCapability,
    GoogleCalendarCapability, XCapability
)

class WeatherSpecialistAgent(SmartAgent):
    """Specialized agent for weather analysis and impact assessment"""
    
    def __init__(self):
        super().__init__(
            name="WeatherBot",
            description="Specialist agent for weather analysis and activity impact assessment"
        )
        self.add_capability(WeatherCapability())
    
    def analyze_weather_impact(self, city: str, events: list = None) -> dict:
        """Analyze weather impact on scheduled events"""
        # Get weather data
        weather_result = self.execute_capability("weather", {"city": city})
        
        if not weather_result.success:
            return {"error": weather_result.message}
        
        weather_data = weather_result.data["weather"]
        impact_analysis = weather_result.data["impact_analysis"]
        
        # Analyze impact on events if provided
        event_impacts = []
        if events:
            for event in events:
                event_impact = self._assess_event_impact(event, weather_data, impact_analysis)
                event_impacts.append(event_impact)
        
        return {
            "weather": weather_data,
            "impact_analysis": impact_analysis,
            "event_impacts": event_impacts,
            "recommendations": self._generate_contextual_recommendations(weather_data, events)
        }
    
    def _assess_event_impact(self, event: dict, weather_data: dict, impact_analysis: dict) -> dict:
        """Assess weather impact on a specific event"""
        event_type = event.get("title", "").lower()
        outdoor_score = impact_analysis["outdoor_suitability"]
        
        # Determine if event is likely outdoor
        outdoor_keywords = ["picnic", "outdoor", "park", "beach", "hiking", "sports", "barbecue", "festival"]
        is_outdoor = any(keyword in event_type for keyword in outdoor_keywords)
        
        impact_level = "low"
        recommendations = []
        
        if is_outdoor and outdoor_score < 50:
            impact_level = "high"
            recommendations.append("Consider moving indoors or rescheduling")
        elif is_outdoor and outdoor_score < 75:
            impact_level = "medium"
            recommendations.append("Have backup indoor plan ready")
        
        if weather_data["condition"].lower() in ["rainy", "snowy"]:
            recommendations.append("Bring appropriate weather gear")
        
        return {
            "event": event,
            "impact_level": impact_level,
            "is_outdoor": is_outdoor,
            "recommendations": recommendations
        }
    
    def _generate_contextual_recommendations(self, weather_data: dict, events: list) -> list:
        """Generate contextual recommendations based on weather and events"""
        recommendations = []
        condition = weather_data["condition"].lower()
        temp = weather_data["temperature"]
        
        # General weather recommendations
        if condition == "rainy":
            recommendations.append("Carry an umbrella and wear waterproof clothing")
        elif condition == "snowy":
            recommendations.append("Allow extra travel time and dress warmly")
        elif temp > 30:
            recommendations.append("Stay hydrated and avoid prolonged sun exposure")
        elif temp < 5:
            recommendations.append("Dress in layers and protect extremities")
        
        # Event-specific recommendations
        if events:
            outdoor_events = [e for e in events if self._is_likely_outdoor(e)]
            if outdoor_events and condition in ["rainy", "snowy", "stormy"]:
                recommendations.append(f"Consider rescheduling {len(outdoor_events)} outdoor event(s)")
        
        return recommendations
    
    def _is_likely_outdoor(self, event: dict) -> bool:
        """Determine if an event is likely to be outdoors"""
        event_text = event.get("title", "").lower()
        outdoor_keywords = ["picnic", "outdoor", "park", "beach", "hiking", "sports", "barbecue", "festival", "walk"]
        return any(keyword in event_text for keyword in outdoor_keywords)

class CalendarSpecialistAgent(SmartAgent):
    """Specialized agent for calendar management and conflict detection"""
    
    def __init__(self):
        super().__init__(
            name="CalendarBot",
            description="Specialist agent for calendar management and scheduling optimization"
        )
        self.add_capability(CalendarCapability())
        self.add_capability(GoogleCalendarCapability())
    
    def analyze_schedule_conflicts(self, weather_impact: dict = None) -> dict:
        """Analyze schedule for conflicts and weather impacts"""
        # Get events from Google Calendar first, fallback to basic calendar
        google_result = self.execute_capability("google_calendar", {"action": "list"})
        
        if google_result.success and google_result.data:
            events = google_result.data
            source = "google_calendar"
        else:
            basic_result = self.execute_capability("calendar", {"action": "list"})
            events = basic_result.data if basic_result.success else []
            source = "basic_calendar"
        
        # Analyze conflicts
        conflicts = self._detect_conflicts(events)
        
        # Analyze weather impacts if provided
        weather_conflicts = []
        if weather_impact and weather_impact.get("event_impacts"):
            weather_conflicts = [
                impact for impact in weather_impact["event_impacts"]
                if impact["impact_level"] in ["medium", "high"]
            ]
        
        return {
            "events": events,
            "source": source,
            "conflicts": conflicts,
            "weather_conflicts": weather_conflicts,
            "recommendations": self._generate_scheduling_recommendations(conflicts, weather_conflicts)
        }
    
    def _detect_conflicts(self, events: list) -> list:
        """Detect scheduling conflicts between events"""
        conflicts = []
        
        # Simple conflict detection (for demo purposes)
        # In a real implementation, you'd parse dates/times properly
        for i, event1 in enumerate(events):
            for j, event2 in enumerate(events[i+1:], i+1):
                if self._events_overlap(event1, event2):
                    conflicts.append({
                        "event1": event1,
                        "event2": event2,
                        "type": "time_overlap"
                    })
        
        return conflicts
    
    def _events_overlap(self, event1: dict, event2: dict) -> bool:
        """Check if two events overlap (simplified)"""
        # For demo purposes, assume no overlaps
        # In real implementation, parse and compare datetime objects
        return False
    
    def _generate_scheduling_recommendations(self, conflicts: list, weather_conflicts: list) -> list:
        """Generate scheduling recommendations"""
        recommendations = []
        
        if conflicts:
            recommendations.append(f"Found {len(conflicts)} scheduling conflict(s) - review and reschedule")
        
        if weather_conflicts:
            for weather_conflict in weather_conflicts:
                event = weather_conflict["event"]
                recs = weather_conflict["recommendations"]
                recommendations.extend([f"{event.get('summary', event.get('title', 'Event'))}: {rec}" for rec in recs])
        
        if not conflicts and not weather_conflicts:
            recommendations.append("No scheduling conflicts detected - your calendar looks good!")
        
        return recommendations

class DecisionSpecialistAgent(SmartAgent):
    """Specialized agent for making cross-domain decisions and recommendations"""
    
    def __init__(self):
        super().__init__(
            name="DecisionBot",
            description="Specialist agent for cross-domain decision making and recommendations"
        )
    
    def make_contextual_decision(self, weather_analysis: dict, schedule_analysis: dict, user_request: str) -> dict:
        """Make intelligent decisions based on multiple data sources"""
        decision_factors = {
            "weather_impact": self._assess_weather_factors(weather_analysis),
            "schedule_impact": self._assess_schedule_factors(schedule_analysis),
            "user_intent": self._analyze_user_intent(user_request)
        }
        
        # Generate decision
        decision = self._generate_decision(decision_factors)
        
        return {
            "decision": decision,
            "factors": decision_factors,
            "confidence": self._calculate_confidence(decision_factors),
            "alternatives": self._suggest_alternatives(decision_factors)
        }
    
    def _assess_weather_factors(self, weather_analysis: dict) -> dict:
        """Assess weather-related decision factors"""
        if not weather_analysis or "error" in weather_analysis:
            return {"impact": "unknown", "score": 50}
        
        outdoor_score = weather_analysis.get("impact_analysis", {}).get("outdoor_suitability", 50)
        weather_conflicts = len(weather_analysis.get("event_impacts", []))
        
        return {
            "impact": "high" if outdoor_score < 50 else "low",
            "score": outdoor_score,
            "conflicts": weather_conflicts
        }
    
    def _assess_schedule_factors(self, schedule_analysis: dict) -> dict:
        """Assess schedule-related decision factors"""
        conflicts = len(schedule_analysis.get("conflicts", []))
        weather_conflicts = len(schedule_analysis.get("weather_conflicts", []))
        
        return {
            "conflicts": conflicts,
            "weather_conflicts": weather_conflicts,
            "impact": "high" if conflicts > 0 or weather_conflicts > 0 else "low"
        }
    
    def _analyze_user_intent(self, user_request: str) -> dict:
        """Analyze user intent from request"""
        request_lower = user_request.lower()
        
        intent_keywords = {
            "weather": ["weather", "temperature", "rain", "sunny", "cloudy"],
            "schedule": ["schedule", "calendar", "event", "meeting", "appointment"],
            "urgent": ["urgent", "important", "asap", "immediately"],
            "flexible": ["maybe", "if possible", "when convenient", "flexible"]
        }
        
        detected_intents = []
        for intent, keywords in intent_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                detected_intents.append(intent)
        
        return {
            "primary_intent": detected_intents[0] if detected_intents else "general",
            "all_intents": detected_intents,
            "urgency": "high" if "urgent" in detected_intents else "normal",
            "flexibility": "high" if "flexible" in detected_intents else "normal"
        }
    
    def _generate_decision(self, factors: dict) -> str:
        """Generate a decision based on all factors"""
        weather_impact = factors["weather_impact"]["impact"]
        schedule_impact = factors["schedule_impact"]["impact"]
        urgency = factors["user_intent"]["urgency"]
        
        if weather_impact == "high" and schedule_impact == "high":
            return "Recommend rescheduling due to weather and schedule conflicts"
        elif weather_impact == "high":
            return "Recommend weather-appropriate adjustments or indoor alternatives"
        elif schedule_impact == "high":
            return "Recommend resolving schedule conflicts before proceeding"
        elif urgency == "high":
            return "Proceed with caution but prioritize user urgency"
        else:
            return "Proceed as planned - conditions are favorable"
    
    def _calculate_confidence(self, factors: dict) -> float:
        """Calculate confidence score for the decision"""
        base_confidence = 0.7
        
        # Adjust based on data availability
        if factors["weather_impact"]["score"] != 50:  # Real weather data available
            base_confidence += 0.1
        
        if factors["schedule_impact"]["conflicts"] == 0:  # No conflicts
            base_confidence += 0.1
        
        if factors["user_intent"]["primary_intent"] != "general":  # Clear intent
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _suggest_alternatives(self, factors: dict) -> list:
        """Suggest alternative actions"""
        alternatives = []
        
        if factors["weather_impact"]["impact"] == "high":
            alternatives.append("Move outdoor activities indoors")
            alternatives.append("Reschedule for better weather")
        
        if factors["schedule_impact"]["conflicts"] > 0:
            alternatives.append("Reschedule conflicting events")
            alternatives.append("Shorten event durations to avoid conflicts")
        
        if factors["user_intent"]["flexibility"] == "high":
            alternatives.append("Postpone to a more convenient time")
        
        return alternatives

class ContextAwareAgent(SmartAgent):
    """Main context-aware agent that orchestrates specialist agents"""
    
    def __init__(self, name="ContextBuddy"):
        super().__init__(
            name=name,
            description="Context-aware AI agent with specialist sub-agents for intelligent decision making"
        )
        
        # Create orchestrator and specialist agents
        self.orchestrator = AgentOrchestrator("MainOrchestrator")
        self.weather_agent = WeatherSpecialistAgent()
        self.calendar_agent = CalendarSpecialistAgent()
        self.decision_agent = DecisionSpecialistAgent()
        
        # Register specialist agents
        self.orchestrator.register_agent(self.weather_agent)
        self.orchestrator.register_agent(self.calendar_agent)
        self.orchestrator.register_agent(self.decision_agent)
        
        # Add basic capabilities to main agent
        self.add_capability(EmailCapability())
        self.add_capability(XCapability())
        
        print(f"🧠 {self.name} initialized with context-aware capabilities!")
        print(f"🤖 Specialist agents: {', '.join(self.orchestrator.list_agents())}")
        
        self._check_services()
    
    def _check_services(self):
        """Check service availability"""
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
    
    def process_contextual_request(self, user_request: str) -> str:
        """Process request with full context awareness"""
        print(f"🧠 Processing contextual request: {user_request}")
        
        # Step 1: Analyze weather impact
        city = self._extract_city(user_request)
        weather_analysis = self.weather_agent.analyze_weather_impact(city)
        
        # Step 2: Analyze schedule
        schedule_analysis = self.calendar_agent.analyze_schedule_conflicts(weather_analysis)
        
        # Step 3: Make contextual decision
        decision_analysis = self.decision_agent.make_contextual_decision(
            weather_analysis, schedule_analysis, user_request
        )
        
        # Step 4: Generate comprehensive response
        response = self._generate_contextual_response(
            user_request, weather_analysis, schedule_analysis, decision_analysis
        )
        
        # Store context for future reference
        self.store_memory("last_analysis", {
            "request": user_request,
            "weather": weather_analysis,
            "schedule": schedule_analysis,
            "decision": decision_analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def _generate_contextual_response(self, request: str, weather: dict, schedule: dict, decision: dict) -> str:
        """Generate comprehensive contextual response"""
        response = []
        
        # Weather information
        if "error" not in weather:
            weather_data = weather["weather"]
            impact = weather["impact_analysis"]
            
            response.append(f"🌤️ Weather Analysis for {weather_data['city']}:")
            response.append(f"   • Temperature: {weather_data['temperature']}°C ({weather_data['condition']})")
            response.append(f"   • Outdoor suitability: {impact['outdoor_suitability']}%")
            
            if weather["event_impacts"]:
                response.append(f"\n📅 Schedule Impact Analysis:")
                response.append(f"   Found {len(weather['event_impacts'])} potential conflict(s):")
                
                for impact in weather["event_impacts"]:
                    if impact["impact_level"] != "low":
                        event_name = impact["event"].get("summary", impact["event"].get("title", "Event"))
                        response.append(f"   • {event_name} ({impact['impact_level']} impact)")
                        for rec in impact["recommendations"]:
                            response.append(f"     💡 {rec}")
        
        # Schedule analysis
        if schedule["conflicts"] or schedule["weather_conflicts"]:
            response.append(f"\n⚠️ Schedule Conflicts Detected:")
            for conflict in schedule["conflicts"]:
                response.append(f"   • Time overlap between events")
            
            for weather_conflict in schedule["weather_conflicts"]:
                event_name = weather_conflict["event"].get("summary", weather_conflict["event"].get("title", "Event"))
                response.append(f"   • Weather impact on {event_name}")
        
        # Decision and recommendations
        response.append(f"\n🎯 Recommendation:")
        response.append(f"   {decision['decision']}")
        response.append(f"   Confidence: {decision['confidence']:.0%}")
        
        if decision["alternatives"]:
            response.append(f"\n🔄 Alternative Options:")
            for alt in decision["alternatives"]:
                response.append(f"   • {alt}")
        
        return "\n".join(response)
    
    def _extract_city(self, text: str) -> str:
        """Extract city name from text"""
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() == "in" and i + 1 < len(words):
                return words[i + 1].title()
        return os.getenv("DEFAULT_CITY", "New York")
    
    def chat(self):
        """Interactive chat interface with context awareness"""
        print("\n🧠 Context-Aware Chat Interface")
        print("I can analyze weather impacts on your schedule and make intelligent recommendations!")
        print("Try: 'What's the weather like?' or 'Check my schedule for conflicts'")
        print("-" * 70)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n👋 Goodbye! Thanks for using {self.name}!")
                    break
                
                if not user_input:
                    continue
                
                # Process with full context awareness
                response = self.process_contextual_request(user_input)
                print(f"\n{self.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Goodbye! Thanks for using {self.name}!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function to run the context-aware agent"""
    print("🚀 Starting Context-Aware Personal AI Agent with Strands Agents SDK...")
    
    # Create and run the agent
    agent = ContextAwareAgent("ContextBuddy")
    
    # Start interactive chat
    agent.chat()

if __name__ == "__main__":
    main()
