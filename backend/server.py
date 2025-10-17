from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import socketio
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random

from models import (
    Agent, Task, TaskCreate, HiveMessage, HiveBroadcast,
    Project, Activity, Certification, ChatMessage, ChatResponse
)
from agent_system import orchestrator
from security_engine import security_analyzer
from metrics_engine import MetricsEngine

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="AI Cyber Security & Development Company API", version="2.0.0")

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)
socket_app = socketio.ASGIApp(sio, app)

# Create API router with prefix
api_router = APIRouter(prefix="/api")

# Scheduler for automated tasks
scheduler = AsyncIOScheduler()

# Initialize metrics engine
metrics_engine = None

# Helper functions
def clean_mongo_doc(doc):
    """Remove MongoDB _id field from document"""
    if doc and '_id' in doc:
        doc.pop('_id')
    return doc

def clean_mongo_docs(docs):
    """Remove MongoDB _id field from list of documents"""
    return [clean_mongo_doc(doc) for doc in docs]

# WebSocket connection management
active_connections = set()

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    active_connections.add(sid)
    await sio.emit('connection_established', {'status': 'connected', 'sid': sid}, room=sid)
    logging.info(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    active_connections.discard(sid)
    logging.info(f"Client {sid} disconnected")

@sio.event
async def subscribe_updates(sid, data):
    """Subscribe to real-time updates"""
    await sio.enter_room(sid, 'updates')
    await sio.emit('subscribed', {'message': 'Subscribed to updates'}, room=sid)

async def broadcast_update(event_type: str, data: dict):
    """Broadcast update to all connected clients"""
    await sio.emit('update', {'type': event_type, 'data': data}, room='updates')

# Initialize database with default data
async def initialize_database():
    """Initialize database with default agents and data"""
    try:
        existing_agents = await db.agents.count_documents({})
        if existing_agents == 0:
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

# Scheduled tasks
async def generate_agent_activity():
    """Generate random agent activities periodically"""
    try:
        agents = await db.agents.find().to_list(100)
        if not agents:
            return
            
        agent = random.choice(agents)
        actions = [
            "Analyzed security log patterns",
            "Updated threat intelligence database",
            "Completed code review",
            "Generated compliance report",
            "Detected anomaly in network traffic",
            "Optimized system performance",
            "Updated encryption protocols",
            "Scanned for vulnerabilities"
        ]
        
        activity = Activity(
            agent_id=agent["agent_id"],
            action=random.choice(actions),
            activity_type=random.choice(["info", "success"])
        )
        
        await db.activities.insert_one(activity.dict())
        
        # Broadcast to connected clients
        activity_data = activity.dict()
        activity_data["agent_name"] = agent["name"]
        await broadcast_update("new_activity", activity_data)
        
    except Exception as e:
        logging.error(f"Error generating activity: {str(e)}")

async def update_certification_progress():
    """Update certification progress periodically"""
    try:
        certs = await db.certifications.find({"status": "in_progress"}).to_list(100)
        for cert in certs:
            if cert["progress"] < 100 and random.random() < 0.3:  # 30% chance to progress
                new_progress = min(100, cert["progress"] + random.randint(1, 5))
                completed_modules = int((new_progress / 100) * cert["total_modules"])
                
                update_data = {
                    "progress": new_progress,
                    "completed_modules": completed_modules,
                    "last_updated": datetime.utcnow()
                }
                
                if new_progress >= 100:
                    update_data["status"] = "certified"
                
                await db.certifications.update_one(
                    {"name": cert["name"]},
                    {"$set": update_data}
                )
                
                await broadcast_update("certification_progress", {
                    "name": cert["name"],
                    "progress": new_progress,
                    "status": update_data.get("status", "in_progress")
                })
                
    except Exception as e:
        logging.error(f"Error updating certifications: {str(e)}")

# Agent Endpoints with real-time updates
@api_router.get("/agents")
async def get_agents():
    """Get all AI agents with their current status"""
    agents = await db.agents.find().to_list(100)
    result = []
    for agent in agents:
        agent.pop('_id', None)
        if agent.get("current_task_id"):
            task = await db.tasks.find_one({"task_id": agent["current_task_id"]})
            agent["current_task"] = task.get("title") if task else "Processing task"
        else:
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
        
        activity = Activity(
            agent_id=agent_id,
            action=f"Responded to user query: {message.message[:50]}...",
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
    
    tasks = await db.tasks.find(query).sort("created_at", -1).limit(50).to_list(50)
    tasks = clean_mongo_docs(tasks)
    
    for task in tasks:
        if task.get("assigned_agent_id"):
            agent = await db.agents.find_one({"agent_id": task["assigned_agent_id"]})
            task["agent_name"] = agent.get("name") if agent else "Unknown"
    
    return tasks

@api_router.post("/tasks")
async def create_task(task: TaskCreate):
    """Create a new task and auto-assign to best agent"""
    task_lower = task.title.lower() + " " + task.description.lower()
    
    if any(word in task_lower for word in ["security", "threat", "vulnerability"]):
        agent_id = "agent-1"
    elif any(word in task_lower for word in ["code", "develop", "build"]):
        agent_id = "agent-4"
    elif any(word in task_lower for word in ["review", "audit"]):
        agent_id = "agent-5"
    elif any(word in task_lower for word in ["compliance", "regulation"]):
        agent_id = "agent-6"
    else:
        agent_id = "agent-1"
    
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        assigned_agent_id=agent_id,
        status="in_progress",
        eta_minutes=120
    )
    
    await db.tasks.insert_one(new_task.dict())
    await db.agents.update_one(
        {"agent_id": agent_id},
        {"$set": {"current_task_id": new_task.task_id}}
    )
    
    # Broadcast new task
    task_data = new_task.dict()
    agent = await db.agents.find_one({"agent_id": agent_id})
    task_data["agent_name"] = agent.get("name") if agent else "Unknown"
    await broadcast_update("new_task", task_data)
    
    asyncio.create_task(process_task_background(new_task.task_id, agent_id))
    return new_task

async def process_task_background(task_id: str, agent_id: str):
    """Background task processor with real-time progress updates"""
    try:
        task = await db.tasks.find_one({"task_id": task_id})
        if not task:
            return
        
        ai_agent = orchestrator.get_agent(agent_id)
        if not ai_agent:
            return
        
        for progress in [25, 50, 75]:
            await asyncio.sleep(2)
            await db.tasks.update_one(
                {"task_id": task_id},
                {"$set": {"progress": progress}}
            )
            await broadcast_update("task_progress", {"task_id": task_id, "progress": progress})
        
        result = await ai_agent.process_task(task["title"], task["description"])
        
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
        
        await db.agents.update_one(
            {"agent_id": agent_id},
            {
                "$set": {"current_task_id": None},
                "$inc": {"tasks_completed": 1}
            }
        )
        
        agent_data = await db.agents.find_one({"agent_id": agent_id})
        activity = Activity(
            agent_id=agent_id,
            action=f"Completed task: {task['title']}",
            activity_type="success"
        )
        await db.activities.insert_one(activity.dict())
        
        await broadcast_update("task_completed", {"task_id": task_id, "agent_name": agent_data.get("name")})
        
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
    messages = clean_mongo_docs(messages)
    
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
        
        hive_msg = HiveMessage(
            from_agent_id="system",
            to_agent_id="all",
            message=f"User query: {broadcast.message}",
            message_type="request"
        )
        await db.hive_messages.insert_one(hive_msg.dict())
        
        response_msg = HiveMessage(
            from_agent_id=result.get("primary_agent", "agent-1"),
            to_agent_id="system",
            message=result["primary_response"][:200] + "...",
            message_type="info"
        )
        await db.hive_messages.insert_one(response_msg.dict())
        
        await broadcast_update("new_hive_message", response_msg.dict())
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Analytics Endpoints
@api_router.get("/analytics/dashboard")
async def get_dashboard_analytics():
    """Get comprehensive dashboard analytics"""
    try:
        # Task stats
        total_tasks = await db.tasks.count_documents({})
        completed_tasks = await db.tasks.count_documents({"status": "completed"})
        in_progress_tasks = await db.tasks.count_documents({"status": "in_progress"})
        failed_tasks = await db.tasks.count_documents({"status": "failed"})
        
        # Agent stats
        agents_data = await db.agents.find().to_list(100)
        total_tasks_completed = sum(agent.get("tasks_completed", 0) for agent in agents_data)
        avg_success_rate = sum(agent.get("success_rate", 0) for agent in agents_data) / len(agents_data) if agents_data else 0
        
        # Time-based activity
        last_24h = datetime.utcnow() - timedelta(hours=24)
        recent_activities = await db.activities.count_documents({"timestamp": {"$gte": last_24h}})
        
        # Certification stats
        certified_count = await db.certifications.count_documents({"status": "certified"})
        in_progress_certs = await db.certifications.count_documents({"status": "in_progress"})
        
        return {
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "failed": failed_tasks,
                "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            "agents": {
                "total": len(agents_data),
                "active": len([a for a in agents_data if a.get("status") == "active"]),
                "total_tasks_completed": total_tasks_completed,
                "average_success_rate": round(avg_success_rate, 2)
            },
            "activity": {
                "last_24h": recent_activities
            },
            "certifications": {
                "certified": certified_count,
                "in_progress": in_progress_certs
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@api_router.get("/analytics/agent-performance")
async def get_agent_performance():
    """Get detailed agent performance metrics"""
    agents = await db.agents.find().to_list(100)
    performance_data = []
    
    for agent in agents:
        agent_id = agent["agent_id"]
        
        # Get task stats for this agent
        agent_tasks = await db.tasks.find({"assigned_agent_id": agent_id}).to_list(1000)
        completed = len([t for t in agent_tasks if t.get("status") == "completed"])
        failed = len([t for t in agent_tasks if t.get("status") == "failed"])
        
        # Calculate average completion time
        completion_times = []
        for task in agent_tasks:
            if task.get("completed_at") and task.get("created_at"):
                duration = (task["completed_at"] - task["created_at"]).total_seconds() / 60
                completion_times.append(duration)
        
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        performance_data.append({
            "agent_id": agent_id,
            "name": agent["name"],
            "type": agent["type"],
            "tasks_completed": completed,
            "tasks_failed": failed,
            "success_rate": agent.get("success_rate", 0),
            "avg_completion_time_minutes": round(avg_completion_time, 2)
        })
    
    return performance_data

# Other Endpoints
@api_router.get("/activities")
async def get_activities(limit: int = Query(20)):
    """Get recent activities"""
    activities = await db.activities.find().sort("timestamp", -1).limit(limit).to_list(limit)
    activities = clean_mongo_docs(activities)
    
    for activity in activities:
        agent = await db.agents.find_one({"agent_id": activity["agent_id"]})
        activity["agent_name"] = agent.get("name") if agent else "Unknown"
    
    return activities

@api_router.get("/certifications")
async def get_certifications():
    """Get all certifications with progress"""
    certifications = await db.certifications.find().to_list(100)
    return clean_mongo_docs(certifications)

@api_router.get("/metrics/security")
async def get_security_metrics():
    """Get REAL security metrics calculated from actual data"""
    global metrics_engine
    if not metrics_engine:
        metrics_engine = MetricsEngine(db)
    return await metrics_engine.calculate_security_metrics()

@api_router.get("/metrics/development")
async def get_development_metrics():
    """Get REAL development metrics calculated from actual data"""
    global metrics_engine
    if not metrics_engine:
        metrics_engine = MetricsEngine(db)
    return await metrics_engine.calculate_development_metrics()

@api_router.get("/health")
async def health_check():
    """System health check"""
    try:
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "agents": len(orchestrator.get_all_agents()),
            "active_websockets": len(active_connections),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@api_router.get("/")
async def root():
    return {
        "message": "AI Cyber Security & Development Company API v2.0",
        "status": "operational",
        "docs": "/docs",
        "features": [
            "6 Specialized AI Agents",
            "Real-time WebSocket Updates",
            "Advanced Analytics",
            "Task Automation",
            "Hive Mind Collaboration"
        ]
    }

# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Startup/Shutdown events
@app.on_event("startup")
async def startup_db_client():
    await initialize_database()
    
    # Start scheduled tasks
    scheduler.add_job(generate_agent_activity, 'interval', seconds=30)
    scheduler.add_job(update_certification_progress, 'interval', minutes=2)
    scheduler.start()
    
    logger.info("AI Agent system initialized with real-time features")

@app.on_event("shutdown")
async def shutdown_db_client():
    scheduler.shutdown()
    client.close()
    logger.info("System shutdown complete")
