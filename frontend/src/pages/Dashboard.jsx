import React, { useState, useEffect } from 'react';
import { Activity, Shield, Code, CheckCircle2, AlertTriangle, TrendingUp, Zap, Users } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Badge } from '../components/ui/badge';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [activeAgents, setActiveAgents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [activities, setActivities] = useState([]);
  const [certifications, setCertifications] = useState([]);
  const [securityMetrics, setSecurityMetrics] = useState({});
  const [developmentMetrics, setDevelopmentMetrics] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [agentsRes, tasksRes, activitiesRes, certsRes, secMetricsRes, devMetricsRes] = await Promise.all([
        axios.get(`${API}/agents`),
        axios.get(`${API}/tasks?status=in_progress`),
        axios.get(`${API}/activities`),
        axios.get(`${API}/certifications`),
        axios.get(`${API}/metrics/security`),
        axios.get(`${API}/metrics/development`)
      ]);

      setActiveAgents(agentsRes.data);
      setTasks(tasksRes.data);
      setActivities(activitiesRes.data);
      setCertifications(certsRes.data);
      setSecurityMetrics(secMetricsRes.data);
      setDevelopmentMetrics(devMetricsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      default: return 'bg-blue-500';
    }
  };

  const getActivityIcon = (type) => {
    switch(type) {
      case 'alert': return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'success': return <CheckCircle2 className="w-4 h-4 text-green-500" />;
      case 'warning': return <Shield className="w-4 h-4 text-yellow-500" />;
      default: return <Activity className="w-4 h-4 text-blue-500" />;
    }
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diff = Math.floor((now - time) / 1000); // in seconds
    
    if (diff < 60) return `${diff}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white flex items-center justify-center">
        <div className="text-2xl">Loading AI agents...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
          AI Cyber Security & Development Company
        </h1>
        <p className="text-slate-400">Autonomous Hive Mind Collective - Operational Status: Active</p>
      </div>

      {/* Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Shield className="w-4 h-4 mr-2 text-cyan-500" />
              Security Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-cyan-400">{securityMetrics.securityScore}%</div>
            <p className="text-xs text-slate-500 mt-1">+2.3% from last week</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <AlertTriangle className="w-4 h-4 mr-2 text-orange-500" />
              Threats Blocked
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-orange-400">{securityMetrics.threatsBlocked?.toLocaleString()}</div>
            <p className="text-xs text-slate-500 mt-1">Last 30 days</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Code className="w-4 h-4 mr-2 text-green-500" />
              Projects Completed
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-400">{developmentMetrics.projectsCompleted}</div>
            <p className="text-xs text-slate-500 mt-1">This quarter</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Users className="w-4 h-4 mr-2 text-purple-500" />
              Active Agents
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-400">{activeAgents.length}</div>
            <p className="text-xs text-slate-500 mt-1">All systems operational</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active AI Agents */}
        <div className="lg:col-span-2">
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="w-5 h-5 mr-2 text-yellow-500" />
                Active AI Agents
              </CardTitle>
              <CardDescription className="text-slate-400">Hive mind collective status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {activeAgents.map(agent => (
                  <div key={agent.agent_id} className="border border-slate-800 rounded-lg p-4 hover:border-slate-700 transition-all hover:shadow-lg hover:shadow-cyan-500/10">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center">
                        <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${agent.color} flex items-center justify-center font-bold mr-3`}>
                          {agent.avatar}
                        </div>
                        <div>
                          <h3 className="font-semibold">{agent.name}</h3>
                          <p className="text-xs text-slate-400">{agent.type}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-1">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        <span className="text-xs text-green-400">{agent.status}</span>
                      </div>
                    </div>
                    <div className="text-sm text-slate-300 mb-2">{agent.current_task}</div>
                    <div className="flex justify-between text-xs text-slate-500">
                      <span>{agent.tasks_completed} tasks</span>
                      <span className="text-cyan-400">{agent.success_rate}% success</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Active Tasks */}
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur mt-6">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Activity className="w-5 h-5 mr-2 text-cyan-500" />
                Active Tasks
              </CardTitle>
              <CardDescription className="text-slate-400">Real-time task execution</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {tasks.length === 0 ? (
                  <p className="text-slate-400 text-center py-4">No active tasks</p>
                ) : (
                  tasks.map(task => (
                    <div key={task.task_id} className="border border-slate-800 rounded-lg p-4 hover:border-slate-700 transition-all">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <div className="flex items-center mb-1">
                            <h4 className="font-medium text-sm">{task.title}</h4>
                            <Badge className={`ml-2 ${getPriorityColor(task.priority)} text-xs`}>
                              {task.priority}
                            </Badge>
                          </div>
                          <p className="text-xs text-slate-400">Assigned to: {task.agent_name || 'Assigning...'}</p>
                        </div>
                        <span className="text-xs text-slate-500">{task.eta_minutes}m</span>
                      </div>
                      <Progress value={task.progress} className="h-2" />
                      <div className="text-right text-xs text-slate-500 mt-1">{Math.round(task.progress)}%</div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recent Activity */}
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {activities.map(activity => (
                  <div key={activity.activity_id} className="flex items-start space-x-3 text-sm pb-3 border-b border-slate-800 last:border-0">
                    {getActivityIcon(activity.activity_type)}
                    <div className="flex-1">
                      <p className="text-slate-300">{activity.action}</p>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-xs text-slate-500">{activity.agent_name || activity.agent_id}</span>
                        <span className="text-xs text-slate-600">{formatTimeAgo(activity.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Certifications */}
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center">
                <CheckCircle2 className="w-5 h-5 mr-2 text-purple-500" />
                Certifications
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {certifications.map((cert, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium">{cert.name}</span>
                      <Badge className={cert.status === 'certified' ? 'bg-green-500' : 'bg-blue-500'}>
                        {cert.status === 'certified' ? 'Certified' : 'In Progress'}
                      </Badge>
                    </div>
                    <Progress value={cert.progress} className="h-2" />
                    <div className="text-xs text-slate-500 mt-1">
                      {cert.completed_modules}/{cert.total_modules} modules completed
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
