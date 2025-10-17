from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import asyncio

from models import (
    Agent, Task, TaskCreate, HiveMessage, HiveBroadcast,
    Project, Activity, Certification, ChatMessage, ChatResponse
)
from agent_system import orchestrator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Helper function to clean MongoDB documents
def clean_mongo_doc(doc):
    """Remove MongoDB _id field from document"""
    if doc and '_id' in doc:
        doc.pop('_id')
    return doc

def clean_mongo_docs(docs):
    """Remove MongoDB _id field from list of documents"""
    return [clean_mongo_doc(doc) for doc in docs]

# Initialize default data
async def initialize_database():
    """Initialize database with default agents and data"""
    try:
        # Check if agents already exist
        existing_agents = await db.agents.count_documents({})
        if existing_agents == 0:
            # Initialize agents
            agents_data = [
                {
                    "agent_id": "agent-1",
                    "name": "Sentinel",
                    "type": "Security Analyst",
                    "status": "active",
                    "model_provider": "openai",
                    "model_name": "gpt-5",
                    "avatar": "SA",
                    "color": "from-blue-500 to-cyan-500",
                    "current_task_id": None,
                    "tasks_completed": 1247,
                    "success_rate": 98.5,
                    "specialization": ["Threat Detection", "Risk Assessment", "SIEM Analysis"],
                    "created_at": datetime.utcnow()
                },
                {
                    "agent_id": "agent-2",
                    "name": "Phoenix",
                    "type": "Penetration Tester",
                    "status": "active",
                    "model_provider": "anthropic",
                    "model_name": "claude-4-sonnet-20250514",
                    "avatar": "PT",
                    "color": "from-red-500 to-orange-500",
                    "current_task_id": None,
                    "tasks_completed": 892,
                    "success_rate": 96.2,
                    "specialization": ["Web App Testing", "Network Pentesting", "Social Engineering"],
                    "created_at": datetime.utcnow()
                },
                {
                    "agent_id": "agent-3",
                    "name": "Cipher",
                    "type": "Cryptography Expert",
                    "status": "active",
                    "model_provider": "gemini",
                    "model_name": "gemini-2.5-pro",
                    "avatar": "CE",
                    "color": "from-purple-500 to-pink-500",
                    "current_task_id": None,
                    "tasks_completed": 654,
                    "success_rate": 99.1,
                    "specialization": ["Encryption", "Key Management", "Blockchain Security"],
                    "created_at": datetime.utcnow()
                },
                {
                    "agent_id": "agent-4",
                    "name": "Architect",
                    "type": "Software Developer",
                    "status": "active",
                    "model_provider": "openai",
                    "model_name": "gpt-5",
                    "avatar": "SD",
                    "color": "from-green-500 to-emerald-500",
                    "current_task_id": None,
                    "tasks_completed": 2103,
                    "success_rate": 97.8,
                    "specialization": ["Full-Stack Dev", "Cloud Architecture", "API Design"],
                    "created_at": datetime.utcnow()
                },
                {
                    "agent_id": "agent-5",
                    "name": "Validator",
                    "type": "Code Reviewer",
                    "status": "active",
                    "model_provider": "anthropic",
                    "model_name": "claude-4-sonnet-20250514",
                    "avatar": "CR",
                    "color": "from-yellow-500 to-amber-500",
                    "current_task_id": None,
                    "tasks_completed": 1876,
                    "success_rate": 98.9,
                    "specialization": ["Static Analysis", "Code Quality", "Security Audit"],
                    "created_at": datetime.utcnow()
                },
                {
                    "agent_id": "agent-6",
                    "name": "Guardian",
                    "type": "Compliance Expert",
                    "status": "active",
                    "model_provider": "gemini",
                    "model_name": "gemini-2.5-pro",
                    "avatar": "CM",
                    "color": "from-indigo-500 to-blue-500",
                    "current_task_id": None,
                    "tasks_completed": 543,
                    "success_rate": 99.7,
                    "specialization": ["GDPR", "HIPAA", "SOC 2", "ISO 27001"],
                    "created_at": datetime.utcnow()
                }
            ]
            await db.agents.insert_many(agents_data)
            
            # Initialize certifications
            certifications_data = [
                {"name": "CISSP", "progress": 87, "status": "in_progress", "total_modules": 8, "completed_modules": 7, "last_updated": datetime.utcnow()},
                {"name": "CEH", "progress": 100, "status": "certified", "total_modules": 20, "completed_modules": 20, "last_updated": datetime.utcnow()},
                {"name": "OSCP", "progress": 62, "status": "in_progress", "total_modules": 12, "completed_modules": 7, "last_updated": datetime.utcnow()},
                {"name": "CISM", "progress": 100, "status": "certified", "total_modules": 4, "completed_modules": 4, "last_updated": datetime.utcnow()},
                {"name": "CompTIA Security+", "progress": 100, "status": "certified", "total_modules": 6, "completed_modules": 6, "last_updated": datetime.utcnow()},
                {"name": "AWS Security", "progress": 45, "status": "in_progress", "total_modules": 10, "completed_modules": 4, "last_updated": datetime.utcnow()}
            ]
            await db.certifications.insert_many(certifications_data)
            
            logging.info("Database initialized with default data")
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")

# Agent Endpoints
@api_router.get("/agents")
async def get_agents():
    """Get all AI agents with their current status"""
    agents = await db.agents.find().to_list(100)
    
    # Remove MongoDB _id field and add current task info
    result = []
    for agent in agents:
        agent.pop('_id', None)  # Remove _id
        if agent.get("current_task_id"):
            task = await db.tasks.find_one({"task_id": agent["current_task_id"]})
            agent["current_task"] = task.get("title") if task else "Processing task"
        else:
            # Set dynamic current task based on agent type
            task_map = {
                "Security Analyst": "Analyzing network traffic patterns",
                "Penetration Tester": "Running OWASP Top 10 vulnerability scan",
                "Cryptography Expert": "Implementing zero-knowledge proof protocol",
                "Software Developer": "Developing microservices architecture",
                "Code Reviewer": "Reviewing authentication module for vulnerabilities",
                "Compliance Expert": "Generating SOC 2 Type II documentation"
            }
            agent["current_task"] = task_map.get(agent.get("type"), "Idle")
        result.append(agent)
    
    return result

@api_router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent details"""
    agent = await db.agents.find_one({"agent_id": agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return clean_mongo_doc(agent)

@api_router.post("/agents/{agent_id}/chat")
async def chat_with_agent(agent_id: str, message: ChatMessage):
    """Chat with a specific AI agent"""
    agent_data = await db.agents.find_one({"agent_id": agent_id})
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    ai_agent = orchestrator.get_agent(agent_id)
    if not ai_agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        response = await ai_agent.chat(message.message, message.session_id)
        
        # Log activity
        activity = Activity(
            agent_id=agent_id,
            action=f"Responded to user query about: {message.message[:50]}...",
            activity_type="info"
        )
        await db.activities.insert_one(activity.dict())
        
        return ChatResponse(
            response=response,
            agent_name=agent_data["name"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Task Endpoints
@api_router.get("/tasks")
async def get_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None)
):
    """Get all tasks with optional filters"""
    query = {}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if agent_id:
        query["assigned_agent_id"] = agent_id
    
    tasks = await db.tasks.find(query).sort("created_at", -1).to_list(100)
    
    # Add agent names
    for task in tasks:
        if task.get("assigned_agent_id"):
            agent = await db.agents.find_one({"agent_id": task["assigned_agent_id"]})
            task["agent_name"] = agent.get("name") if agent else "Unknown"
    
    return tasks

@api_router.post("/tasks")
async def create_task(task: TaskCreate):
    """Create a new task and auto-assign to best agent"""
    # Select best agent based on task content
    task_lower = task.title.lower() + " " + task.description.lower()
    
    if any(word in task_lower for word in ["security", "threat", "vulnerability"]):
        agent_id = "agent-1"  # Sentinel
    elif any(word in task_lower for word in ["code", "develop", "build"]):
        agent_id = "agent-4"  # Architect
    elif any(word in task_lower for word in ["review", "audit"]):
        agent_id = "agent-5"  # Validator
    elif any(word in task_lower for word in ["compliance", "regulation"]):
        agent_id = "agent-6"  # Guardian
    else:
        agent_id = "agent-1"  # Default
    
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        assigned_agent_id=agent_id,
        status="in_progress",
        eta_minutes=120
    )
    
    await db.tasks.insert_one(new_task.dict())
    
    # Update agent status
    await db.agents.update_one(
        {"agent_id": agent_id},
        {"$set": {"current_task_id": new_task.task_id}}
    )
    
    # Start task processing in background
    asyncio.create_task(process_task_background(new_task.task_id, agent_id))
    
    return new_task

async def process_task_background(task_id: str, agent_id: str):
    """Background task processor"""
    try:
        task = await db.tasks.find_one({"task_id": task_id})
        if not task:
            return
        
        ai_agent = orchestrator.get_agent(agent_id)
        if not ai_agent:
            return
        
        # Update progress
        for progress in [25, 50, 75]:
            await asyncio.sleep(2)
            await db.tasks.update_one(
                {"task_id": task_id},
                {"$set": {"progress": progress}}
            )
        
        # Process task with AI
        result = await ai_agent.process_task(task["title"], task["description"])
        
        # Complete task
        await db.tasks.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "progress": 100,
                    "status": "completed",
                    "result": result,
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        # Update agent
        await db.agents.update_one(
            {"agent_id": agent_id},
            {
                "$set": {"current_task_id": None},
                "$inc": {"tasks_completed": 1}
            }
        )
        
        # Log activity
        activity = Activity(
            agent_id=agent_id,
            action=f"Completed task: {task['title']}",
            activity_type="success"
        )
        await db.activities.insert_one(activity.dict())
        
    except Exception as e:
        logging.error(f"Error processing task {task_id}: {str(e)}")
        await db.tasks.update_one(
            {"task_id": task_id},
            {"$set": {"status": "failed", "result": f"Error: {str(e)}"}}
        )

# Hive Mind Endpoints
@api_router.get("/hive/messages")
async def get_hive_messages(limit: int = Query(50)):
    """Get recent inter-agent messages"""
    messages = await db.hive_messages.find().sort("timestamp", -1).limit(limit).to_list(limit)
    
    # Add agent names
    for msg in messages:
        from_agent = await db.agents.find_one({"agent_id": msg["from_agent_id"]})
        msg["from_agent_name"] = from_agent.get("name") if from_agent else "System"
        
        if msg["to_agent_id"] == "all":
            msg["to_agent_name"] = "All"
        else:
            to_agent = await db.agents.find_one({"agent_id": msg["to_agent_id"]})
            msg["to_agent_name"] = to_agent.get("name") if to_agent else "Unknown"
    
    return list(reversed(messages))

@api_router.post("/hive/broadcast")
async def broadcast_to_hive(broadcast: HiveBroadcast):
    """User broadcasts message to hive mind"""
    try:
        result = await orchestrator.broadcast_to_hive(broadcast.message)
        
        # Save hive message
        hive_msg = HiveMessage(
            from_agent_id="system",
            to_agent_id="all",
            message=f"User query: {broadcast.message}",
            message_type="request"
        )
        await db.hive_messages.insert_one(hive_msg.dict())
        
        # Save agent response
        response_msg = HiveMessage(
            from_agent_id=result.get("primary_agent", "agent-1"),
            to_agent_id="system",
            message=result["primary_response"][:200] + "...",
            message_type="info"
        )
        await db.hive_messages.insert_one(response_msg.dict())
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Other Endpoints
@api_router.get("/activities")
async def get_activities(limit: int = Query(20)):
    """Get recent activities"""
    activities = await db.activities.find().sort("timestamp", -1).limit(limit).to_list(limit)
    
    # Add agent names
    for activity in activities:
        agent = await db.agents.find_one({"agent_id": activity["agent_id"]})
        activity["agent_name"] = agent.get("name") if agent else "Unknown"
    
    return activities

@api_router.get("/certifications")
async def get_certifications():
    """Get all certifications with progress"""
    certifications = await db.certifications.find().to_list(100)
    return certifications

@api_router.get("/metrics/security")
async def get_security_metrics():
    """Get security metrics dashboard data"""
    return {
        "vulnerabilitiesFound": 1247,
        "vulnerabilitiesFixed": 1198,
        "threatsBlocked": 8934,
        "uptime": 99.97,
        "avgResponseTime": "1.2s",
        "securityScore": 96
    }

@api_router.get("/metrics/development")
async def get_development_metrics():
    """Get development metrics dashboard data"""
    projects_count = await db.projects.count_documents({})
    return {
        "projectsCompleted": projects_count,
        "codeReviews": 432,
        "deploymentsToday": 23,
        "testCoverage": 94.5,
        "bugsFixed": 156,
        "performance": 98
    }

@api_router.get("/")
async def root():
    return {"message": "AI Cyber Security & Development Company API", "status": "operational"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    await initialize_database()
    logger.info("AI Agent system initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()