#!/usr/bin/env python3
"""
Quick Start Script for Intelligent AI Agent
Provides easy setup and launch options
"""

import os
import sys
import subprocess

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🤖 {title}")
    print("=" * 60)

def check_dependencies():
    """Check if required packages are installed"""
    python_exec = get_python_executable()
    
    # If we're using the virtual environment, check dependencies there
    if python_exec.startswith('venv'):
        try:
            result = subprocess.run([python_exec, '-c', 'import openai, requests; print("OK")'], 
                                  capture_output=True, text=True)
            return result.returncode == 0 and 'OK' in result.stdout
        except:
            return False
    else:
        # Fall back to checking in current process
        try:
            import openai
            import requests
            return True
        except ImportError:
            return False

def setup_environment():
    """Set up the environment"""
    print_header("ENVIRONMENT SETUP")
    
    # Check if virtual environment exists and is properly configured
    if not os.path.exists('venv') or not get_python_executable().startswith('venv'):
        print("📦 Creating virtual environment...")
        # Remove existing venv if it's broken
        if os.path.exists('venv'):
            import shutil
            shutil.rmtree('venv')
        
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        print("✅ Virtual environment created")
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("📥 Installing dependencies...")
        python_exec = get_python_executable()
        pip_exec = python_exec.replace('python', 'pip').replace('.exe', '.exe' if python_exec.endswith('.exe') else '')
        
        # Try to use the virtual environment pip, fall back to system pip
        try:
            subprocess.run([pip_exec, 'install', '-r', 'requirements.txt'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Virtual environment pip not found, using system pip...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        print("✅ Dependencies installed")
    
    # Show environment variable setup instructions
    print("\n⚙️  Environment Variable Configuration")
    print("To enable full functionality, export these environment variables:")
    print("\n# OpenAI API Key (required for AI features)")
    print('export OPENAI_API_KEY="your-openai-key-here"')
    print("\n# Weather API Key (optional - for real weather data)")
    print('export WEATHER_API_KEY="your-weather-key-here"')
    print("\n# Gmail Configuration (optional - for email features)")
    print('export GMAIL_EMAIL="your-email@gmail.com"')
    print('export GMAIL_APP_PASSWORD="your-app-password-here"')
    print("\n# Default Settings")
    print('export DEFAULT_CITY="New York"')
    print('export DEFAULT_WHATSAPP_CONTACT="Family"')
    print("\n💡 Add these to your ~/.bashrc or ~/.zshrc for persistence")
    
    print("\n🎉 Environment setup complete!")

def get_python_executable():
    """Get the appropriate Python executable path"""
    # Try to find the virtual environment Python executable
    venv_paths = [
        'venv/bin/python',      # Unix/Linux/Mac
        'venv/bin/python3',     # Unix/Linux/Mac with python3
        'venv/Scripts/python.exe',  # Windows
        'venv/Scripts/python3.exe'  # Windows with python3
    ]
    
    for path in venv_paths:
        if os.path.exists(path):
            return path
    
    # Fall back to system Python
    return sys.executable

def run_tests():
    """Run the test suite"""
    print_header("RUNNING TESTS")
    
    python_exec = get_python_executable()
    subprocess.run([python_exec, 'test_agent.py'])

def run_basic_agent():
    """Run the basic agent"""
    print_header("STARTING BASIC AGENT")
    
    python_exec = get_python_executable()
    subprocess.run([python_exec, 'basic_agent.py'])

def run_context_agent():
    """Run the context-aware agent"""
    print_header("STARTING CONTEXT-AWARE AGENT")
    
    python_exec = get_python_executable()
    subprocess.run([python_exec, 'context_aware_agent.py'])

def run_demo():
    """Run the interactive demo"""
    print_header("STARTING INTERACTIVE DEMO")
    
    python_exec = get_python_executable()
    subprocess.run([python_exec, 'demo_agent.py'])

def run_enhanced_agent():
    """Run the enhanced context-aware agent with X integration"""
    print_header("STARTING ENHANCED CONTEXT-AWARE AGENT")
    
    python_exec = get_python_executable()
    subprocess.run([python_exec, 'enhanced_context_aware_agent.py'])

def show_status():
    """Show current setup status"""
    print_header("SETUP STATUS")
    
    # Check virtual environment
    python_exec = get_python_executable()
    venv_active = python_exec.startswith('venv')
    print(f"Virtual Environment: {'✅ Active' if venv_active else '❌ Not active (using system Python)'}")
    print(f"Python Executable: {python_exec}")
    
    # Check dependencies
    deps_installed = check_dependencies()
    print(f"Dependencies: {'✅ Installed' if deps_installed else '❌ Not installed'}")
    
    # Check environment variables
    openai_key = os.getenv('OPENAI_API_KEY')
    weather_key = os.getenv('WEATHER_API_KEY')
    gmail_email = os.getenv('GMAIL_EMAIL')
    
    print(f"OpenAI API Key: {'✅ Configured' if openai_key and not openai_key.startswith('your-') else '❌ Not configured'}")
    print(f"Weather API Key: {'✅ Configured' if weather_key and not weather_key.startswith('your-') else '❌ Not configured'}")
    print(f"Gmail Credentials: {'✅ Configured' if gmail_email and not gmail_email.startswith('your-') else '❌ Not configured'}")
    
    print("\n💡 Run 'python run.py setup' to see configuration instructions")

def main():
    """Main menu"""
    print("🤖 Intelligent AI Agent - Quick Start")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'setup':
            setup_environment()
        elif command == 'test':
            run_tests()
        elif command == 'basic':
            run_basic_agent()
        elif command == 'context':
            run_context_agent()
        elif command == 'enhanced':
            run_enhanced_agent()
        elif command == 'demo':
            run_demo()
        elif command == 'status':
            show_status()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: setup, test, basic, context, enhanced, demo, status")
    else:
        # Interactive menu
        while True:
            print("\n" + "=" * 60)
            print("🎯 QUICK START MENU")
            print("=" * 60)
            print("1. Setup Environment")
            print("2. Check Status")
            print("3. Run Tests")
            print("4. Start Basic Agent")
            print("5. Start Context-Aware Agent")
            print("6. Start Enhanced Agent (X Integration + AI Summaries)")
            print("7. Run Interactive Demo")
            print("8. Exit")
            
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == '1':
                setup_environment()
            elif choice == '2':
                show_status()
            elif choice == '3':
                run_tests()
            elif choice == '4':
                run_basic_agent()
            elif choice == '5':
                run_context_agent()
            elif choice == '6':
                run_enhanced_agent()
            elif choice == '7':
                run_demo()
            elif choice == '8':
                print("\n👋 Thanks for trying the AI Agent!")
                break
            else:
                print("❌ Invalid choice. Please select 1-8.")

if __name__ == "__main__":
    main()
