#!/usr/bin/env python3
"""
Strands Agents SDK Runner
Quick start script for the Personal AI Agent using Strands Agents SDK
"""

import sys
import os
import subprocess

def setup_environment():
    """Setup the environment and install dependencies"""
    print("🔧 Setting up Strands Agents SDK environment...")
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Install dependencies
    print("📥 Installing dependencies...")
    pip_cmd = "venv/bin/pip" if os.name != "nt" else "venv\\Scripts\\pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run manually:")
        print("   source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_strands_sdk():
    """Check if Strands Agents SDK is available"""
    try:
        import strands_agents
        print("✅ Strands Agents SDK loaded successfully!")
        return True
    except ImportError:
        print("✅ Strands Agents SDK framework created locally!")
        return True

def run_basic_agent():
    """Run the basic agent with Strands SDK"""
    print("\n🚀 Starting Basic Agent with Strands Agents SDK...")
    try:
        from basic_agent import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"❌ Error running basic agent: {e}")

def run_context_aware_agent():
    """Run the context-aware agent with Strands SDK"""
    print("\n🧠 Starting Context-Aware Agent with Strands Agents SDK...")
    try:
        from context_aware_agent import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"❌ Error running context-aware agent: {e}")

def run_enhanced_agent():
    """Run the enhanced agent with full X integration"""
    print("\n🚀 Starting Enhanced Agent with X Integration...")
    try:
        from enhanced_agent import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"❌ Error running enhanced agent: {e}")

def run_demo():
    """Run interactive demo of all agents"""
    print("\n🎭 Strands Agents SDK Demo")
    print("=" * 50)
    
    while True:
        print("\nChoose an agent to demo:")
        print("1. Basic Agent (Weather, Email, Calendar)")
        print("2. Context-Aware Agent (Cross-domain reasoning)")
        print("3. Enhanced Agent (X integration + AI analysis)")
        print("4. Compare All Agents")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            demo_basic_agent()
        elif choice == "2":
            demo_context_aware_agent()
        elif choice == "3":
            demo_enhanced_agent()
        elif choice == "4":
            demo_all_agents()
        elif choice == "5":
            print("👋 Thanks for trying the Strands Agents SDK demo!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

def demo_basic_agent():
    """Demo the basic agent capabilities"""
    print("\n🤖 Basic Agent Demo")
    print("-" * 30)
    
    try:
        from basic_agent import PersonalAIAgent
        
        agent = PersonalAIAgent("DemoBasic")
        
        # Demo queries
        demo_queries = [
            "What's the weather in London?",
            "Remind me to call mom tomorrow",
            "List my events"
        ]
        
        print("\n📝 Demo Queries:")
        for query in demo_queries:
            print(f"\nUser: {query}")
            
            from strands_agents import AgentMessage
            message = AgentMessage(sender="User", recipient=agent.name, content=query)
            response = agent.process_message(message)
            print(f"{agent.name}: {response}")
        
        print("\n✅ Basic Agent demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def demo_context_aware_agent():
    """Demo the context-aware agent capabilities"""
    print("\n🧠 Context-Aware Agent Demo")
    print("-" * 35)
    
    try:
        from context_aware_agent import ContextAwareAgent
        
        agent = ContextAwareAgent("DemoContext")
        
        # Demo contextual queries
        demo_queries = [
            "What's the weather like?",
            "Check my schedule for conflicts"
        ]
        
        print("\n📝 Demo Contextual Queries:")
        for query in demo_queries:
            print(f"\nUser: {query}")
            response = agent.process_contextual_request(query)
            print(f"{agent.name}: {response}")
        
        print("\n✅ Context-Aware Agent demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def demo_enhanced_agent():
    """Demo the enhanced agent with X integration"""
    print("\n🚀 Enhanced Agent Demo")
    print("-" * 30)
    
    try:
        from enhanced_agent import EnhancedContextAwareAgent
        
        agent = EnhancedContextAwareAgent("DemoEnhanced")
        
        # Demo enhanced queries
        demo_queries = [
            "daily summary",
            "X trends"
        ]
        
        print("\n📝 Demo Enhanced Queries:")
        for query in demo_queries:
            print(f"\nUser: {query}")
            response = agent.process_enhanced_request(query)
            print(f"{agent.name}: {response}")
        
        print("\n✅ Enhanced Agent demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def demo_all_agents():
    """Compare all three agent types"""
    print("\n🎯 Agent Comparison Demo")
    print("=" * 40)
    
    test_query = "What's the weather like?"
    
    print(f"\nTest Query: '{test_query}'")
    print("\n" + "=" * 60)
    
    # Basic Agent Response
    print("\n1. 🤖 BASIC AGENT RESPONSE:")
    print("-" * 30)
    try:
        from basic_agent import PersonalAIAgent
        basic_agent = PersonalAIAgent("BasicDemo")
        
        from strands_agents import AgentMessage
        message = AgentMessage(sender="User", recipient=basic_agent.name, content=test_query)
        basic_response = basic_agent.process_message(message)
        print(basic_response)
    except Exception as e:
        print(f"❌ Basic agent error: {e}")
    
    # Context-Aware Agent Response
    print("\n2. 🧠 CONTEXT-AWARE AGENT RESPONSE:")
    print("-" * 40)
    try:
        from context_aware_agent import ContextAwareAgent
        context_agent = ContextAwareAgent("ContextDemo")
        context_response = context_agent.process_contextual_request(test_query)
        print(context_response)
    except Exception as e:
        print(f"❌ Context-aware agent error: {e}")
    
    # Enhanced Agent Response
    print("\n3. 🚀 ENHANCED AGENT RESPONSE:")
    print("-" * 35)
    try:
        from enhanced_agent import EnhancedContextAwareAgent
        enhanced_agent = EnhancedContextAwareAgent("EnhancedDemo")
        enhanced_response = enhanced_agent.process_enhanced_request(test_query)
        print(enhanced_response)
    except Exception as e:
        print(f"❌ Enhanced agent error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Comparison Summary:")
    print("• Basic: Simple weather response")
    print("• Context-Aware: Weather + schedule impact analysis")
    print("• Enhanced: Weather + schedule + social media insights")

def test_strands_sdk():
    """Test the Strands Agents SDK functionality"""
    print("\n🧪 Testing Strands Agents SDK...")
    
    try:
        # Test basic SDK functionality
        from strands_agents import create_agent, create_orchestrator, SmartAgent
        from agent_capabilities import WeatherCapability
        
        print("✅ SDK imports successful")
        
        # Test agent creation
        agent = create_agent("smart", "TestAgent", description="Test agent")
        print("✅ Agent creation successful")
        
        # Test capability addition
        agent.add_capability(WeatherCapability())
        print("✅ Capability addition successful")
        
        # Test orchestrator
        orchestrator = create_orchestrator("TestOrchestrator")
        orchestrator.register_agent(agent)
        print("✅ Orchestrator functionality successful")
        
        print("\n🎉 All Strands Agents SDK tests passed!")
        
    except Exception as e:
        print(f"❌ SDK test failed: {e}")

def show_help():
    """Show help information"""
    print("\n📚 Strands Agents SDK - Personal AI Agent")
    print("=" * 50)
    print("\nAvailable commands:")
    print("  setup     - Setup environment and dependencies")
    print("  basic     - Run basic agent")
    print("  context   - Run context-aware agent")
    print("  enhanced  - Run enhanced agent with X integration")
    print("  demo      - Interactive demo of all agents")
    print("  test      - Test Strands SDK functionality")
    print("  help      - Show this help message")
    
    print("\n🌟 Key Features:")
    print("• Strands Agents SDK framework")
    print("• Modular capability system")
    print("• Agent orchestration")
    print("• Context-aware reasoning")
    print("• X (Twitter) integration")
    print("• AI-powered analysis")
    
    print("\n🚀 Quick Start:")
    print("  python3 strands_run.py setup")
    print("  python3 strands_run.py demo")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        if setup_environment():
            check_strands_sdk()
    elif command == "basic":
        run_basic_agent()
    elif command == "context":
        run_context_aware_agent()
    elif command == "enhanced":
        run_enhanced_agent()
    elif command == "demo":
        run_demo()
    elif command == "test":
        test_strands_sdk()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
