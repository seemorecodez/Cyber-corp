import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
import asyncio
import uuid
from typing import Dict, Optional
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class AIAgent:
    """Individual AI Agent with specific specialization"""
    
    def __init__(self, agent_id: str, name: str, agent_type: str, 
                 model_provider: str, model_name: str, specialization: list):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.model_provider = model_provider
        self.model_name = model_name
        self.specialization = specialization
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        
        # Define system prompts based on agent type
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        prompts = {
            "Security Analyst": (
                "You are Sentinel, an expert AI Security Analyst specializing in threat detection, "
                "risk assessment, and SIEM analysis. You analyze security vulnerabilities, identify threats, "
                "and provide actionable security recommendations. Be precise, thorough, and security-focused."
            ),
            "Penetration Tester": (
                "You are Phoenix, an elite AI Penetration Tester specializing in vulnerability testing, "
                "OWASP Top 10, network pentesting, and security exploitation. You find security flaws "
                "and provide detailed remediation steps. Be thorough and methodical."
            ),
            "Cryptography Expert": (
                "You are Cipher, a master AI Cryptography Expert specializing in encryption, "
                "key management, and blockchain security. You design secure cryptographic systems "
                "and ensure data protection. Be mathematically precise and security-conscious."
            ),
            "Software Developer": (
                "You are Architect, an expert AI Software Developer specializing in full-stack development, "
                "cloud architecture, and API design. You write clean, efficient, scalable code and "
                "follow best practices. Be practical and solution-oriented."
            ),
            "Code Reviewer": (
                "You are Validator, a meticulous AI Code Reviewer specializing in static analysis, "
                "code quality, and security audits. You review code for bugs, security issues, "
                "and best practices. Be detailed and constructive."
            ),
            "Compliance Expert": (
                "You are Guardian, an AI Compliance Expert specializing in GDPR, HIPAA, SOC 2, "
                "and ISO 27001. You ensure regulatory compliance and generate documentation. "
                "Be thorough, accurate, and regulation-focused."
            )
        }
        return prompts.get(self.agent_type, "You are a helpful AI assistant.")
    
    async def chat(self, message: str, session_id: Optional[str] = None) -> str:
        """Send a message to this agent and get response"""
        try:
            if not session_id:
                session_id = str(uuid.uuid4())
            
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=self.system_prompt
            ).with_model(self.model_provider, self.model_name)
            
            user_message = UserMessage(text=message)
            response = await chat.send_message(user_message)
            
            return response
        except Exception as e:
            logger.error(f"Error in agent {self.name} chat: {str(e)}")
            return f"Error processing request: {str(e)}"
    
    async def process_task(self, task_title: str, task_description: str) -> str:
        """Process a task and return results"""
        prompt = f"""Task: {task_title}

Description: {task_description}

Please analyze this task based on your expertise as a {self.agent_type} and provide:
1. Your analysis
2. Recommended approach
3. Key findings or deliverables
4. Any risks or considerations

Provide a comprehensive but concise response."""
        
        return await self.chat(prompt)


class HiveMindOrchestrator:
    """Orchestrates multiple AI agents working together"""
    
    def __init__(self):
        self.agents: Dict[str, AIAgent] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize the 6 specialized agents"""
        agent_configs = [
            {
                "agent_id": "agent-1",
                "name": "Sentinel",
                "type": "Security Analyst",
                "provider": "openai",
                "model": "gpt-5",
                "specialization": ["Threat Detection", "Risk Assessment", "SIEM Analysis"]
            },
            {
                "agent_id": "agent-2",
                "name": "Phoenix",
                "type": "Penetration Tester",
                "provider": "anthropic",
                "model": "claude-4-sonnet-20250514",
                "specialization": ["Web App Testing", "Network Pentesting", "OWASP Top 10"]
            },
            {
                "agent_id": "agent-3",
                "name": "Cipher",
                "type": "Cryptography Expert",
                "provider": "gemini",
                "model": "gemini-2.5-pro",
                "specialization": ["Encryption", "Key Management", "Blockchain Security"]
            },
            {
                "agent_id": "agent-4",
                "name": "Architect",
                "type": "Software Developer",
                "provider": "openai",
                "model": "gpt-5",
                "specialization": ["Full-Stack Dev", "Cloud Architecture", "API Design"]
            },
            {
                "agent_id": "agent-5",
                "name": "Validator",
                "type": "Code Reviewer",
                "provider": "anthropic",
                "model": "claude-4-sonnet-20250514",
                "specialization": ["Static Analysis", "Code Quality", "Security Audit"]
            },
            {
                "agent_id": "agent-6",
                "name": "Guardian",
                "type": "Compliance Expert",
                "provider": "gemini",
                "model": "gemini-2.5-pro",
                "specialization": ["GDPR", "HIPAA", "SOC 2", "ISO 27001"]
            }
        ]
        
        for config in agent_configs:
            agent = AIAgent(
                agent_id=config["agent_id"],
                name=config["name"],
                agent_type=config["type"],
                model_provider=config["provider"],
                model_name=config["model"],
                specialization=config["specialization"]
            )
            self.agents[config["agent_id"]] = agent
    
    def get_agent(self, agent_id: str) -> Optional[AIAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> Dict[str, AIAgent]:
        """Get all agents"""
        return self.agents
    
    async def broadcast_to_hive(self, message: str) -> dict:
        """Broadcast message to all agents and get collaborative response"""
        responses = {}
        
        # Select primary agent based on message content
        primary_agent_id = self._select_primary_agent(message)
        primary_agent = self.agents[primary_agent_id]
        
        # Get primary response
        primary_response = await primary_agent.chat(message)
        responses[primary_agent.name] = primary_response
        
        return {
            "primary_agent": primary_agent.name,
            "primary_response": primary_response,
            "all_responses": responses
        }
    
    def _select_primary_agent(self, message: str) -> str:
        """Select best agent based on message content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["security", "threat", "vulnerability", "attack"]):
            return "agent-1"  # Sentinel
        elif any(word in message_lower for word in ["code", "develop", "build", "implement"]):
            return "agent-4"  # Architect
        elif any(word in message_lower for word in ["review", "audit", "check"]):
            return "agent-5"  # Validator
        elif any(word in message_lower for word in ["compliance", "regulation", "gdpr", "hipaa"]):
            return "agent-6"  # Guardian
        elif any(word in message_lower for word in ["encrypt", "crypto", "security key"]):
            return "agent-3"  # Cipher
        else:
            return "agent-1"  # Default to Sentinel

# Global orchestrator instance
orchestrator = HiveMindOrchestrator()
