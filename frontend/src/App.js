import './App.css';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Shield, Network, Code2, Home, Menu, X, BarChart3 } from 'lucide-react';
import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import HiveMind from './pages/HiveMind';
import Projects from './pages/Projects';
import Analytics from './pages/Analytics';

const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/hive-mind', icon: Network, label: 'Hive Mind' },
    { path: '/projects', icon: Code2, label: 'Projects' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' }
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-slate-900/80 backdrop-blur-lg border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-white">CyberAI Corp</h1>
                <p className="text-xs text-slate-400">Autonomous Security & Dev</p>
              </div>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center space-x-2 transition-all ${
                    isActive(item.path)
                      ? 'bg-cyan-600 text-white'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-slate-300 hover:text-white p-2"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-800">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-3 py-2 rounded-lg text-base font-medium flex items-center space-x-2 ${
                  isActive(item.path)
                    ? 'bg-cyan-600 text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

function App() {
  return (
    <div className="App min-h-screen bg-slate-950">
      <BrowserRouter>
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/hive-mind" element={<HiveMind />} />
          <Route path="/projects" element={<Projects />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
