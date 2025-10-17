import React, { useState, useEffect, useRef } from 'react';
import { Send, Network, Sparkles, Brain } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const HiveMind = () => {
  const [messages, setMessages] = useState(hiveMindMessages);
  const [userMessage, setUserMessage] = useState('');
  const [activeConnections, setActiveConnections] = useState(agents.length * (agents.length - 1));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Simulate agent communication
    const interval = setInterval(() => {
      const randomAgent = agents[Math.floor(Math.random() * agents.length)];
      const actions = [
        'Processing security scan results',
        'Analyzing code patterns',
        'Updating threat intelligence',
        'Optimizing deployment pipeline',
        'Reviewing compliance requirements',
        'Coordinating with team members'
      ];
      const newMessage = {
        id: messages.length + 1,
        from: randomAgent.name,
        to: 'All',
        message: actions[Math.floor(Math.random() * actions.length)],
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, newMessage]);
    }, 8000);

    return () => clearInterval(interval);
  }, [messages.length]);

  const handleSendMessage = () => {
    if (!userMessage.trim()) return;

    const newUserMessage = {
      id: messages.length + 1,
      from: 'You',
      to: 'Hive Mind',
      message: userMessage,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      isUser: true
    };

    setMessages(prev => [...prev, newUserMessage]);
    setUserMessage('');

    // Simulate AI response
    setTimeout(() => {
      const respondingAgent = agents[Math.floor(Math.random() * agents.length)];
      const aiResponse = {
        id: messages.length + 2,
        from: respondingAgent.name,
        to: 'You',
        message: `Processing your request. The hive mind is analyzing and coordinating the best approach.`,
        timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-2 flex items-center">
          <Brain className="w-10 h-10 mr-3 text-purple-500" />
          Hive Mind Collective
        </h1>
        <p className="text-slate-400">Real-time inter-agent communication and collaboration</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Network Status */}
        <div className="lg:col-span-1">
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur mb-6">
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <Network className="w-5 h-5 mr-2 text-cyan-500" />
                Network Status
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-slate-400 mb-1">Active Connections</p>
                  <p className="text-3xl font-bold text-cyan-400">{activeConnections}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400 mb-1">Network Latency</p>
                  <p className="text-2xl font-bold text-green-400">0.8ms</p>
                </div>
                <div>
                  <p className="text-sm text-slate-400 mb-1">Sync Status</p>
                  <Badge className="bg-green-500">Synchronized</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur">
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <Sparkles className="w-5 h-5 mr-2 text-yellow-500" />
                Connected Agents
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {agents.map(agent => (
                  <div key={agent.id} className="flex items-center justify-between p-2 rounded bg-slate-800/50">
                    <div className="flex items-center">
                      <div className={`w-8 h-8 rounded-full bg-gradient-to-br ${agent.color} flex items-center justify-center text-xs font-bold mr-2`}>
                        {agent.avatar}
                      </div>
                      <span className="text-sm">{agent.name}</span>
                    </div>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Communication Hub */}
        <div className="lg:col-span-3">
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur h-[calc(100vh-200px)] flex flex-col">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Network className="w-5 h-5 mr-2 text-purple-500" />
                Collective Communication Hub
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto mb-4 space-y-3 pr-2">
                {messages.map(msg => (
                  <div key={msg.id} className={`p-3 rounded-lg ${
                    msg.isUser 
                      ? 'bg-blue-900/30 border border-blue-800 ml-12' 
                      : 'bg-slate-800/50 border border-slate-700 mr-12'
                  }`}>
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center">
                        <span className={`font-semibold text-sm ${
                          msg.isUser ? 'text-blue-400' : 'text-cyan-400'
                        }`}>
                          {msg.from}
                        </span>
                        <span className="text-slate-500 text-xs mx-2">→</span>
                        <span className="text-slate-400 text-xs">{msg.to}</span>
                      </div>
                      <span className="text-xs text-slate-500">{msg.timestamp}</span>
                    </div>
                    <p className="text-sm text-slate-300">{msg.message}</p>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <div className="flex space-x-2 border-t border-slate-800 pt-4">
                <Input
                  value={userMessage}
                  onChange={(e) => setUserMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Send instruction to the hive mind..."
                  className="flex-1 bg-slate-800 border-slate-700 text-white placeholder:text-slate-500"
                />
                <Button 
                  onClick={handleSendMessage}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HiveMind;
