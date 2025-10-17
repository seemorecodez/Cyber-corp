import React, { useState } from 'react';
import { Code2, GitBranch, PlayCircle, CheckCircle2, Clock, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';

const Projects = () => {
  const [activeProjects] = useState([
    {
      id: 1,
      name: 'SecureBank API',
      type: 'Backend Development',
      status: 'In Progress',
      progress: 67,
      agent: 'Architect',
      tech: ['Node.js', 'PostgreSQL', 'Redis'],
      security: 94,
      tests: 156,
      testsPassed: 152
    },
    {
      id: 2,
      name: 'E-Commerce Platform',
      type: 'Full Stack',
      status: 'Testing',
      progress: 89,
      agent: 'Architect & Phoenix',
      tech: ['React', 'FastAPI', 'MongoDB'],
      security: 98,
      tests: 234,
      testsPassed: 234
    },
    {
      id: 3,
      name: 'Mobile Healthcare App',
      type: 'Mobile Development',
      status: 'In Progress',
      progress: 45,
      agent: 'Architect',
      tech: ['React Native', 'Firebase'],
      security: 91,
      tests: 89,
      testsPassed: 84
    }
  ]);

  const [completedProjects] = useState([
    {
      id: 4,
      name: 'Insurance Portal',
      completedDate: '2025-07-15',
      agent: 'Architect',
      securityScore: 96,
      linesOfCode: 45000
    },
    {
      id: 5,
      name: 'IoT Management System',
      completedDate: '2025-07-10',
      agent: 'Architect & Cipher',
      securityScore: 98,
      linesOfCode: 62000
    },
    {
      id: 6,
      name: 'Legal Document AI',
      completedDate: '2025-07-05',
      agent: 'Architect',
      securityScore: 95,
      linesOfCode: 38000
    }
  ]);

  const [securityScans] = useState([
    { name: 'SQL Injection', status: 'Passed', severity: 'Critical' },
    { name: 'XSS Prevention', status: 'Passed', severity: 'High' },
    { name: 'CSRF Protection', status: 'Passed', severity: 'High' },
    { name: 'Authentication', status: 'Passed', severity: 'Critical' },
    { name: 'Data Encryption', status: 'Passed', severity: 'Critical' },
    { name: 'API Rate Limiting', status: 'Warning', severity: 'Medium' }
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent mb-2 flex items-center">
          <Code2 className="w-10 h-10 mr-3 text-green-500" />
          Development Projects
        </h1>
        <p className="text-slate-400">AI-powered software development and deployment</p>
      </div>

      <Tabs defaultValue="active" className="w-full">
        <TabsList className="bg-slate-900 border border-slate-800 mb-6">
          <TabsTrigger value="active" className="data-[state=active]:bg-slate-800">Active Projects</TabsTrigger>
          <TabsTrigger value="completed" className="data-[state=active]:bg-slate-800">Completed</TabsTrigger>
          <TabsTrigger value="security" className="data-[state=active]:bg-slate-800">Security Scans</TabsTrigger>
        </TabsList>

        <TabsContent value="active">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {activeProjects.map(project => (
              <Card key={project.id} className="bg-slate-900/50 border-slate-800 backdrop-blur hover:border-slate-700 transition-all">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-xl mb-2">{project.name}</CardTitle>
                      <p className="text-sm text-slate-400">{project.type}</p>
                    </div>
                    <Badge className="bg-blue-600">{project.status}</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-400">Overall Progress</span>
                        <span className="text-sm font-semibold text-cyan-400">{project.progress}%</span>
                      </div>
                      <Progress value={project.progress} className="h-2" />
                    </div>

                    <div className="flex items-center space-x-2">
                      <PlayCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm text-slate-300">Assigned to: {project.agent}</span>
                    </div>

                    <div>
                      <p className="text-sm text-slate-400 mb-2">Technology Stack</p>
                      <div className="flex flex-wrap gap-2">
                        {project.tech.map(tech => (
                          <Badge key={tech} className="bg-slate-800 text-slate-300">{tech}</Badge>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-800">
                      <div>
                        <p className="text-xs text-slate-500">Security Score</p>
                        <p className="text-2xl font-bold text-green-400">{project.security}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-slate-500">Tests Passed</p>
                        <p className="text-2xl font-bold text-cyan-400">{project.testsPassed}/{project.tests}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="completed">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {completedProjects.map(project => (
              <Card key={project.id} className="bg-slate-900/50 border-slate-800 backdrop-blur hover:border-green-900 transition-all">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center">
                    <CheckCircle2 className="w-5 h-5 mr-2 text-green-500" />
                    {project.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center text-sm">
                      <Clock className="w-4 h-4 mr-2 text-slate-400" />
                      <span className="text-slate-400">Completed: {project.completedDate}</span>
                    </div>
                    <div className="flex items-center text-sm">
                      <GitBranch className="w-4 h-4 mr-2 text-slate-400" />
                      <span className="text-slate-400">{project.agent}</span>
                    </div>
                    <div className="pt-3 border-t border-slate-800">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm text-slate-400">Security Score</span>
                        <span className="text-lg font-bold text-green-400">{project.securityScore}%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-400">Lines of Code</span>
                        <span className="text-lg font-bold text-cyan-400">{project.linesOfCode.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="security">
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-cyan-500" />
                Latest Security Scan Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {securityScans.map((scan, index) => (
                  <div key={index} className="flex items-center justify-between p-4 rounded-lg bg-slate-800/50 border border-slate-700">
                    <div className="flex items-center space-x-3">
                      {scan.status === 'Passed' ? (
                        <CheckCircle2 className="w-5 h-5 text-green-500" />
                      ) : (
                        <Clock className="w-5 h-5 text-yellow-500" />
                      )}
                      <div>
                        <p className="font-medium">{scan.name}</p>
                        <p className="text-xs text-slate-400">Severity: {scan.severity}</p>
                      </div>
                    </div>
                    <Badge className={scan.status === 'Passed' ? 'bg-green-600' : 'bg-yellow-600'}>
                      {scan.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Projects;
