from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# Agent Models
class Agent(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"agent-{uuid.uuid4().hex[:8]}")
    name: str
    type: str
    status: str = "active"
    model_provider: str
    model_name: str
    avatar: str
    color: str
    current_task_id: Optional[str] = None
    tasks_completed: int = 0
    success_rate: float = 100.0
    specialization: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Task Models
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str = "medium"  # critical, high, medium, low

class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    assigned_agent_id: Optional[str] = None
    priority: str
    status: str = "pending"  # pending, in_progress, completed, failed
    progress: int = 0
    eta_minutes: int = 0
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Hive Mind Message Models
class HiveMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    from_agent_id: str
    to_agent_id: str  # "all" for broadcast
    message: str
    message_type: str = "info"  # alert, info, request
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False

class HiveBroadcast(BaseModel):
    message: str

# Project Models
class Project(BaseModel):
    project_id: str = Field(default_factory=lambda: f"proj-{uuid.uuid4().hex[:8]}")
    name: str
    type: str
    status: str = "in_progress"  # in_progress, testing, completed
    progress: int = 0
    assigned_agents: List[str] = []
    tech_stack: List[str] = []
    security_score: int = 100
    total_tests: int = 0
    tests_passed: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Activity Models
class Activity(BaseModel):
    activity_id: str = Field(default_factory=lambda: f"act-{uuid.uuid4().hex[:8]}")
    agent_id: str
    action: str
    activity_type: str  # alert, success, warning, info
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Certification Models
class Certification(BaseModel):
    name: str
    progress: int
    status: str  # in_progress, certified
    total_modules: int
    completed_modules: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# Chat Models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    agent_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
