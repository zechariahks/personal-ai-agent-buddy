#!/usr/bin/env python3
"""
Demo Script for Intelligent AI Agent
Showcases all capabilities with interactive examples
"""

import os
import time
from datetime import datetime
from basic_agent import IntelligentAgent
from context_aware_agent import ContextAwareAgent

class AgentDemo:
    """Interactive demo of agent capabilities"""
    
    def __init__(self):
        self.current_agent = None
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"🎯 {title}")
        print("=" * 60)
    
    def print_step(self, step_num, description):
        """Print a formatted step"""
        print(f"\n{step_num}. {description}")
        print("-" * 40)
    
    def wait_for_user(self, message="Press Enter to continue..."):
        """Wait for user input"""
        input(f"\n💡 {message}")
    
    def demo_basic_agent(self):
        """Demonstrate basic agent capabilities"""
        self.print_header("BASIC AGENT DEMONSTRATION")
        
        print("Creating a basic intelligent agent...")
        agent = IntelligentAgent("DemoBot")
        self.current_agent = agent
        
        self.wait_for_user()
        
        # Demo 1: Service Status
        self.print_step(1, "Checking Service Status")
        status = agent.get_service_status()
        print(status)
        self.wait_for_user()
        
        # Demo 2: Help System
        self.print_step(2, "Help System")
        help_text = agent.show_help()
        print(help_text)
        self.wait_for_user()
        
        # Demo 3: Weather (Basic)
        self.print_step(3, "Weather Information (Basic)")
        weather = agent.check_weather_basic("Paris")
        print(weather)
        self.wait_for_user()
        
        # Demo 4: Real Weather (if configured)
        if agent.services_status.get("Weather", False):
            self.print_step(4, "Real Weather Data")
            real_weather = agent.check_weather_real("London")
            print(real_weather)
            self.wait_for_user()
        else:
            print("\n4. Real Weather Data - Skipped (API key not configured)")
        
        # Demo 5: Reminders
        self.print_step(5, "Creating and Managing Reminders")
        reminder1 = agent.create_reminder_basic("Call the dentist tomorrow")
        print(reminder1)
        
        reminder2 = agent.create_reminder_basic("Buy groceries after work")
        print(reminder2)
        
        print("\nListing all reminders:")
        reminders = agent.list_reminders()
        print(reminders)
        self.wait_for_user()
        
        # Demo 6: Calendar Events
        self.print_step(6, "Creating and Managing Calendar Events")
        event1 = agent.create_calendar_event_basic("Team Meeting", "Tomorrow", "10:00 AM", "Weekly team sync")
        print(event1)
        
        event2 = agent.create_calendar_event_basic("Lunch with Client", "Friday", "12:30 PM", "Business lunch downtown")
        print(event2)
        
        print("\nListing all events:")
        events = agent.list_events()
        print(events)
        self.wait_for_user()
        
        # Demo 7: Natural Language Processing
        self.print_step(7, "Natural Language Understanding")
        test_requests = [
            "What's the weather in Tokyo?",
            "Remind me to water the plants",
            "Schedule a meeting tomorrow at 3 PM",
            "Show my reminders"
        ]
        
        for request in test_requests:
            print(f"\nUser: {request}")
            response = agent.process_request(request)
            print(f"Agent: {response}")
            time.sleep(1)
        
        self.wait_for_user()
        
        return agent
    
    def demo_context_aware_agent(self):
        """Demonstrate context-aware agent capabilities"""
        self.print_header("CONTEXT-AWARE AGENT DEMONSTRATION")
        
        print("Creating a context-aware intelligent agent with specialist sub-agents...")
        agent = ContextAwareAgent("ContextBot")
        self.current_agent = agent
        
        self.wait_for_user()
        
        # Demo 1: Specialist Agents
        self.print_step(1, "Specialist Agent Architecture")
        print("This agent has specialized sub-agents:")
        for name, specialist in agent.agent_specialists.items():
            print(f"• {name.title()} Agent ({specialist.name}): {specialist.__class__.__doc__.split('.')[0] if specialist.__class__.__doc__ else 'Specialized functionality'}")
        self.wait_for_user()
        
        # Demo 2: Add some test events for context
        self.print_step(2, "Setting Up Test Scenario")
        print("Adding some calendar events to demonstrate context awareness...")
        
        agent.create_calendar_event_basic("Outdoor Team Picnic", "Tomorrow", "2:00 PM", "Annual team building event in Central Park")
        agent.create_calendar_event_basic("Morning Jog", "Tomorrow", "7:00 AM", "Daily exercise routine around the neighborhood")
        agent.create_calendar_event_basic("Indoor Meeting", "Tomorrow", "10:00 AM", "Conference room strategy session")
        
        events = agent.list_events()
        print(events)
        self.wait_for_user()
        
        # Demo 3: Weather Analysis with Context
        self.print_step(3, "Contextual Weather Analysis")
        print("Now let's check the weather and see how the agent analyzes the impact...")
        
        if agent.services_status.get("Weather", False):
            print("\nAsking: 'What's the weather in New York?'")
            weather_response = agent.process_request("What's the weather in New York?")
            print(f"\nAgent Response:\n{weather_response}")
        else:
            print("Weather API not configured - demonstrating with mock data...")
            # Simulate the contextual analysis
            agent.demonstrate_agent_communication()
        
        self.wait_for_user()
        
        # Demo 4: Decision History
        self.print_step(4, "Decision Making History")
        if agent.decision_history:
            print("The agent has made the following contextual decisions:")
            for i, decision in enumerate(agent.decision_history, 1):
                print(f"\nDecision {i}:")
                print(f"• Trigger: {decision['trigger']}")
                print(f"• Decision: {decision['decision']}")
                print(f"• Confidence: {decision['confidence']}%")
                print(f"• Actions: {', '.join(decision['actions'])}")
                print(f"• Reasoning: {'; '.join(decision['reasoning'])}")
        else:
            print("No contextual decisions made yet.")
        
        self.wait_for_user()
        
        # Demo 5: Context Memory
        self.print_step(5, "Context Memory System")
        print("The agent maintains context memory across interactions:")
        if agent.context_memory:
            for key, value in agent.context_memory.items():
                print(f"\n• {key.replace('_', ' ').title()}:")
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, (str, int, float)):
                            print(f"  - {subkey}: {subvalue}")
                        elif isinstance(subvalue, list) and subvalue:
                            print(f"  - {subkey}: {len(subvalue)} items")
                        elif isinstance(subvalue, dict) and subvalue:
                            print(f"  - {subkey}: {list(subvalue.keys())}")
        else:
            print("Context memory is empty.")
        
        self.wait_for_user()
        
        return agent
    
    def demo_interactive_session(self, agent):
        """Run an interactive session with the agent"""
        self.print_header("INTERACTIVE SESSION")
        
        print(f"You can now chat directly with {agent.name}!")
        print("Try asking about weather, creating reminders, scheduling events, or general questions.")
        print("Type 'quit' to end the session.")
        
        self.wait_for_user("Press Enter to start the interactive session...")
        
        # Start the chat interface
        agent.chat()
    
    def demo_comparison(self):
        """Compare basic vs context-aware agents"""
        self.print_header("AGENT COMPARISON")
        
        print("Let's compare how basic and context-aware agents handle the same request:")
        
        # Create both agents
        basic = IntelligentAgent("BasicBot")
        context = ContextAwareAgent("ContextBot")
        
        # Add some events to both
        for agent in [basic, context]:
            agent.create_calendar_event_basic("Outdoor Concert", "Tomorrow", "7:00 PM", "Music festival in the park")
        
        test_request = "What's the weather tomorrow?"
        
        print(f"\nTest Request: '{test_request}'")
        
        print("\n🤖 BASIC AGENT RESPONSE:")
        print("-" * 30)
        basic_response = basic.process_request(test_request)
        print(basic_response)
        
        print("\n🧠 CONTEXT-AWARE AGENT RESPONSE:")
        print("-" * 30)
        context_response = context.process_request(test_request)
        print(context_response)
        
        print("\n📊 COMPARISON:")
        print("• Basic Agent: Provides weather information only")
        print("• Context-Aware Agent: Analyzes weather impact on scheduled events")
        print("• Context-Aware Agent: Suggests actions based on conflicts")
        print("• Context-Aware Agent: Considers multiple factors (travel, outdoor activities)")
        
        self.wait_for_user()
    
    def run_full_demo(self):
        """Run the complete demonstration"""
        print("🎭 Welcome to the Intelligent AI Agent Demo!")
        print("This demonstration will showcase all the capabilities of your AI agent.")
        
        while True:
            print("\n" + "=" * 60)
            print("🎯 DEMO MENU")
            print("=" * 60)
            print("1. Basic Agent Demo")
            print("2. Context-Aware Agent Demo")
            print("3. Agent Comparison")
            print("4. Interactive Session (Basic)")
            print("5. Interactive Session (Context-Aware)")
            print("6. Run All Demos")
            print("7. Exit")
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == "1":
                self.demo_basic_agent()
            elif choice == "2":
                self.demo_context_aware_agent()
            elif choice == "3":
                self.demo_comparison()
            elif choice == "4":
                agent = IntelligentAgent("InteractiveBot")
                self.demo_interactive_session(agent)
            elif choice == "5":
                agent = ContextAwareAgent("InteractiveContextBot")
                self.demo_interactive_session(agent)
            elif choice == "6":
                self.demo_basic_agent()
                self.demo_context_aware_agent()
                self.demo_comparison()
            elif choice == "7":
                print("\n👋 Thanks for trying the AI Agent Demo!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")


def main():
    """Main demo function"""
    # Check for .env file
    if not os.path.exists('.env'):
        print("⚠️  No .env file found.")
        print("The demo will work with limited functionality.")
        print("Create a .env file with your API keys for full functionality.")
        print("\nContinuing with demo...")
        time.sleep(2)
    
    # Run the demo
    demo = AgentDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
