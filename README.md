# 🤖 CyberAI Corp - AI-Powered Cyber Security & Development Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248.svg?style=flat&logo=MongoDB&logoColor=white)](https://www.mongodb.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933.svg?style=flat&logo=Node.js&logoColor=white)](https://nodejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 Project Overview

**CyberAI Corp** is a state-of-the-art, fully automated AI-powered cyber security and software development platform featuring **6 specialized AI agents** working as a collaborative **hive mind collective**. This cutting-edge platform combines advanced AI capabilities with real-time monitoring, analytics, and automated task processing to deliver comprehensive cyber security solutions and enterprise-grade software development.

### 🎯 Purpose

The platform is designed to:
- **Automate cyber security operations** with AI-powered threat detection and vulnerability assessment
- **Streamline software development** with intelligent code generation, review, and deployment
- **Ensure compliance** with automated tracking of GDPR, HIPAA, SOC 2, and ISO 27001 standards
- **Enable collaboration** through a hive mind architecture where AI agents work together
- **Provide real-time insights** via advanced analytics dashboards and live monitoring

### ✨ Key Features

#### 🤖 6 Specialized AI Agents
Each agent leverages cutting-edge LLM models optimized for their domain:

1. **Sentinel** (Security Analyst) - *Powered by GPT-5*
   - Threat detection and risk assessment
   - Real-time network traffic monitoring
   - Security log pattern analysis
   - SIEM analysis and incident response

2. **Phoenix** (Penetration Tester) - *Powered by Claude-4-Sonnet*
   - OWASP Top 10 vulnerability scanning
   - Network and web application penetration testing
   - Social engineering assessments
   - Security weakness identification

3. **Cipher** (Cryptography Expert) - *Powered by Gemini-2.5-Pro*
   - Encryption implementation and key management
   - Blockchain security analysis
   - Zero-knowledge proof protocols
   - Cryptographic algorithm recommendations

4. **Architect** (Software Developer) - *Powered by GPT-5*
   - Full-stack development (frontend + backend)
   - Cloud architecture design
   - Microservices implementation
   - Best practices enforcement

5. **Validator** (Code Reviewer) - *Powered by Claude-4-Sonnet*
   - Static code analysis and security audits
   - Code quality assurance
   - Performance optimization recommendations
   - Security vulnerability detection in code

6. **Guardian** (Compliance Expert) - *Powered by Gemini-2.5-Pro*
   - GDPR, HIPAA, SOC 2, ISO 27001 compliance tracking
   - Automated documentation generation
   - Regulatory requirement monitoring
   - Policy enforcement and audit preparation

#### 🔥 Core Capabilities

- **Real-Time WebSocket Communication**: Live updates for all system events with instant task progress notifications
- **Advanced Analytics Dashboard**: Performance metrics, interactive charts (bar, pie, line graphs), agent efficiency tracking
- **Intelligent Task Management**: Auto-assignment to best-suited agents, background processing, priority queuing
- **Hive Mind Collaboration**: Inter-agent communication, collective problem solving, context awareness
- **Automated Certification Progress**: Track CISSP, CEH, OSCP, CISM, CompTIA Security+, AWS Security certifications
- **Comprehensive RESTful API**: FastAPI with OpenAPI/Swagger documentation at `/docs`
- **Scheduled Automation**: Periodic activity generation, certification updates, health checks

### 🛠️ Technology Stack

#### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **AI Integration**: emergentintegrations library
  - OpenAI (GPT-5)
  - Anthropic (Claude-4-Sonnet)
  - Google (Gemini-2.5-Pro)
- **Real-Time**: Socket.IO for WebSocket communication
- **Scheduling**: APScheduler for automated tasks
- **Async Processing**: asyncio for concurrent operations

#### Frontend
- **Framework**: React 19
- **UI Components**: Shadcn/ui with Radix UI primitives
- **Styling**: Tailwind CSS with custom animations
- **Charts**: Recharts for data visualization
- **Real-Time**: Socket.IO Client
- **State Management**: React Hooks
- **Routing**: React Router v7

#### Database Collections
- `agents`: Agent profiles and status
- `tasks`: Task queue and history
- `hive_messages`: Inter-agent communications
- `activities`: System activity log
- `certifications`: Certification progress tracking
- `projects`: Development projects (extensible)

### 🌟 Unique Aspects

- **Multi-Model AI Integration**: Leverages the strengths of different LLMs (GPT-5, Claude-4-Sonnet, Gemini-2.5-Pro)
- **Hive Mind Architecture**: Agents collaborate like a real team with shared intelligence
- **Real-Time Everything**: Live updates across the entire system without page reloads
- **Zero Configuration**: Works out of the box with an Emergent LLM API key
- **Enterprise Grade**: Production-ready with monitoring, health checks, and error handling

## 🚀 Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18 or higher ([Download](https://nodejs.org/))
- **Python**: Version 3.11 or higher ([Download](https://www.python.org/downloads/))
- **MongoDB**: Version 4.4 or higher ([Download](https://www.mongodb.com/try/download/community))
- **Yarn**: Package manager for Node.js (`npm install -g yarn`)
- **pip**: Python package installer (included with Python)
- **Emergent LLM Key**: Required for AI agent functionality ([Get API Key](https://www.emergentagi.com))

### System Requirements

**Development Environment:**
- RAM: 4GB minimum (8GB recommended)
- Disk Space: 10GB minimum
- OS: Linux, macOS, or Windows with WSL

**Production Environment:**
- RAM: 8GB minimum (16GB recommended)
- Disk Space: 20GB minimum
- SSL certificate for HTTPS
- Reverse proxy (nginx recommended)
- Load balancer (optional, for scaling)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/seemorecodez/Cyber-corp.git
cd Cyber-corp
```

#### 2. Backend Setup

Navigate to the backend directory and install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory with the following configuration:
```bash
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=cyberai_db

# CORS Configuration
CORS_ORIGINS=*

# AI Integration (Required)
EMERGENT_LLM_KEY=sk-emergent-your-api-key-here
```

**Note**: Replace `sk-emergent-your-api-key-here` with your actual Emergent LLM API key.

#### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:
```bash
cd ../frontend
yarn install
```

Create a `.env` file in the `frontend` directory:
```bash
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001
```

#### 4. Start MongoDB

Ensure MongoDB is running on your system:
```bash
# On Linux/macOS
sudo systemctl start mongod

# On macOS with Homebrew
brew services start mongodb-community

# On Windows
net start MongoDB
```

Verify MongoDB is running:
```bash
mongosh --eval "db.version()"
```

#### 5. Start the Application

**Start the Backend Server** (from the `backend` directory):
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

The backend API will be available at: `http://localhost:8001`
API documentation (Swagger UI): `http://localhost:8001/docs`

**Start the Frontend Application** (from the `frontend` directory, in a new terminal):
```bash
cd frontend
yarn start
```

The frontend application will open automatically in your browser at: `http://localhost:3000`

### 🔍 Verification

Once both services are running:
1. Open your browser to `http://localhost:3000`
2. You should see the CyberAI Corp dashboard with the 6 AI agents
3. Check the API documentation at `http://localhost:8001/docs`
4. WebSocket connection should establish automatically (check browser console)

### 🐛 Troubleshooting

#### MongoDB Connection Issues
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Check MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

#### Port Already in Use
```bash
# Find process using port 8001 (backend)
lsof -i :8001
kill -9 <PID>

# Find process using port 3000 (frontend)
lsof -i :3000
kill -9 <PID>
```

#### Python Dependencies Issues
```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Node.js Dependencies Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json yarn.lock
yarn cache clean
yarn install
```

#### AI Agents Not Responding
- Verify your `EMERGENT_LLM_KEY` is correct in the `.env` file
- Check backend logs for API key validation errors
- Ensure you have internet connectivity for AI API calls

## 📁 File Structure Overview

```
Cyber-corp/
├── backend/                      # Backend API server (FastAPI)
│   ├── server.py                 # Main FastAPI application and API endpoints
│   ├── agent_system.py           # AI agent system implementation
│   ├── models.py                 # Pydantic models and database schemas
│   ├── security_engine.py        # Security-related functionality
│   ├── metrics_engine.py         # Analytics and metrics calculation
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment configuration (create this)
│
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/           # React components
│   │   │   └── ui/               # Shadcn/ui components
│   │   ├── pages/                # Page components (Dashboard, HiveMind, etc.)
│   │   ├── App.js                # Main React application
│   │   └── index.js              # Application entry point
│   ├── public/                   # Static assets
│   ├── package.json              # Node.js dependencies
│   ├── tailwind.config.js        # Tailwind CSS configuration
│   └── .env                      # Frontend environment variables (create this)
│
├── tests/                        # Test files
│   ├── __init__.py
│   └── (test files to be added)
│
├── README.md                     # This file - project documentation
├── SYSTEM_DOCUMENTATION.md       # Detailed system architecture documentation
├── contracts.md                  # API contracts and database schemas
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── backend_test.py               # Backend test suite
└── backend_test_results.json     # Test results

```

### Key Files and Their Purposes

| File | Purpose |
|------|---------|
| `backend/server.py` | Main FastAPI application with all API endpoints, WebSocket handling, and scheduled tasks |
| `backend/agent_system.py` | Implementation of the 6 AI agents and hive mind coordination logic |
| `backend/models.py` | Pydantic models for data validation and MongoDB schemas |
| `backend/security_engine.py` | Security-related functionality and threat detection |
| `backend/metrics_engine.py` | Analytics calculation and performance metrics |
| `frontend/src/App.js` | Main React application with routing and global state |
| `frontend/src/components/ui/` | Reusable UI components from Shadcn/ui library |
| `SYSTEM_DOCUMENTATION.md` | Comprehensive system architecture and technical details |
| `contracts.md` | API contracts, database schemas, and integration strategy |

## 🤝 Contribution Guidelines

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or enhancing tests, your help is appreciated.

### How to Contribute

#### 1. Fork the Repository
Click the "Fork" button at the top right of the repository page.

#### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/Cyber-corp.git
cd Cyber-corp
```

#### 3. Create a Feature Branch
Use descriptive branch names following our naming convention:
```bash
# Feature development
git checkout -b feature/add-new-agent

# Bug fixes
git checkout -b fix/websocket-reconnection

# Documentation updates
git checkout -b docs/api-documentation

# Performance improvements
git checkout -b perf/optimize-database-queries

# Refactoring
git checkout -b refactor/agent-system
```

### Branch Naming Convention

- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Adding or updating tests
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `style/` - Code style changes (formatting, etc.)
- `chore/` - Maintenance tasks

### Code Style Guidelines

#### Python (Backend)
- **Style Guide**: Follow [PEP 8](https://pep8.org/)
- **Formatter**: Use `black` for code formatting
  ```bash
  black backend/
  ```
- **Linter**: Use `flake8` for linting
  ```bash
  flake8 backend/
  ```
- **Type Hints**: Use type hints for function parameters and return values
  ```python
  def get_agent(agent_id: str) -> dict:
      """Get agent by ID."""
      pass
  ```
- **Docstrings**: Use Google-style docstrings
  ```python
  def process_task(task_id: str) -> dict:
      """Process a task with an AI agent.
      
      Args:
          task_id: The unique identifier of the task
          
      Returns:
          dict: The task result with status and output
      """
      pass
  ```

#### JavaScript/React (Frontend)
- **Style Guide**: Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Formatter**: Use Prettier (if configured)
- **Component Style**: Use functional components with hooks
  ```javascript
  const AgentCard = ({ agent }) => {
    const [status, setStatus] = useState('idle');
    // Component logic
    return <div>...</div>;
  };
  ```
- **Naming Conventions**:
  - Components: PascalCase (`AgentCard.jsx`)
  - Functions: camelCase (`fetchAgentData`)
  - Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)

### Commit Message Conventions

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(agents): add new compliance agent for GDPR
fix(websocket): resolve reconnection issue on network failure
docs(readme): update setup instructions for Windows
test(api): add unit tests for task assignment logic
refactor(database): optimize query performance for agent status
```

### Contribution Areas

We welcome contributions in the following areas:

#### 🎨 Frontend Development
- React component development
- UI/UX improvements
- Responsive design enhancements
- Chart and visualization features
- Accessibility improvements
- Performance optimization

**Skills Needed**: React, JavaScript/TypeScript, Tailwind CSS, HTML/CSS

#### ⚙️ Backend Development
- API endpoint development
- Database schema improvements
- AI agent logic enhancements
- WebSocket functionality
- Background job processing
- Performance optimization

**Skills Needed**: Python, FastAPI, MongoDB, asyncio, AI/LLM integration

#### 📚 Documentation
- README improvements
- API documentation
- Code comments and docstrings
- Tutorial creation
- Architecture diagrams
- Video tutorials

**Skills Needed**: Technical writing, Markdown, documentation tools

#### 🧪 Testing
- Unit test creation
- Integration tests
- End-to-end tests
- Performance testing
- Security testing
- Test coverage improvements

**Skills Needed**: pytest (Python), Jest/React Testing Library (JavaScript)

#### 🔒 Security
- Security vulnerability identification
- Code security audits
- Penetration testing
- Encryption improvements
- Authentication/authorization

**Skills Needed**: Security expertise, OWASP knowledge, penetration testing

#### 🚀 DevOps
- CI/CD pipeline setup
- Docker containerization
- Kubernetes deployment
- Monitoring and logging
- Performance profiling

**Skills Needed**: Docker, CI/CD tools, cloud platforms, monitoring tools

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Test Your Changes**
   - Run backend tests: `pytest backend_test.py`
   - Run frontend tests: `yarn test` (if configured)
   - Manually test the application

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat(agents): add new security scanning feature"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin your-feature-branch
   ```

5. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template with:
     - Description of changes
     - Related issues (if any)
     - Testing performed
     - Screenshots (for UI changes)

6. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Push updates to your branch (PR will update automatically)

7. **Merge**
   - Once approved, a maintainer will merge your PR
   - Delete your feature branch after merge

### Code Review Checklist

Before submitting your PR, ensure:
- [ ] Code follows style guidelines
- [ ] Commit messages follow conventions
- [ ] Tests pass successfully
- [ ] Documentation is updated
- [ ] No unnecessary console.log or debug code
- [ ] No hardcoded credentials or sensitive data
- [ ] Code is properly formatted
- [ ] New features include tests
- [ ] Breaking changes are documented

## 🗺️ Roadmap

### Current Version: v1.0
- ✅ 6 Specialized AI Agents
- ✅ Real-time WebSocket communication
- ✅ Advanced analytics dashboard
- ✅ Hive mind collaboration
- ✅ Task management system
- ✅ MongoDB integration
- ✅ Comprehensive API

### Future Enhancements

#### v1.1 - Authentication & Authorization (Q1 2025)
- JWT-based authentication system
- Role-based access control (Admin, User, Viewer)
- User registration and login
- Session management
- OAuth integration (Google, GitHub)

#### v1.2 - Advanced Features (Q2 2025)
- Report generation (PDF export with jsPDF)
- Email notification system
- Advanced search and filtering
- Data export (CSV/JSON)
- Audit logs and activity tracking
- Custom dashboards

#### v1.3 - Enterprise Features (Q3 2025)
- Multi-tenancy support
- Organization management
- Team collaboration features
- Advanced analytics and insights
- AI model selection (switch between models)
- Custom agent creation

#### v1.4 - Integration & Scaling (Q4 2025)
- Third-party integrations (Slack, Jira, GitHub)
- Webhook support
- API rate limiting
- Caching layer (Redis)
- Horizontal scaling support
- Docker and Kubernetes deployment guides

#### v2.0 - Next Generation (2026)
- GraphQL API
- Mobile application (React Native)
- Advanced AI features (fine-tuning, custom models)
- Real-time collaboration workspace
- Video conferencing integration
- Advanced security features (2FA, SSO)

## 📊 API Documentation

The complete API documentation is available at `http://localhost:8001/docs` when running the backend server.

### Key Endpoints

**Agents**
- `GET /api/agents` - List all agents
- `GET /api/agents/{agent_id}` - Get specific agent
- `POST /api/agents/{agent_id}/chat` - Chat with agent

**Tasks**
- `GET /api/tasks` - List tasks (with filters)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get task details

**Hive Mind**
- `GET /api/hive/messages` - Get hive messages
- `POST /api/hive/broadcast` - Broadcast to all agents

**Analytics**
- `GET /api/analytics/dashboard` - Dashboard analytics
- `GET /api/analytics/agent-performance` - Agent performance metrics

For detailed API contracts and schemas, see [contracts.md](contracts.md).

## 📞 Contact & Community

### Maintainers
- **Primary Maintainer**: [@seemorecodez](https://github.com/seemorecodez)

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/seemorecodez/Cyber-corp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/seemorecodez/Cyber-corp/discussions)
- **Documentation**: [System Documentation](SYSTEM_DOCUMENTATION.md)

### Community
- Star ⭐ this repository if you find it useful
- Watch 👀 for updates and new releases
- Fork 🍴 to contribute your own improvements

### Reporting Issues
When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node.js version)
- Error messages or logs
- Screenshots (for UI issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent Python web framework
- **React**: For the powerful frontend library
- **MongoDB**: For the flexible NoSQL database
- **OpenAI, Anthropic, Google**: For providing cutting-edge AI models
- **Emergent AGI**: For the unified LLM integration platform
- **Shadcn/ui**: For the beautiful UI component library
- **Tailwind CSS**: For the utility-first CSS framework

---

**Built with ❤️ using cutting-edge AI technology**

**Powered by**: GPT-5, Claude-4-Sonnet, Gemini-2.5-Pro | **Framework**: FastAPI + React + MongoDB
