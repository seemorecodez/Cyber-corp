import React, { useState, useEffect } from 'react';
import { TrendingUp, Activity, Shield, Code, Clock, Target, Zap, Award } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Analytics = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [agentPerformance, setAgentPerformance] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [dashboardRes, performanceRes] = await Promise.all([
        axios.get(`${API}/analytics/dashboard`),
        axios.get(`${API}/analytics/agent-performance`)
      ]);

      setDashboardData(dashboardRes.data);
      setAgentPerformance(performanceRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  if (loading || !dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white flex items-center justify-center">
        <div className="text-2xl">Loading Analytics...</div>
      </div>
    );
  }

  const COLORS = ['#06b6d4', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#3b82f6'];

  const taskDistribution = [
    { name: 'Completed', value: dashboardData.tasks.completed },
    { name: 'In Progress', value: dashboardData.tasks.in_progress },
    { name: 'Failed', value: dashboardData.tasks.failed }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-2">
          Advanced Analytics Dashboard
        </h1>
        <p className="text-slate-400">Comprehensive system performance and insights</p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Target className="w-4 h-4 mr-2 text-cyan-500" />
              Task Success Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-cyan-400">
              {dashboardData.tasks.success_rate.toFixed(1)}%
            </div>
            <Progress value={dashboardData.tasks.success_rate} className="h-2 mt-2" />
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Zap className="w-4 h-4 mr-2 text-yellow-500" />
              Total Tasks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-yellow-400">{dashboardData.tasks.total}</div>
            <p className="text-xs text-slate-500 mt-1">{dashboardData.tasks.completed} completed</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Activity className="w-4 h-4 mr-2 text-green-500" />
              Activities (24h)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-400">{dashboardData.activity.last_24h}</div>
            <p className="text-xs text-slate-500 mt-1">Agent actions tracked</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-slate-400 flex items-center">
              <Award className="w-4 h-4 mr-2 text-purple-500" />
              Certifications
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-400">{dashboardData.certifications.certified}</div>
            <p className="text-xs text-slate-500 mt-1">{dashboardData.certifications.in_progress} in progress</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Agent Performance Chart */}
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-cyan-500" />
              Agent Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={agentPerformance}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                  labelStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Bar dataKey="tasks_completed" fill="#06b6d4" name="Tasks Completed" />
                <Bar dataKey="success_rate" fill="#10b981" name="Success Rate %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Task Distribution */}
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="w-5 h-5 mr-2 text-purple-500" />
              Task Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={taskDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {taskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Agent Performance Table */}
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
        <CardHeader>
          <CardTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2 text-green-500" />
            Detailed Agent Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left p-3 text-slate-400">Agent</th>
                  <th className="text-left p-3 text-slate-400">Type</th>
                  <th className="text-right p-3 text-slate-400">Completed</th>
                  <th className="text-right p-3 text-slate-400">Failed</th>
                  <th className="text-right p-3 text-slate-400">Success Rate</th>
                  <th className="text-right p-3 text-slate-400">Avg Time (min)</th>
                </tr>
              </thead>
              <tbody>
                {agentPerformance.map((agent, index) => (
                  <tr key={index} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
                    <td className="p-3 font-medium text-cyan-400">{agent.name}</td>
                    <td className="p-3 text-slate-300">{agent.type}</td>
                    <td className="p-3 text-right text-green-400">{agent.tasks_completed}</td>
                    <td className="p-3 text-right text-red-400">{agent.tasks_failed}</td>
                    <td className="p-3 text-right">
                      <span className={`font-semibold ${agent.success_rate >= 95 ? 'text-green-400' : 'text-yellow-400'}`}>
                        {agent.success_rate}%
                      </span>
                    </td>
                    <td className="p-3 text-right text-slate-400">{agent.avg_completion_time_minutes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <Code className="w-5 h-5 mr-2 text-blue-500" />
              Agent Stats
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Total Agents</span>
                <span className="font-bold text-blue-400">{dashboardData.agents.total}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Active Agents</span>
                <span className="font-bold text-green-400">{dashboardData.agents.active}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Total Tasks Done</span>
                <span className="font-bold text-cyan-400">{dashboardData.agents.total_tasks_completed}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Avg Success Rate</span>
                <span className="font-bold text-purple-400">{dashboardData.agents.average_success_rate}%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <Clock className="w-5 h-5 mr-2 text-orange-500" />
              Task Breakdown
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Completed</span>
                <div className="flex items-center space-x-2">
                  <Progress value={(dashboardData.tasks.completed / dashboardData.tasks.total) * 100} className="w-24 h-2" />
                  <span className="font-bold text-green-400">{dashboardData.tasks.completed}</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">In Progress</span>
                <div className="flex items-center space-x-2">
                  <Progress value={(dashboardData.tasks.in_progress / dashboardData.tasks.total) * 100} className="w-24 h-2" />
                  <span className="font-bold text-yellow-400">{dashboardData.tasks.in_progress}</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Failed</span>
                <div className="flex items-center space-x-2">
                  <Progress value={(dashboardData.tasks.failed / dashboardData.tasks.total) * 100} className="w-24 h-2" />
                  <span className="font-bold text-red-400">{dashboardData.tasks.failed}</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <Shield className="w-5 h-5 mr-2 text-cyan-500" />
              System Health
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400">Status</span>
                <span className="font-bold text-green-400">Operational</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Uptime</span>
                <span className="font-bold text-cyan-400">99.97%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Avg Response</span>
                <span className="font-bold text-blue-400">1.2s</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Success Rate</span>
                <span className="font-bold text-purple-400">{dashboardData.agents.average_success_rate}%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Analytics;
