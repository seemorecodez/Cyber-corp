# AI Cyber Security & Development Company - Backend Contracts

## Overview
Full-stack MVP with 6 specialized AI agents working as a hive mind collective for autonomous cyber security and software development.

## Architecture

### AI Agent System
**6 Specialized Agents** (each using different model configurations):
1. **Sentinel** (Security Analyst) - GPT-5 for threat detection
2. **Phoenix** (Penetration Tester) - Claude-4-Sonnet for vulnerability testing
3. **Cipher** (Cryptography Expert) - Gemini-2.5-Pro for encryption
4. **Architect** (Software Developer) - GPT-5 for code generation
5. **Validator** (Code Reviewer) - Claude-4-Sonnet for code analysis
6. **Guardian** (Compliance Expert) - Gemini-2.5-Pro for compliance

### Database Collections

#### 1. agents
```json
{
  "_id": "ObjectId",
  "agent_id": "agent-1",
  "name": "Sentinel",
  "type": "Security Analyst",
  "status": "active|idle|busy",
  "model_provider": "openai",
  "model_name": "gpt-5",
  "avatar": "SA",
  "color": "from-blue-500 to-cyan-500",
  "current_task_id": "task-123",
  "tasks_completed": 1247,
  "success_rate": 98.5,
  "specialization": ["Threat Detection", "Risk Assessment"],
  "created_at": "ISO date"
}
```

#### 2. tasks
```json
{
  "_id": "ObjectId",
  "task_id": "task-123",
  "title": "Vulnerability Assessment - E-commerce Platform",
  "description": "Full security audit",
  "assigned_agent_id": "agent-1",
  "priority": "critical|high|medium|low",
  "status": "pending|in_progress|completed|failed",
  "progress": 73,
  "eta_minutes": 135,
  "result": "Task findings...",
  "created_at": "ISO date",
  "started_at": "ISO date",
  "completed_at": "ISO date"
}
```

#### 3. hive_messages
```json
{
  "_id": "ObjectId",
  "message_id": "msg-456",
  "from_agent_id": "agent-1",
  "to_agent_id": "agent-2|all",
  "message": "Detected SQL injection vector",
  "message_type": "alert|info|request",
  "timestamp": "ISO date",
  "read": false
}
```

#### 4. projects
```json
{
  "_id": "ObjectId",
  "project_id": "proj-789",
  "name": "SecureBank API",
  "type": "Backend Development",
  "status": "in_progress|testing|completed",
  "progress": 67,
  "assigned_agents": ["agent-4"],
  "tech_stack": ["Node.js", "PostgreSQL"],
  "security_score": 94,
  "total_tests": 156,
  "tests_passed": 152,
  "created_at": "ISO date"
}
```

#### 5. activities
```json
{
  "_id": "ObjectId",
  "activity_id": "act-101",
  "agent_id": "agent-2",
  "action": "Found critical XSS vulnerability",
  "activity_type": "alert|success|warning|info",
  "timestamp": "ISO date"
}
```

#### 6. certifications
```json
{
  "_id": "ObjectId",
  "name": "CISSP",
  "progress": 87,
  "status": "in_progress|certified",
  "total_modules": 8,
  "completed_modules": 7,
  "last_updated": "ISO date"
}
```

#### 7. chat_sessions
```json
{
  "_id": "ObjectId",
  "session_id": "sess-uuid",
  "agent_id": "agent-1",
  "messages": [
    {
      "role": "user|assistant",
      "content": "message text",
      "timestamp": "ISO date"
    }
  ],
  "created_at": "ISO date"
}
```

## API Endpoints

### Agents
- `GET /api/agents` - Get all agents with current status
- `GET /api/agents/{agent_id}` - Get specific agent details
- `POST /api/agents/{agent_id}/chat` - Chat with specific agent
  - Body: `{ "message": "user message", "session_id": "optional" }`
  - Returns: AI response from that agent

### Tasks
- `GET /api/tasks` - Get all tasks (with filters: status, priority, agent_id)
- `POST /api/tasks` - Create new task
  - Body: `{ "title": "", "description": "", "priority": "" }`
  - Auto-assigns to best available agent
- `GET /api/tasks/{task_id}` - Get task details
- `PUT /api/tasks/{task_id}` - Update task (progress, status)

### Hive Mind
- `GET /api/hive/messages` - Get recent inter-agent messages
- `POST /api/hive/broadcast` - User broadcasts to all agents
  - Body: `{ "message": "instruction to hive" }`
  - Triggers collaborative response

### Projects
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create new project
- `GET /api/projects/{project_id}` - Get project details

### Activities
- `GET /api/activities` - Get recent activities (paginated)

### Certifications
- `GET /api/certifications` - Get all certifications with progress

### Metrics
- `GET /api/metrics/security` - Security metrics dashboard
- `GET /api/metrics/development` - Development metrics dashboard

## AI Integration Strategy

### Using Emergent LLM Key
- Install: `emergentintegrations` library
- Add to `.env`: `EMERGENT_LLM_KEY=sk-emergent-52583FcEa8827264b8`
- Each agent uses different model for specialization:
  - Security agents → GPT-5, Claude-4-Sonnet (better reasoning)
  - Code agents → GPT-5 (best for code)
  - Analysis agents → Gemini-2.5-Pro (multimodal capabilities)

### Agent Behavior
Each agent has:
1. **System Prompt** defining its role and expertise
2. **Model Assignment** based on specialization
3. **Session Management** for conversation persistence
4. **Task Processing** loop that actually executes tasks

### Hive Mind Coordination
1. User sends message to hive
2. Primary agent processes and determines if help needed
3. Agents communicate via `hive_messages` collection
4. Collaborative responses synthesized
5. Final result returned to user

## Frontend Integration Changes

### Replace Mock Data With API Calls
1. **Dashboard.jsx**
   - Replace `agents` import with `useEffect` fetch from `/api/agents`
   - Replace `activeTasks` with fetch from `/api/tasks?status=in_progress`
   - Replace `recentActivity` with fetch from `/api/activities`
   - Poll for updates every 5 seconds

2. **HiveMind.jsx**
   - Load messages from `/api/hive/messages`
   - Send user messages to `/api/hive/broadcast`
   - WebSocket or polling for real-time updates

3. **Projects.jsx**
   - Fetch from `/api/projects`
   - Add project creation form

## Implementation Steps

1. ✅ Install `emergentintegrations` library
2. ✅ Add `EMERGENT_LLM_KEY` to `.env`
3. ✅ Create MongoDB models (Pydantic)
4. ✅ Implement agent system with LLM integration
5. ✅ Create all API endpoints
6. ✅ Add background task processor for agent execution
7. ✅ Update frontend to use real APIs
8. ✅ Test agent collaboration

## Task Automation System

### Auto-Task Assignment
When task created:
1. Analyze task type/requirements
2. Match to agent specialization
3. Assign to least busy agent with required skills
4. Agent processes task using LLM
5. Updates progress and results in real-time

### Certification Progress
Background job that:
1. Tracks agent learning from completed tasks
2. Updates certification progress
3. Automatically marks certifications as complete

## Security Considerations
- Rate limiting on AI endpoints
- Input validation and sanitization
- API key protection in environment
- Error handling for LLM failures
