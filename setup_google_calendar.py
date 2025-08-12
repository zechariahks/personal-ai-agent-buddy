#!/usr/bin/env python3
"""
Google Calendar Setup Guide for AI Agent
Helps users set up Google Calendar integration step by step
"""

import os
import json

def check_credentials_file():
    """Check if credentials.json exists"""
    if os.path.exists('credentials.json'):
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
                if 'installed' in creds or 'web' in creds:
                    print("✅ credentials.json found and appears valid")
                    return True
                else:
                    print("❌ credentials.json found but format appears invalid")
                    return False
        except json.JSONDecodeError:
            print("❌ credentials.json found but contains invalid JSON")
            return False
    else:
        print("❌ credentials.json not found")
        return False

def check_token_file():
    """Check if token.pickle exists (authentication completed)"""
    if os.path.exists('token.pickle'):
        print("✅ token.pickle found - authentication previously completed")
        return True
    else:
        print("⚠️ token.pickle not found - authentication needed")
        return False

def provide_setup_instructions():
    """Provide detailed setup instructions"""
    print("\n📋 Google Calendar Integration Setup Guide:")
    print("=" * 60)
    
    print("\n1. 🌐 Go to Google Cloud Console:")
    print("   https://console.cloud.google.com/")
    
    print("\n2. 📁 Create or Select Project:")
    print("   • Click 'Select a project' dropdown")
    print("   • Create new project or select existing one")
    print("   • Name it something like 'AI Agent Calendar'")
    
    print("\n3. 🔧 Enable Google Calendar API:")
    print("   • Go to 'APIs & Services' > 'Library'")
    print("   • Search for 'Google Calendar API'")
    print("   • Click on it and press 'Enable'")
    
    print("\n4. 🔑 Create OAuth 2.0 Credentials:")
    print("   • Go to 'APIs & Services' > 'Credentials'")
    print("   • Click '+ CREATE CREDENTIALS'")
    print("   • Select 'OAuth client ID'")
    print("   • Choose 'Desktop application'")
    print("   • Name it 'AI Agent'")
    print("   • Click 'Create'")
    
    print("\n5. 📥 Download Credentials:")
    print("   • Click the download button (⬇️) next to your credential")
    print("   • Save the file as 'credentials.json'")
    print("   • Move it to this directory:")
    print(f"   {os.getcwd()}")
    
    print("\n6. 🔄 Run Setup:")
    print("   python3 setup_google_calendar.py")
    
    print("\n7. 🚀 Test Integration:")
    print("   python3 google_calendar_integration.py")

def test_calendar_integration():
    """Test if Google Calendar integration works"""
    try:
        from google_calendar_integration import GoogleCalendarManager
        
        print("\n🧪 Testing Google Calendar Integration:")
        print("=" * 50)
        
        calendar_manager = GoogleCalendarManager()
        
        if calendar_manager.is_configured():
            print("✅ Google Calendar integration working!")
            
            # Test listing events
            print("\n📋 Testing event listing...")
            events = calendar_manager.list_upcoming_events(3)
            print(events)
            
            return True
        else:
            print("❌ Google Calendar integration not working")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error testing integration: {e}")
        return False

def main():
    """Main setup function"""
    print("📅 Google Calendar Integration Setup")
    print("=" * 60)
    
    print("\n🔍 Checking current setup...")
    
    # Check credentials file
    has_credentials = check_credentials_file()
    
    # Check token file
    has_token = check_token_file()
    
    # Check dependencies
    try:
        import google.auth
        import googleapiclient.discovery
        print("✅ Google API dependencies installed")
        has_dependencies = True
    except ImportError:
        print("❌ Google API dependencies missing")
        print("💡 Run: pip install -r requirements.txt")
        has_dependencies = False
    
    print(f"\n📊 Setup Status:")
    print(f"• Dependencies: {'✅' if has_dependencies else '❌'}")
    print(f"• Credentials: {'✅' if has_credentials else '❌'}")
    print(f"• Authentication: {'✅' if has_token else '❌'}")
    
    if has_dependencies and has_credentials and has_token:
        print("\n🎉 Google Calendar integration appears to be set up!")
        
        # Test the integration
        if test_calendar_integration():
            print("\n✅ Setup complete! Your AI Agent can now use Google Calendar.")
            print("\n🚀 Try these commands in your AI Agent:")
            print("• 'Schedule meeting tomorrow at 2 PM'")
            print("• 'List my events'")
            print("• 'Calendar status'")
        else:
            print("\n⚠️ Setup appears complete but testing failed.")
            print("💡 Try running the agent and check for error messages.")
    
    elif has_dependencies and has_credentials and not has_token:
        print("\n🔐 Credentials found! Running authentication...")
        
        # Try to authenticate
        try:
            from google_calendar_integration import GoogleCalendarManager
            calendar_manager = GoogleCalendarManager()
            
            if calendar_manager.is_configured():
                print("✅ Authentication successful!")
                print("🎉 Google Calendar integration is now ready!")
            else:
                print("❌ Authentication failed")
                provide_setup_instructions()
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            provide_setup_instructions()
    
    else:
        print("\n❌ Setup incomplete.")
        provide_setup_instructions()
        
        if not has_dependencies:
            print(f"\n🔧 First, install dependencies:")
            print(f"   cd '{os.getcwd()}'")
            print(f"   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
