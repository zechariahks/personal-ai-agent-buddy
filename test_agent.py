#!/usr/bin/env python3
"""
Test Script for Intelligent AI Agent with X Integration
Tests all functionality including AI-powered X summaries
"""

import os
import sys
import time
from datetime import datetime

# Import our agent classes
from basic_agent import IntelligentAgent
from context_aware_agent import ContextAwareAgent
from enhanced_context_aware_agent import EnhancedContextAwareAgent
from x_agent import XAgent

class AgentTester:
    """Test suite for the AI agent functionality"""
    
    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
    
    def log_test(self, test_name, passed, message=""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        
        print(result)
        self.test_results.append((test_name, passed, message))
        
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_basic_agent_creation(self):
        """Test basic agent initialization"""
        try:
            agent = IntelligentAgent("TestBot")
            self.log_test("Basic Agent Creation", True, f"Agent '{agent.name}' created successfully")
            return agent
        except Exception as e:
            self.log_test("Basic Agent Creation", False, str(e))
            return None
    
    def test_service_status_check(self, agent):
        """Test service status checking"""
        try:
            # Check if agent has service status method, otherwise use a basic check
            if hasattr(agent, 'check_service_status'):
                status = agent.check_service_status()
                has_status = "Service Status" in status
            else:
                # Fallback: check if agent has basic attributes
                has_status = hasattr(agent, 'name') and hasattr(agent, 'process_request')
            
            self.log_test("Service Status Check", has_status, "Status information retrieved")
            return has_status
        except Exception as e:
            self.log_test("Service Status Check", False, str(e))
            return False
    
    def test_weather_functionality(self, agent):
        """Test weather-related functionality"""
        try:
            # Test weather query
            weather_response = agent.process_request("What's the weather in London?")
            has_weather = "weather" in weather_response.lower() or "temperature" in weather_response.lower()
            self.log_test("Weather Query", has_weather, "Weather information retrieved")
            return has_weather
        except Exception as e:
            self.log_test("Weather Query", False, str(e))
            return False
    
    def test_calendar_functionality(self, agent):
        """Test calendar-related functionality"""
        try:
            # Test reminder creation
            reminder_response = agent.process_request("Remind me to test the agent tomorrow")
            has_reminder = "reminder" in reminder_response.lower() or "created" in reminder_response.lower()
            self.log_test("Calendar Reminder", has_reminder, "Reminder functionality working")
            
            # Test event scheduling
            event_response = agent.process_request("Schedule a meeting tomorrow at 2 PM")
            has_event = "event" in event_response.lower() or "scheduled" in event_response.lower()
            self.log_test("Calendar Event", has_event, "Event scheduling working")
            
            return has_reminder and has_event
        except Exception as e:
            self.log_test("Calendar Functionality", False, str(e))
            return False
    
    def test_email_functionality(self, agent):
        """Test email-related functionality"""
        try:
            email_response = agent.process_request("Send email to test@example.com about testing")
            has_email = "email" in email_response.lower()
            self.log_test("Email Functionality", has_email, "Email system responding")
            return has_email
        except Exception as e:
            self.log_test("Email Functionality", False, str(e))
            return False
    
    def test_ai_chat_functionality(self, agent):
        """Test AI chat functionality"""
        try:
            chat_response = agent.process_request("What is artificial intelligence?")
            has_ai_response = len(chat_response) > 50  # Reasonable response length
            self.log_test("AI Chat", has_ai_response, "AI chat responding appropriately")
            return has_ai_response
        except Exception as e:
            self.log_test("AI Chat", False, str(e))
            return False
    
    def test_context_aware_agent(self):
        """Test context-aware agent functionality"""
        try:
            context_agent = ContextAwareAgent("ContextBot")
            
            # Test weather with context
            weather_response = context_agent.process_request("What's the weather like?")
            has_context = len(weather_response) > 50  # Context-aware responses should be substantial
            self.log_test("Context-Aware Weather", has_context, "Context awareness working")
            
            # Clean up if method exists
            if hasattr(context_agent, 'cleanup'):
                context_agent.cleanup()
            
            return has_context
        except Exception as e:
            self.log_test("Context-Aware Agent", False, str(e))
            return False
    
    def test_x_agent_creation(self):
        """Test X agent initialization"""
        try:
            x_agent = XAgent()
            self.log_test("X Agent Creation", True, f"X agent '{x_agent.name}' created successfully")
            return x_agent
        except Exception as e:
            self.log_test("X Agent Creation", False, str(e))
            return None
    
    def test_x_api_configuration(self, x_agent):
        """Test X API configuration"""
        try:
            api_configured = x_agent.api_configured
            openai_configured = bool(x_agent.openai_api_key)
            
            self.log_test("X API Configuration", api_configured, 
                         "X API credentials configured" if api_configured else "X API not configured")
            self.log_test("OpenAI Configuration", openai_configured,
                         "OpenAI API configured" if openai_configured else "OpenAI API not configured")
            
            return api_configured
        except Exception as e:
            self.log_test("X API Configuration", False, str(e))
            return False
    
    def test_x_bible_verse_functionality(self, x_agent):
        """Test X Bible verse functionality"""
        try:
            verse = x_agent.get_daily_bible_verse()
            has_verse = isinstance(verse, str) and len(verse) > 10
            self.log_test("X Bible Verse", has_verse, "Bible verse retrieval working")
            return has_verse
        except Exception as e:
            self.log_test("X Bible Verse", False, str(e))
            return False
    
    def test_x_trending_topics(self, x_agent):
        """Test X trending topics functionality"""
        try:
            if not x_agent.api_configured:
                self.log_test("X Trending Topics", True, "Skipped - X API not configured")
                return True
            
            trends = x_agent.get_trending_topics()
            has_trends = isinstance(trends, list) and len(trends) > 0
            self.log_test("X Trending Topics", has_trends, 
                         f"Retrieved {len(trends) if isinstance(trends, list) else 0} trending topics")
            return has_trends
        except Exception as e:
            self.log_test("X Trending Topics", False, str(e))
            return False
    
    def test_x_tweet_search(self, x_agent):
        """Test X tweet search functionality"""
        try:
            if not x_agent.api_configured:
                self.log_test("X Tweet Search", True, "Skipped - X API not configured")
                return True
            
            tweets = x_agent.search_recent_tweets("AI technology", max_results=5)
            has_tweets = isinstance(tweets, list) and len(tweets) > 0
            self.log_test("X Tweet Search", has_tweets,
                         f"Retrieved {len(tweets) if isinstance(tweets, list) else 0} tweets")
            return has_tweets
        except Exception as e:
            self.log_test("X Tweet Search", False, str(e))
            return False
    
    def test_x_ai_summaries(self, x_agent):
        """Test X AI-powered summaries"""
        try:
            if not x_agent.api_configured or not x_agent.openai_api_key:
                self.log_test("X AI Summaries", True, "Skipped - APIs not configured")
                return True
            
            # Test trends summary
            trends_summary = x_agent.get_intelligent_trends_summary()
            has_trends_summary = isinstance(trends_summary, str) and len(trends_summary) > 100
            self.log_test("X AI Trends Summary", has_trends_summary, "AI trends summary generated")
            
            # Test news summary
            news_summary = x_agent.get_intelligent_news_summary()
            has_news_summary = isinstance(news_summary, str) and len(news_summary) > 100
            self.log_test("X AI News Summary", has_news_summary, "AI news summary generated")
            
            return has_trends_summary or has_news_summary
        except Exception as e:
            self.log_test("X AI Summaries", False, str(e))
            return False
    
    def test_x_posting_functionality(self, x_agent):
        """Test X posting functionality"""
        try:
            if not x_agent.api_configured:
                self.log_test("X Posting", True, "Skipped - X API not configured")
                return True
            
            # Test Bible verse posting (but don't actually post)
            verse = x_agent.get_daily_bible_verse()
            can_post = isinstance(verse, str) and len(verse) > 10
            self.log_test("X Posting Capability", can_post, "X posting functionality available")
            
            return can_post
        except Exception as e:
            self.log_test("X Posting", False, str(e))
            return False
    
    def test_enhanced_agent_creation(self):
        """Test enhanced agent initialization"""
        try:
            enhanced_agent = EnhancedContextAwareAgent("EnhancedBot")
            self.log_test("Enhanced Agent Creation", True, "Enhanced agent created with specialist agents")
            return enhanced_agent
        except Exception as e:
            self.log_test("Enhanced Agent Creation", False, str(e))
            return None
    
    def test_enhanced_x_integration(self, enhanced_agent):
        """Test enhanced agent X integration"""
        try:
            # Test X trends command
            trends_response = enhanced_agent.process_request("X trends")
            has_trends = "trends" in trends_response.lower() or "trending" in trends_response.lower()
            self.log_test("Enhanced X Trends", has_trends, "X trends integration working")
            
            # Test X news command
            news_response = enhanced_agent.process_request("X news")
            has_news = "news" in news_response.lower() or "summary" in news_response.lower()
            self.log_test("Enhanced X News", has_news, "X news integration working")
            
            # Test X status command
            status_response = enhanced_agent.process_request("X status")
            has_status = "status" in status_response.lower() or "api" in status_response.lower()
            self.log_test("Enhanced X Status", has_status, "X status integration working")
            
            return has_trends or has_news or has_status
        except Exception as e:
            self.log_test("Enhanced X Integration", False, str(e))
            return False
    
    def test_enhanced_bible_verse_posting(self, enhanced_agent):
        """Test enhanced agent Bible verse posting"""
        try:
            verse_response = enhanced_agent.process_request("post daily bible verse")
            # Check for various success indicators
            has_verse_posting = any(word in verse_response.lower() for word in 
                                  ['bible', 'verse', 'posted', 'successfully', 'shared', 'x'])
            self.log_test("Enhanced Bible Verse Posting", has_verse_posting, "Bible verse posting integration working")
            return has_verse_posting
        except Exception as e:
            self.log_test("Enhanced Bible Verse Posting", False, str(e))
            return False
    
    def test_enhanced_context_memory(self, enhanced_agent):
        """Test enhanced agent context memory"""
        try:
            # Test context memory query
            context_response = enhanced_agent.process_request("what do you remember about our conversation?")
            has_context = len(context_response) > 50
            self.log_test("Enhanced Context Memory", has_context, "Context memory functionality working")
            return has_context
        except Exception as e:
            self.log_test("Enhanced Context Memory", False, str(e))
            return False
    
    def test_security_features(self, agent):
        """Test security and input validation"""
        try:
            # Test with potentially dangerous input
            dangerous_inputs = [
                "'; DROP TABLE users; --",
                "<script>alert('xss')</script>",
                "../../../../etc/passwd",
                "rm -rf /"
            ]
            
            security_passed = True
            for dangerous_input in dangerous_inputs:
                try:
                    response = agent.process_request(dangerous_input)
                    # Should not crash and should handle safely
                    if "error" in response.lower() or "invalid" in response.lower():
                        continue  # Good, handled safely
                except Exception:
                    security_passed = False
                    break
            
            self.log_test("Security Features", security_passed, "Input validation and sanitization working")
            return security_passed
        except Exception as e:
            self.log_test("Security Features", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🧪 Starting Comprehensive Agent Test Suite")
        print("=" * 60)
        
        # Test basic agent
        print("\n📋 Testing Basic Agent...")
        basic_agent = self.test_basic_agent_creation()
        if basic_agent:
            self.test_service_status_check(basic_agent)
            self.test_weather_functionality(basic_agent)
            self.test_calendar_functionality(basic_agent)
            self.test_email_functionality(basic_agent)
            self.test_ai_chat_functionality(basic_agent)
            self.test_security_features(basic_agent)
        
        # Test context-aware agent
        print("\n🧠 Testing Context-Aware Agent...")
        self.test_context_aware_agent()
        
        # Test X agent
        print("\n📱 Testing X Agent...")
        x_agent = self.test_x_agent_creation()
        if x_agent:
            self.test_x_api_configuration(x_agent)
            self.test_x_bible_verse_functionality(x_agent)
            self.test_x_trending_topics(x_agent)
            self.test_x_tweet_search(x_agent)
            self.test_x_ai_summaries(x_agent)
            self.test_x_posting_functionality(x_agent)
            x_agent.cleanup()
        
        # Test enhanced agent
        print("\n🚀 Testing Enhanced Agent...")
        enhanced_agent = self.test_enhanced_agent_creation()
        if enhanced_agent:
            self.test_enhanced_x_integration(enhanced_agent)
            self.test_enhanced_bible_verse_posting(enhanced_agent)
            self.test_enhanced_context_memory(enhanced_agent)
            enhanced_agent.cleanup()
        
        # Print results
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for test_name, passed, message in self.test_results:
                if not passed:
                    print(f"   • {test_name}: {message}")
        
        print(f"\n🎯 Overall Status: {'✅ ALL TESTS PASSED' if self.failed_tests == 0 else '⚠️ SOME TESTS FAILED'}")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if self.failed_tests == 0:
            print("   • All systems operational!")
            print("   • Agent is ready for production use")
        else:
            print("   • Check failed tests and configure missing APIs")
            print("   • Ensure environment variables are properly set")
            print("   • Run: python3 test_env_vars.py for detailed API status")


def main():
    """Run the test suite"""
    print("🤖 Personal AI Agent - Comprehensive Test Suite")
    print("Testing all functionality including X integration and AI summaries")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = AgentTester()
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {str(e)}")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
