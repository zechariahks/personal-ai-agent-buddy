#!/usr/bin/env python3
"""
Example showing how to control logging in Strands Agents SDK
"""

from strands_agents import (
    create_agent, enable_verbose_logging, disable_verbose_logging, 
    enable_debug_logging, set_log_level
)
from agent_capabilities import WeatherCapability

def main():
    print("🔧 Strands Agents SDK Logging Control Example")
    print("=" * 50)
    
    # Default: Quiet mode (WARNING level)
    print("\n1. 📵 Default (Quiet) Mode:")
    agent = create_agent("smart", "QuietAgent")
    agent.add_capability(WeatherCapability())
    result = agent.execute_capability("weather", {"city": "London"})
    print(f"   Result: {result.success}")
    
    # Enable verbose logging
    print("\n2. 📢 Verbose Mode (INFO level):")
    enable_verbose_logging()
    agent2 = create_agent("smart", "VerboseAgent")
    agent2.add_capability(WeatherCapability())
    result2 = agent2.execute_capability("weather", {"city": "Tokyo"})
    print(f"   Result: {result2.success}")
    
    # Back to quiet mode
    print("\n3. 📵 Back to Quiet Mode:")
    disable_verbose_logging()
    result3 = agent.execute_capability("weather", {"city": "Paris"})
    print(f"   Result: {result3.success}")
    
    # Debug mode (very verbose)
    print("\n4. 🐛 Debug Mode (DEBUG level):")
    enable_debug_logging()
    result4 = agent.execute_capability("weather", {"city": "Berlin"})
    print(f"   Result: {result4.success}")
    
    # Custom level
    print("\n5. ⚙️ Custom Level (ERROR only):")
    set_log_level('ERROR')
    result5 = agent.execute_capability("weather", {"city": "Madrid"})
    print(f"   Result: {result5.success}")
    
    print("\n✅ Logging control demonstration complete!")

if __name__ == "__main__":
    main()
