#!/usr/bin/env python3
"""
Test environment variables and enhanced agent
"""

import os
import subprocess

def load_env_vars_from_zshrc():
    """Load environment variables from zshrc"""
    try:
        # Get environment variables from zshrc
        result = subprocess.run(['zsh', '-c', 'source ~/.zshrc && env'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            env_vars = {}
            for line in result.stdout.split('\n'):
                if '=' in line and (line.startswith('LINKEDIN_') or line.startswith('X_')):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
                    os.environ[key] = value
            
            return env_vars
        else:
            print(f"❌ Error loading zshrc: {result.stderr}")
            return {}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {}

def test_environment_variables():
    """Test if environment variables are properly set"""
    print("🔍 Environment Variables Status:")
    print("=" * 50)
    
    # LinkedIn variables
    linkedin_vars = {
        'LINKEDIN_CLIENT_ID': os.getenv('LINKEDIN_CLIENT_ID'),
        'LINKEDIN_CLIENT_SECRET': os.getenv('LINKEDIN_CLIENT_SECRET'), 
        'LINKEDIN_ACCESS_TOKEN': os.getenv('LINKEDIN_ACCESS_TOKEN')
    }
    
    print("🔗 LinkedIn Variables:")
    for key, value in linkedin_vars.items():
        status = "✅ Set" if value else "❌ Not set"
        preview = f" ({value[:20]}...)" if value and len(value) > 20 else f" ({value})" if value else ""
        print(f"  {key}: {status}{preview}")
    
    # X variables (check both naming conventions)
    x_vars = {
        'X_BEARER_TOKEN': os.getenv('X_BEARER_TOKEN'),
        'X_API_KEY': os.getenv('X_API_KEY') or os.getenv('X_CONSUMER_KEY'),
        'X_API_SECRET': os.getenv('X_API_SECRET') or os.getenv('X_CONSUMER_SECRET'),
        'X_ACCESS_TOKEN': os.getenv('X_ACCESS_TOKEN'),
        'X_ACCESS_TOKEN_SECRET': os.getenv('X_ACCESS_TOKEN_SECRET')
    }
    
    print("\n📱 X Variables:")
    for key, value in x_vars.items():
        status = "✅ Set" if value else "❌ Not set"
        preview = f" ({value[:20]}...)" if value and len(value) > 20 else f" ({value})" if value else ""
        print(f"  {key}: {status}{preview}")
    
    # Set the correct X variable names if using consumer key/secret
    if os.getenv('X_CONSUMER_KEY') and not os.getenv('X_API_KEY'):
        os.environ['X_API_KEY'] = os.getenv('X_CONSUMER_KEY')
        print("  ↳ Mapped X_CONSUMER_KEY to X_API_KEY")
    
    if os.getenv('X_CONSUMER_SECRET') and not os.getenv('X_API_SECRET'):
        os.environ['X_API_SECRET'] = os.getenv('X_CONSUMER_SECRET')
        print("  ↳ Mapped X_CONSUMER_SECRET to X_API_SECRET")
    
    return linkedin_vars, x_vars

def test_linkedin_agent():
    """Test LinkedIn agent functionality"""
    print("\n🔗 Testing LinkedIn Agent:")
    print("=" * 30)
    
    try:
        from linkedin_agent import LinkedInAgent
        agent = LinkedInAgent()
        
        print(f"API Configured: {agent.api_configured}")
        
        if agent.api_configured:
            # Test profile info
            profile = agent.get_profile_info()
            if isinstance(profile, dict):
                print(f"✅ Profile retrieved: {profile.get('name', 'Unknown')}")
            else:
                print(f"⚠️  Profile result: {str(profile)[:100]}...")
        
        agent.cleanup()
        return agent.api_configured
        
    except Exception as e:
        print(f"❌ LinkedIn agent error: {str(e)}")
        return False

def test_x_agent():
    """Test X agent functionality"""
    print("\n📱 Testing X Agent:")
    print("=" * 20)
    
    try:
        from x_agent import XAgent
        agent = XAgent()
        
        print(f"API Configured: {agent.api_configured}")
        
        if agent.api_configured:
            # Test Bible verse (doesn't require API)
            verse = agent.get_daily_bible_verse()
            print(f"✅ Bible verse: {verse[:50]}...")
        else:
            # Still test Bible verse functionality
            verse = agent.get_daily_bible_verse()
            print(f"📖 Bible verse (no API): {verse[:50]}...")
        
        agent.cleanup()
        return agent.api_configured
        
    except Exception as e:
        print(f"❌ X agent error: {str(e)}")
        return False

def test_enhanced_agent():
    """Test enhanced agent with social media integration"""
    print("\n🚀 Testing Enhanced Agent:")
    print("=" * 30)
    
    try:
        from enhanced_context_aware_agent import EnhancedContextAwareAgent
        agent = EnhancedContextAwareAgent('TestAgent')
        
        print("✅ Enhanced agent created successfully!")
        
        # Test LinkedIn integration
        print("\n🔗 Testing LinkedIn integration...")
        result = agent.process_request('linkedin summary')
        print(f"LinkedIn result: {result[:150]}...")
        
        # Test X integration
        print("\n📱 Testing X integration...")
        result = agent.process_request('x status')
        print(f"X result: {result[:150]}...")
        
        # Test Bible verse posting
        print("\n📖 Testing Bible verse posting...")
        result = agent.process_request('post daily bible verse')
        print(f"Bible verse result: {result[:150]}...")
        
        agent.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Enhanced agent error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing LinkedIn and X Environment Variables")
    print("=" * 60)
    
    # Load environment variables from zshrc
    print("📋 Loading environment variables from ~/.zshrc...")
    env_vars = load_env_vars_from_zshrc()
    if env_vars:
        print(f"✅ Loaded {len(env_vars)} environment variables")
    else:
        print("⚠️  Using existing environment variables")
    
    # Test environment variables
    linkedin_vars, x_vars = test_environment_variables()
    
    # Test individual agents
    linkedin_working = test_linkedin_agent()
    x_working = test_x_agent()
    
    # Test enhanced agent
    enhanced_working = test_enhanced_agent()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"🔗 LinkedIn Agent: {'✅ Working' if linkedin_working else '❌ Not configured'}")
    print(f"📱 X Agent: {'✅ Working' if x_working else '❌ Not configured'}")
    print(f"🚀 Enhanced Agent: {'✅ Working' if enhanced_working else '❌ Issues found'}")
    
    if not linkedin_working:
        print("\n💡 LinkedIn Setup:")
        print("   1. Ensure LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET are set")
        print("   2. Run: python linkedin_oauth.py to get access token")
    
    if not x_working:
        print("\n💡 X Setup:")
        print("   1. Ensure all X_* variables are set in ~/.zshrc")
        print("   2. Check X Developer Portal for correct API keys")

if __name__ == "__main__":
    main()
