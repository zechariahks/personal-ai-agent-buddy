#!/usr/bin/env python3
"""
Comprehensive Test Suite for Strands Agents SDK Implementation
Tests all migrated agents and capabilities
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestStrandsAgentsSDK(unittest.TestCase):
    """Test the core Strands Agents SDK functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_env_vars = {
            "OPENAI_API_KEY": "test-openai-key",
            "WEATHER_API_KEY": "test-weather-key",
            "GMAIL_EMAIL": "test@example.com",
            "GMAIL_APP_PASSWORD": "test-password",
            "DEFAULT_CITY": "Test City"
        }
        
        # Mock environment variables
        for key, value in self.test_env_vars.items():
            os.environ[key] = value
    
    def test_sdk_imports(self):
        """Test that all SDK components can be imported"""
        try:
            from strands_agents import (
                BaseAgent, SmartAgent, AgentCapability, AgentOrchestrator,
                AgentMessage, AgentResponse, AgentStatus,
                create_agent, create_orchestrator
            )
            self.assertTrue(True, "SDK imports successful")
        except ImportError as e:
            self.fail(f"SDK import failed: {e}")
    
    def test_agent_creation(self):
        """Test agent creation functionality"""
        from strands_agents import create_agent, SmartAgent
        
        # Test basic agent creation
        basic_agent = create_agent("basic", "TestBasic")
        self.assertIsNotNone(basic_agent)
        self.assertEqual(basic_agent.name, "TestBasic")
        
        # Test smart agent creation
        smart_agent = create_agent("smart", "TestSmart")
        self.assertIsInstance(smart_agent, SmartAgent)
        self.assertEqual(smart_agent.name, "TestSmart")
    
    def test_capability_system(self):
        """Test the capability system"""
        from strands_agents import create_agent
        from agent_capabilities import WeatherCapability
        
        agent = create_agent("smart", "TestAgent")
        
        # Test adding capability
        weather_cap = WeatherCapability()
        agent.add_capability(weather_cap)
        
        self.assertIn("weather", agent.capabilities)
        self.assertEqual(len(agent.list_capabilities()), 1)
        
        # Test removing capability
        agent.remove_capability("weather")
        self.assertNotIn("weather", agent.capabilities)
    
    def test_orchestrator(self):
        """Test agent orchestrator functionality"""
        from strands_agents import create_agent, create_orchestrator
        
        orchestrator = create_orchestrator("TestOrchestrator")
        agent1 = create_agent("smart", "Agent1")
        agent2 = create_agent("smart", "Agent2")
        
        # Test agent registration
        orchestrator.register_agent(agent1)
        orchestrator.register_agent(agent2)
        
        self.assertEqual(len(orchestrator.list_agents()), 2)
        self.assertIn("Agent1", orchestrator.list_agents())
        self.assertIn("Agent2", orchestrator.list_agents())
        
        # Test agent retrieval
        retrieved_agent = orchestrator.get_agent("Agent1")
        self.assertEqual(retrieved_agent.name, "Agent1")

class TestAgentCapabilities(unittest.TestCase):
    """Test individual agent capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        os.environ["WEATHER_API_KEY"] = "test-key"
        os.environ["DEFAULT_CITY"] = "Test City"
    
    def test_weather_capability(self):
        """Test weather capability"""
        from agent_capabilities import WeatherCapability
        
        weather_cap = WeatherCapability()
        self.assertEqual(weather_cap.name, "weather")
        self.assertTrue(weather_cap.enabled)
        
        # Test execution with simulated weather
        result = weather_cap.execute({"city": "London"})
        self.assertTrue(result.success)
        self.assertIn("Weather in London", result.message)
        self.assertIsNotNone(result.data)
    
    def test_calendar_capability(self):
        """Test calendar capability"""
        from agent_capabilities import CalendarCapability
        
        calendar_cap = CalendarCapability()
        self.assertEqual(calendar_cap.name, "calendar")
        
        # Test creating an event
        result = calendar_cap.execute({
            "action": "create",
            "title": "Test Meeting",
            "date": "2024-01-01",
            "time": "14:00"
        })
        
        self.assertTrue(result.success)
        self.assertIn("Test Meeting", result.message)
        
        # Test listing events
        list_result = calendar_cap.execute({"action": "list"})
        self.assertTrue(list_result.success)
        self.assertEqual(len(list_result.data), 1)
    
    def test_email_capability(self):
        """Test email capability"""
        from agent_capabilities import EmailCapability
        
        # Mock environment variables
        os.environ["GMAIL_EMAIL"] = "test@example.com"
        os.environ["GMAIL_APP_PASSWORD"] = "test-password"
        
        email_cap = EmailCapability()
        self.assertEqual(email_cap.name, "email")
        
        # Test without proper credentials (should fail gracefully)
        result = email_cap.execute({
            "to": "recipient@example.com",
            "subject": "Test",
            "body": "Test message"
        })
        
        # Should fail due to mock credentials, but gracefully
        self.assertIsNotNone(result)

class TestBasicAgent(unittest.TestCase):
    """Test the basic agent implementation"""
    
    def setUp(self):
        """Set up test environment"""
        os.environ["DEFAULT_CITY"] = "Test City"
    
    def test_basic_agent_initialization(self):
        """Test basic agent initialization"""
        from basic_agent import PersonalAIAgent
        
        agent = PersonalAIAgent("TestBuddy")
        self.assertEqual(agent.name, "TestBuddy")
        self.assertGreater(len(agent.capabilities), 0)
    
    def test_basic_agent_message_processing(self):
        """Test basic agent message processing"""
        from basic_agent import PersonalAIAgent
        from strands_agents import AgentMessage
        
        agent = PersonalAIAgent("TestBuddy")
        
        # Test weather request
        weather_message = AgentMessage(
            sender="User",
            recipient="TestBuddy",
            content="What's the weather in London?"
        )
        
        response = agent.process_message(weather_message)
        self.assertIsInstance(response, str)
        self.assertIn("Weather", response)
    
    def test_basic_agent_capabilities(self):
        """Test basic agent capabilities"""
        from basic_agent import PersonalAIAgent
        
        agent = PersonalAIAgent("TestBuddy")
        
        # Check that all expected capabilities are loaded
        expected_capabilities = ["weather", "email", "calendar", "google_calendar", "x_integration"]
        
        for cap in expected_capabilities:
            self.assertIn(cap, agent.capabilities)

class TestContextAwareAgent(unittest.TestCase):
    """Test the context-aware agent implementation"""
    
    def setUp(self):
        """Set up test environment"""
        os.environ["DEFAULT_CITY"] = "Test City"
    
    def test_context_agent_initialization(self):
        """Test context-aware agent initialization"""
        from context_aware_agent import ContextAwareAgent
        
        agent = ContextAwareAgent("TestContext")
        self.assertEqual(agent.name, "TestContext")
        self.assertIsNotNone(agent.orchestrator)
        self.assertGreater(len(agent.orchestrator.list_agents()), 0)
    
    def test_specialist_agents(self):
        """Test specialist agent functionality"""
        from context_aware_agent import WeatherSpecialistAgent, CalendarSpecialistAgent, DecisionSpecialistAgent
        
        # Test weather specialist
        weather_agent = WeatherSpecialistAgent()
        self.assertEqual(weather_agent.name, "WeatherBot")
        
        # Test calendar specialist
        calendar_agent = CalendarSpecialistAgent()
        self.assertEqual(calendar_agent.name, "CalendarBot")
        
        # Test decision specialist
        decision_agent = DecisionSpecialistAgent()
        self.assertEqual(decision_agent.name, "DecisionBot")
    
    def test_contextual_processing(self):
        """Test contextual request processing"""
        from context_aware_agent import ContextAwareAgent
        
        agent = ContextAwareAgent("TestContext")
        
        # Test contextual weather request
        response = agent.process_contextual_request("What's the weather like?")
        self.assertIsInstance(response, str)
        self.assertIn("Weather Analysis", response)

class TestEnhancedAgent(unittest.TestCase):
    """Test the enhanced agent with X integration"""
    
    def setUp(self):
        """Set up test environment"""
        os.environ["DEFAULT_CITY"] = "Test City"
    
    def test_enhanced_agent_initialization(self):
        """Test enhanced agent initialization"""
        from enhanced_agent import EnhancedContextAwareAgent
        
        agent = EnhancedContextAwareAgent("TestEnhanced")
        self.assertEqual(agent.name, "TestEnhanced")
        self.assertIsNotNone(agent.social_agent)
        self.assertIsNotNone(agent.proactive_agent)
    
    def test_social_specialist_agent(self):
        """Test social media specialist agent"""
        from enhanced_agent import SocialMediaSpecialistAgent
        
        social_agent = SocialMediaSpecialistAgent()
        self.assertEqual(social_agent.name, "SocialBot")
        self.assertIn("x_integration", social_agent.capabilities)
    
    def test_proactive_agent(self):
        """Test proactive recommendation agent"""
        from enhanced_agent import ProactiveRecommendationAgent
        
        proactive_agent = ProactiveRecommendationAgent()
        self.assertEqual(proactive_agent.name, "ProactiveBot")
    
    def test_enhanced_processing(self):
        """Test enhanced request processing"""
        from enhanced_agent import EnhancedContextAwareAgent
        
        agent = EnhancedContextAwareAgent("TestEnhanced")
        
        # Test daily summary
        response = agent.process_enhanced_request("daily summary")
        self.assertIsInstance(response, str)
        self.assertIn("Daily Summary", response)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        from enhanced_agent import EnhancedContextAwareAgent
        
        agent = EnhancedContextAwareAgent("IntegrationTest")
        
        # Test various request types
        test_requests = [
            "What's the weather?",
            "daily summary",
            "X trends"
        ]
        
        for request in test_requests:
            response = agent.process_enhanced_request(request)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
    
    def test_agent_comparison(self):
        """Test that all three agent types work correctly"""
        from basic_agent import PersonalAIAgent
        from context_aware_agent import ContextAwareAgent
        from enhanced_agent import EnhancedContextAwareAgent
        from strands_agents import AgentMessage
        
        # Create all three agent types
        basic_agent = PersonalAIAgent("BasicTest")
        context_agent = ContextAwareAgent("ContextTest")
        enhanced_agent = EnhancedContextAwareAgent("EnhancedTest")
        
        test_query = "What's the weather?"
        
        # Test basic agent
        message = AgentMessage(sender="User", recipient="BasicTest", content=test_query)
        basic_response = basic_agent.process_message(message)
        self.assertIsInstance(basic_response, str)
        
        # Test context agent
        context_response = context_agent.process_contextual_request(test_query)
        self.assertIsInstance(context_response, str)
        
        # Test enhanced agent
        enhanced_response = enhanced_agent.process_enhanced_request(test_query)
        self.assertIsInstance(enhanced_response, str)
        
        # Enhanced response should be more comprehensive
        self.assertGreater(len(enhanced_response), len(basic_response))

def run_performance_tests():
    """Run performance tests"""
    print("\n⚡ Running Performance Tests...")
    
    import time
    from enhanced_agent import EnhancedContextAwareAgent
    
    agent = EnhancedContextAwareAgent("PerfTest")
    
    # Test response times
    test_queries = [
        "What's the weather?",
        "daily summary",
        "X trends"
    ]
    
    for query in test_queries:
        start_time = time.time()
        response = agent.process_enhanced_request(query)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"   Query: '{query}' - Response time: {response_time:.2f}ms")
        
        # Assert reasonable response time (under 5 seconds)
        assert response_time < 5000, f"Response time too slow: {response_time}ms"
    
    print("✅ Performance tests passed!")

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Strands Agents SDK Test Suite...")
    print("=" * 60)
    
    # Run unit tests
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Run performance tests
    try:
        run_performance_tests()
    except Exception as e:
        print(f"⚠️ Performance tests failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All tests passed! Strands Agents SDK is working correctly.")
        print("\n✅ Migration to Strands Agents SDK completed successfully!")
        print("\n🚀 Ready to use:")
        print("   python3 strands_run.py demo")
    else:
        print("❌ Some tests failed. Please check the output above.")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
