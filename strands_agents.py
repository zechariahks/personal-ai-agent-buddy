#!/usr/bin/env python3
"""
Strands Agents SDK - A simplified framework for building intelligent agents
Inspired by modern agent patterns and best practices
"""

import os
import json
import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging - set to WARNING to reduce verbosity
# Users can override this by setting STRANDS_LOG_LEVEL environment variable
log_level = os.getenv('STRANDS_LOG_LEVEL', 'WARNING').upper()
logging.basicConfig(level=getattr(logging, log_level, logging.WARNING))
logger = logging.getLogger(__name__)

def set_log_level(level: str):
    """Set the logging level for Strands Agents SDK
    
    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    """
    logger.setLevel(getattr(logging, level.upper(), logging.WARNING))

def enable_verbose_logging():
    """Enable verbose logging (INFO level)"""
    set_log_level('INFO')

def disable_verbose_logging():
    """Disable verbose logging (WARNING level)"""
    set_log_level('WARNING')

def enable_debug_logging():
    """Enable debug logging (DEBUG level)"""
    set_log_level('DEBUG')

class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Standard message format for agent communication"""
    sender: str
    recipient: str
    content: str
    message_type: str = "text"
    timestamp: str = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class AgentResponse:
    """Standard response format for agent actions"""
    success: bool
    message: str
    data: Any = None
    error: str = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class AgentCapability(ABC):
    """Base class for agent capabilities"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> AgentResponse:
        """Execute the capability with given parameters"""
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate input parameters"""
        return True

class BaseAgent(ABC):
    """Base agent class with core functionality"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.capabilities: Dict[str, AgentCapability] = {}
        self.memory: Dict[str, Any] = {}
        self.message_history: List[AgentMessage] = []
        self.created_at = datetime.now()
        
        logger.info(f"🤖 Agent '{name}' initialized")
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to the agent"""
        self.capabilities[capability.name] = capability
        logger.info(f"✅ Added capability '{capability.name}' to agent '{self.name}'")
    
    def remove_capability(self, capability_name: str):
        """Remove a capability from the agent"""
        if capability_name in self.capabilities:
            del self.capabilities[capability_name]
            logger.info(f"❌ Removed capability '{capability_name}' from agent '{self.name}'")
    
    def list_capabilities(self) -> List[str]:
        """List all available capabilities"""
        return list(self.capabilities.keys())
    
    def execute_capability(self, capability_name: str, parameters: Dict[str, Any] = None) -> AgentResponse:
        """Execute a specific capability"""
        if parameters is None:
            parameters = {}
        
        if capability_name not in self.capabilities:
            return AgentResponse(
                success=False,
                message=f"Capability '{capability_name}' not found",
                error="CAPABILITY_NOT_FOUND"
            )
        
        capability = self.capabilities[capability_name]
        
        if not capability.enabled:
            return AgentResponse(
                success=False,
                message=f"Capability '{capability_name}' is disabled",
                error="CAPABILITY_DISABLED"
            )
        
        try:
            self.status = AgentStatus.EXECUTING
            logger.info(f"🔄 Executing capability '{capability_name}' for agent '{self.name}'")
            
            result = capability.execute(parameters)
            
            self.status = AgentStatus.IDLE
            logger.info(f"✅ Capability '{capability_name}' executed successfully")
            
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            error_msg = f"Error executing capability '{capability_name}': {str(e)}"
            logger.error(error_msg)
            
            return AgentResponse(
                success=False,
                message=error_msg,
                error="EXECUTION_ERROR"
            )
    
    def send_message(self, recipient: str, content: str, message_type: str = "text") -> AgentMessage:
        """Send a message to another agent or user"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            content=content,
            message_type=message_type
        )
        
        self.message_history.append(message)
        logger.info(f"📤 Message sent from '{self.name}' to '{recipient}'")
        
        return message
    
    def receive_message(self, message: AgentMessage):
        """Receive and process a message"""
        self.message_history.append(message)
        logger.info(f"📥 Message received by '{self.name}' from '{message.sender}'")
        
        # Process the message (can be overridden by subclasses)
        self.process_message(message)
    
    def process_message(self, message: AgentMessage):
        """Process received message (override in subclasses)"""
        pass
    
    def store_memory(self, key: str, value: Any):
        """Store information in agent memory"""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        logger.debug(f"💾 Stored memory '{key}' for agent '{self.name}'")
    
    def retrieve_memory(self, key: str) -> Any:
        """Retrieve information from agent memory"""
        if key in self.memory:
            return self.memory[key]["value"]
        return None
    
    def clear_memory(self, key: str = None):
        """Clear agent memory"""
        if key:
            if key in self.memory:
                del self.memory[key]
                logger.info(f"🗑️ Cleared memory '{key}' for agent '{self.name}'")
        else:
            self.memory.clear()
            logger.info(f"🗑️ Cleared all memory for agent '{self.name}'")
    
    @abstractmethod
    def think(self, input_text: str) -> str:
        """Process input and generate response (must be implemented by subclasses)"""
        pass

class AgentOrchestrator:
    """Orchestrates multiple agents and manages their interactions"""
    
    def __init__(self, name: str = "Orchestrator"):
        self.name = name
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[AgentMessage] = []
        self.running = False
        
        logger.info(f"🎭 Agent Orchestrator '{name}' initialized")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        logger.info(f"📝 Registered agent '{agent.name}' with orchestrator")
    
    def unregister_agent(self, agent_name: str):
        """Unregister an agent from the orchestrator"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            logger.info(f"📝 Unregistered agent '{agent_name}' from orchestrator")
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name"""
        return self.agents.get(agent_name)
    
    def list_agents(self) -> List[str]:
        """List all registered agents"""
        return list(self.agents.keys())
    
    def route_message(self, message: AgentMessage):
        """Route a message to the appropriate agent"""
        if message.recipient in self.agents:
            self.agents[message.recipient].receive_message(message)
        else:
            logger.warning(f"⚠️ Agent '{message.recipient}' not found for message routing")
    
    def broadcast_message(self, sender: str, content: str, message_type: str = "broadcast"):
        """Broadcast a message to all agents"""
        for agent_name, agent in self.agents.items():
            if agent_name != sender:
                message = AgentMessage(
                    sender=sender,
                    recipient=agent_name,
                    content=content,
                    message_type=message_type
                )
                agent.receive_message(message)
        
        logger.info(f"📢 Broadcast message sent from '{sender}' to all agents")
    
    def execute_workflow(self, workflow: List[Dict[str, Any]]) -> List[AgentResponse]:
        """Execute a workflow of agent actions"""
        results = []
        
        for step in workflow:
            agent_name = step.get("agent")
            capability = step.get("capability")
            parameters = step.get("parameters", {})
            
            if agent_name not in self.agents:
                results.append(AgentResponse(
                    success=False,
                    message=f"Agent '{agent_name}' not found",
                    error="AGENT_NOT_FOUND"
                ))
                continue
            
            agent = self.agents[agent_name]
            result = agent.execute_capability(capability, parameters)
            results.append(result)
            
            # Stop workflow if step fails and no continue_on_error flag
            if not result.success and not step.get("continue_on_error", False):
                logger.warning(f"⚠️ Workflow stopped due to failed step: {result.message}")
                break
        
        return results

class SmartAgent(BaseAgent):
    """Enhanced agent with AI capabilities"""
    
    def __init__(self, name: str, description: str = "", ai_model: str = "gpt-3.5-turbo"):
        super().__init__(name, description)
        self.ai_model = ai_model
        self.context_window = []
        self.max_context_length = 10
    
    def think(self, input_text: str) -> str:
        """Use AI to process input and generate intelligent responses"""
        try:
            import openai
            
            # Check if OpenAI API key is available
            if not os.getenv("OPENAI_API_KEY"):
                return self._fallback_response(input_text)
            
            # Build context from recent messages
            context = self._build_context()
            
            # Create the prompt
            system_prompt = f"""You are {self.name}, an intelligent AI agent.
Description: {self.description}
Available capabilities: {', '.join(self.list_capabilities())}

Respond naturally and helpfully. If asked to perform actions, suggest using your capabilities."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                *context,
                {"role": "user", "content": input_text}
            ]
            
            # Make API call
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.ai_model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Update context window
            self._update_context(input_text, ai_response)
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI thinking error: {str(e)}")
            return self._fallback_response(input_text)
    
    def _build_context(self) -> List[Dict[str, str]]:
        """Build context from recent conversation"""
        context = []
        for entry in self.context_window[-self.max_context_length:]:
            context.extend([
                {"role": "user", "content": entry["user"]},
                {"role": "assistant", "content": entry["assistant"]}
            ])
        return context
    
    def _update_context(self, user_input: str, ai_response: str):
        """Update the context window"""
        self.context_window.append({
            "user": user_input,
            "assistant": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent context
        if len(self.context_window) > self.max_context_length:
            self.context_window = self.context_window[-self.max_context_length:]
    
    def _fallback_response(self, input_text: str) -> str:
        """Provide fallback response when AI is not available"""
        responses = [
            f"I understand you said: '{input_text}'. How can I help you with my available capabilities?",
            f"I received your message about '{input_text}'. Let me know which of my capabilities you'd like to use.",
            f"Thanks for your input: '{input_text}'. I'm ready to assist you with my functions."
        ]
        
        import random
        return random.choice(responses)

# Utility functions
def create_agent(agent_type: str = "smart", name: str = "Agent", **kwargs) -> BaseAgent:
    """Factory function to create agents"""
    if agent_type == "smart":
        return SmartAgent(name, **kwargs)
    else:
        # For basic agent, we need a concrete implementation
        class BasicAgentImpl(BaseAgent):
            def think(self, input_text: str) -> str:
                return f"I received: {input_text}. I'm a basic agent with capabilities: {', '.join(self.list_capabilities())}"
        
        return BasicAgentImpl(name, **kwargs)

def create_orchestrator(name: str = "MainOrchestrator") -> AgentOrchestrator:
    """Factory function to create orchestrator"""
    return AgentOrchestrator(name)

# Export main classes and functions
__all__ = [
    'BaseAgent', 'SmartAgent', 'AgentCapability', 'AgentOrchestrator',
    'AgentMessage', 'AgentResponse', 'AgentStatus',
    'create_agent', 'create_orchestrator',
    'set_log_level', 'enable_verbose_logging', 'disable_verbose_logging', 'enable_debug_logging'
]
