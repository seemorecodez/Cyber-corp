// Mock data for AI Cyber Security & Development Company

export const agents = [
  {
    id: 'agent-1',
    name: 'Sentinel',
    type: 'Security Analyst',
    status: 'active',
    avatar: 'SA',
    color: 'from-blue-500 to-cyan-500',
    currentTask: 'Analyzing network traffic patterns',
    tasksCompleted: 1247,
    successRate: 98.5,
    specialization: ['Threat Detection', 'Risk Assessment', 'SIEM Analysis']
  },
  {
    id: 'agent-2',
    name: 'Phoenix',
    type: 'Penetration Tester',
    status: 'active',
    avatar: 'PT',
    color: 'from-red-500 to-orange-500',
    currentTask: 'Running OWASP Top 10 vulnerability scan',
    tasksCompleted: 892,
    successRate: 96.2,
    specialization: ['Web App Testing', 'Network Pentesting', 'Social Engineering']
  },
  {
    id: 'agent-3',
    name: 'Cipher',
    type: 'Cryptography Expert',
    status: 'active',
    avatar: 'CE',
    color: 'from-purple-500 to-pink-500',
    currentTask: 'Implementing zero-knowledge proof protocol',
    tasksCompleted: 654,
    successRate: 99.1,
    specialization: ['Encryption', 'Key Management', 'Blockchain Security']
  },
  {
    id: 'agent-4',
    name: 'Architect',
    type: 'Software Developer',
    status: 'active',
    avatar: 'SD',
    color: 'from-green-500 to-emerald-500',
    currentTask: 'Developing microservices architecture',
    tasksCompleted: 2103,
    successRate: 97.8,
    specialization: ['Full-Stack Dev', 'Cloud Architecture', 'API Design']
  },
  {
    id: 'agent-5',
    name: 'Validator',
    type: 'Code Reviewer',
    status: 'active',
    avatar: 'CR',
    color: 'from-yellow-500 to-amber-500',
    currentTask: 'Reviewing authentication module for vulnerabilities',
    tasksCompleted: 1876,
    successRate: 98.9,
    specialization: ['Static Analysis', 'Code Quality', 'Security Audit']
  },
  {
    id: 'agent-6',
    name: 'Guardian',
    type: 'Compliance Expert',
    status: 'active',
    avatar: 'CM',
    color: 'from-indigo-500 to-blue-500',
    currentTask: 'Generating SOC 2 Type II documentation',
    tasksCompleted: 543,
    successRate: 99.7,
    specialization: ['GDPR', 'HIPAA', 'SOC 2', 'ISO 27001']
  }
];

export const certifications = [
  { name: 'CISSP', progress: 87, status: 'In Progress', modules: 8, completed: 7 },
  { name: 'CEH', progress: 100, status: 'Certified', modules: 20, completed: 20 },
  { name: 'OSCP', progress: 62, status: 'In Progress', modules: 12, completed: 7 },
  { name: 'CISM', progress: 100, status: 'Certified', modules: 4, completed: 4 },
  { name: 'CompTIA Security+', progress: 100, status: 'Certified', modules: 6, completed: 6 },
  { name: 'AWS Security', progress: 45, status: 'In Progress', modules: 10, completed: 4 }
];

export const activeTasks = [
  { id: 1, title: 'Vulnerability Assessment - E-commerce Platform', agent: 'Sentinel', priority: 'high', progress: 73, eta: '2h 15m' },
  { id: 2, title: 'API Development - Payment Gateway', agent: 'Architect', priority: 'critical', progress: 89, eta: '45m' },
  { id: 3, title: 'Code Review - Authentication System', agent: 'Validator', priority: 'medium', progress: 56, eta: '3h 30m' },
  { id: 4, title: 'Penetration Test - Mobile Application', agent: 'Phoenix', priority: 'high', progress: 41, eta: '5h 20m' },
  { id: 5, title: 'Compliance Audit - Healthcare Portal', agent: 'Guardian', priority: 'medium', progress: 67, eta: '2h 45m' },
  { id: 6, title: 'Encryption Implementation - Database Layer', agent: 'Cipher', priority: 'high', progress: 82, eta: '1h 10m' }
];

export const recentActivity = [
  { id: 1, agent: 'Phoenix', action: 'Found critical XSS vulnerability', time: '2m ago', type: 'alert' },
  { id: 2, agent: 'Architect', action: 'Deployed microservice to production', time: '5m ago', type: 'success' },
  { id: 3, agent: 'Validator', action: 'Approved pull request #342', time: '8m ago', type: 'info' },
  { id: 4, agent: 'Sentinel', action: 'Blocked 15 suspicious IP addresses', time: '12m ago', type: 'warning' },
  { id: 5, agent: 'Guardian', action: 'Generated compliance report', time: '15m ago', type: 'success' },
  { id: 6, agent: 'Cipher', action: 'Updated encryption keys', time: '18m ago', type: 'info' },
  { id: 7, agent: 'Phoenix', action: 'Completed penetration test', time: '25m ago', type: 'success' },
  { id: 8, agent: 'Sentinel', action: 'Detected anomaly in network traffic', time: '32m ago', type: 'alert' }
];

export const hiveMindMessages = [
  { id: 1, from: 'Sentinel', to: 'Phoenix', message: 'Detected potential SQL injection vector in /api/users endpoint', timestamp: '10:23 AM' },
  { id: 2, from: 'Phoenix', to: 'Validator', message: 'Confirmed vulnerability. Requesting code review.', timestamp: '10:24 AM' },
  { id: 3, from: 'Validator', to: 'Architect', message: 'Security flaw found in authentication logic. Patch needed.', timestamp: '10:26 AM' },
  { id: 4, from: 'Architect', to: 'All', message: 'Implementing parameterized queries. ETA 30 minutes.', timestamp: '10:28 AM' },
  { id: 5, from: 'Guardian', to: 'All', message: 'Compliance scan scheduled for 2 PM. Please sync databases.', timestamp: '10:35 AM' },
  { id: 6, from: 'Cipher', to: 'Architect', message: 'Encryption module ready for integration.', timestamp: '10:42 AM' }
];

export const securityMetrics = {
  vulnerabilitiesFound: 1247,
  vulnerabilitiesFixed: 1198,
  threatsBlocked: 8934,
  uptime: 99.97,
  avgResponseTime: '1.2s',
  securityScore: 96
};

export const developmentMetrics = {
  projectsCompleted: 87,
  codeReviews: 432,
  deploymentsToday: 23,
  testCoverage: 94.5,
  bugsFixed: 156,
  performance: 98
};
