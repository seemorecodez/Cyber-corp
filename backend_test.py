#!/usr/bin/env python3
"""
Backend API Testing Suite for AI Cyber Security & Development Company
Tests all backend endpoints for functionality, data integrity, and AI integration
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, Any, List

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.created_task_id = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    async def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> tuple:
        """Make HTTP request and return status, response data"""
        try:
            url = f"{API_BASE}{endpoint}"
            kwargs = {}
            
            if data:
                kwargs['json'] = data
            if params:
                kwargs['params'] = params
                
            async with self.session.request(method, url, **kwargs) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status, response_data
                
        except Exception as e:
            return 0, {"error": str(e)}
    
    async def test_get_agents(self):
        """Test GET /api/agents - Should return 6 AI agents"""
        status, data = await self.make_request('GET', '/agents')
        
        if status == 200:
            if isinstance(data, list) and len(data) == 6:
                # Check for required fields and no _id fields
                agent_names = [agent.get('name') for agent in data]
                expected_names = ['Sentinel', 'Phoenix', 'Cipher', 'Architect', 'Validator', 'Guardian']
                
                has_all_agents = all(name in agent_names for name in expected_names)
                no_id_fields = all('_id' not in agent for agent in data)
                has_required_fields = all(
                    all(field in agent for field in ['agent_id', 'name', 'type', 'status', 'specialization'])
                    for agent in data
                )
                
                if has_all_agents and no_id_fields and has_required_fields:
                    self.log_test("GET /api/agents", True, f"Retrieved {len(data)} agents successfully", data)
                else:
                    missing_info = []
                    if not has_all_agents: missing_info.append("missing expected agents")
                    if not no_id_fields: missing_info.append("contains _id fields")
                    if not has_required_fields: missing_info.append("missing required fields")
                    self.log_test("GET /api/agents", False, f"Data validation failed: {', '.join(missing_info)}")
            else:
                self.log_test("GET /api/agents", False, f"Expected 6 agents, got {len(data) if isinstance(data, list) else 'non-list'}")
        else:
            self.log_test("GET /api/agents", False, f"HTTP {status}: {data}")
    
    async def test_get_certifications(self):
        """Test GET /api/certifications - Should return certification progress"""
        status, data = await self.make_request('GET', '/certifications')
        
        if status == 200:
            if isinstance(data, list) and len(data) > 0:
                # Check for required fields and no _id fields
                no_id_fields = all('_id' not in cert for cert in data)
                has_required_fields = all(
                    all(field in cert for field in ['name', 'progress', 'status'])
                    for cert in data
                )
                
                if no_id_fields and has_required_fields:
                    cert_names = [cert.get('name') for cert in data]
                    self.log_test("GET /api/certifications", True, f"Retrieved {len(data)} certifications: {', '.join(cert_names)}", data)
                else:
                    issues = []
                    if not no_id_fields: issues.append("contains _id fields")
                    if not has_required_fields: issues.append("missing required fields")
                    self.log_test("GET /api/certifications", False, f"Data validation failed: {', '.join(issues)}")
            else:
                self.log_test("GET /api/certifications", False, f"Expected certification list, got {type(data)}")
        else:
            self.log_test("GET /api/certifications", False, f"HTTP {status}: {data}")
    
    async def test_get_security_metrics(self):
        """Test GET /api/metrics/security - Should return security metrics"""
        status, data = await self.make_request('GET', '/metrics/security')
        
        if status == 200:
            if isinstance(data, dict):
                expected_fields = ['vulnerabilitiesFound', 'vulnerabilitiesFixed', 'threatsBlocked', 'uptime', 'securityScore']
                has_required_fields = all(field in data for field in expected_fields)
                
                if has_required_fields:
                    self.log_test("GET /api/metrics/security", True, f"Retrieved security metrics with all required fields", data)
                else:
                    missing_fields = [field for field in expected_fields if field not in data]
                    self.log_test("GET /api/metrics/security", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("GET /api/metrics/security", False, f"Expected dict, got {type(data)}")
        else:
            self.log_test("GET /api/metrics/security", False, f"HTTP {status}: {data}")
    
    async def test_create_task(self):
        """Test POST /api/tasks - Create a new security task"""
        task_data = {
            "title": "Test Security Scan",
            "description": "Run vulnerability assessment",
            "priority": "high"
        }
        
        status, data = await self.make_request('POST', '/tasks', data=task_data)
        
        if status == 200:
            if isinstance(data, dict) and 'task_id' in data:
                # Store task ID for later tests
                self.created_task_id = data['task_id']
                
                # Check for required fields and no _id fields
                required_fields = ['task_id', 'title', 'description', 'priority', 'status', 'assigned_agent_id']
                has_required_fields = all(field in data for field in required_fields)
                no_id_field = '_id' not in data
                
                if has_required_fields and no_id_field and data['status'] == 'in_progress':
                    self.log_test("POST /api/tasks", True, f"Created task {data['task_id']} assigned to {data.get('assigned_agent_id')}", data)
                else:
                    issues = []
                    if not has_required_fields: issues.append("missing required fields")
                    if not no_id_field: issues.append("contains _id field")
                    if data.get('status') != 'in_progress': issues.append("incorrect status")
                    self.log_test("POST /api/tasks", False, f"Data validation failed: {', '.join(issues)}")
            else:
                self.log_test("POST /api/tasks", False, f"Expected task object with task_id, got {type(data)}")
        else:
            self.log_test("POST /api/tasks", False, f"HTTP {status}: {data}")
    
    async def test_get_tasks_filtered(self):
        """Test GET /api/tasks?status=in_progress - Should show the created task"""
        # Wait a moment for task to be processed
        await asyncio.sleep(1)
        
        status, data = await self.make_request('GET', '/tasks', params={'status': 'in_progress'})
        
        if status == 200:
            if isinstance(data, list):
                # Check if our created task is in the list
                created_task_found = False
                if self.created_task_id:
                    created_task_found = any(task.get('task_id') == self.created_task_id for task in data)
                
                # Check for no _id fields
                no_id_fields = all('_id' not in task for task in data)
                
                if created_task_found and no_id_fields:
                    self.log_test("GET /api/tasks?status=in_progress", True, f"Found {len(data)} in_progress tasks including created task", data)
                elif not created_task_found and len(data) > 0 and no_id_fields:
                    self.log_test("GET /api/tasks?status=in_progress", True, f"Found {len(data)} in_progress tasks (created task may have completed)", data)
                else:
                    issues = []
                    if not no_id_fields: issues.append("contains _id fields")
                    if not created_task_found and len(data) == 0: issues.append("no tasks found")
                    self.log_test("GET /api/tasks?status=in_progress", False, f"Issues: {', '.join(issues)}")
            else:
                self.log_test("GET /api/tasks?status=in_progress", False, f"Expected list, got {type(data)}")
        else:
            self.log_test("GET /api/tasks?status=in_progress", False, f"HTTP {status}: {data}")
    
    async def test_hive_broadcast(self):
        """Test POST /api/hive/broadcast - Send message to hive mind"""
        broadcast_data = {
            "message": "What is the current security status?"
        }
        
        status, data = await self.make_request('POST', '/hive/broadcast', data=broadcast_data)
        
        if status == 200:
            if isinstance(data, dict):
                required_fields = ['primary_agent', 'primary_response']
                has_required_fields = all(field in data for field in required_fields)
                
                # Check if response is AI-generated (not just mock data)
                response_text = data.get('primary_response', '')
                is_ai_response = (
                    len(response_text) > 50 and  # Substantial response
                    not response_text.startswith('Mock') and  # Not mock data
                    any(word in response_text.lower() for word in ['security', 'status', 'system', 'analysis'])  # Relevant content
                )
                
                if has_required_fields and is_ai_response:
                    self.log_test("POST /api/hive/broadcast", True, f"AI response from {data['primary_agent']}: {response_text[:100]}...", data)
                else:
                    issues = []
                    if not has_required_fields: issues.append("missing required fields")
                    if not is_ai_response: issues.append("response appears to be mock data or too short")
                    self.log_test("POST /api/hive/broadcast", False, f"Issues: {', '.join(issues)}")
            else:
                self.log_test("POST /api/hive/broadcast", False, f"Expected dict, got {type(data)}")
        else:
            self.log_test("POST /api/hive/broadcast", False, f"HTTP {status}: {data}")
    
    async def test_get_hive_messages(self):
        """Test GET /api/hive/messages - Should show broadcast messages"""
        # Wait a moment for messages to be saved
        await asyncio.sleep(1)
        
        status, data = await self.make_request('GET', '/hive/messages')
        
        if status == 200:
            if isinstance(data, list):
                # Check for no _id fields and required fields
                no_id_fields = all('_id' not in msg for msg in data)
                has_required_fields = all(
                    all(field in msg for field in ['message_id', 'from_agent_id', 'to_agent_id', 'message'])
                    for msg in data
                ) if data else True
                
                if no_id_fields and has_required_fields:
                    self.log_test("GET /api/hive/messages", True, f"Retrieved {len(data)} hive messages", data)
                else:
                    issues = []
                    if not no_id_fields: issues.append("contains _id fields")
                    if not has_required_fields: issues.append("missing required fields")
                    self.log_test("GET /api/hive/messages", False, f"Issues: {', '.join(issues)}")
            else:
                self.log_test("GET /api/hive/messages", False, f"Expected list, got {type(data)}")
        else:
            self.log_test("GET /api/hive/messages", False, f"HTTP {status}: {data}")
    
    async def test_get_activities(self):
        """Test GET /api/activities - Should show recent activities"""
        status, data = await self.make_request('GET', '/activities')
        
        if status == 200:
            if isinstance(data, list):
                # Check for no _id fields and required fields
                no_id_fields = all('_id' not in activity for activity in data)
                has_required_fields = all(
                    all(field in activity for field in ['activity_id', 'agent_id', 'action', 'activity_type'])
                    for activity in data
                ) if data else True
                
                if no_id_fields and has_required_fields:
                    self.log_test("GET /api/activities", True, f"Retrieved {len(data)} activities", data)
                else:
                    issues = []
                    if not no_id_fields: issues.append("contains _id fields")
                    if not has_required_fields: issues.append("missing required fields")
                    self.log_test("GET /api/activities", False, f"Issues: {', '.join(issues)}")
            else:
                self.log_test("GET /api/activities", False, f"Expected list, got {type(data)}")
        else:
            self.log_test("GET /api/activities", False, f"HTTP {status}: {data}")
    
    async def run_all_tests(self):
        """Run all backend API tests"""
        print(f"🚀 Starting Backend API Tests")
        print(f"📡 Backend URL: {API_BASE}")
        print("=" * 80)
        
        # Test all endpoints in sequence
        await self.test_get_agents()
        await self.test_get_certifications()
        await self.test_get_security_metrics()
        await self.test_create_task()
        await self.test_get_tasks_filtered()
        await self.test_hive_broadcast()
        await self.test_get_hive_messages()
        await self.test_get_activities()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        
        return self.test_results

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        results = await tester.run_all_tests()
        
        # Save results to file
        with open('/app/backend_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to /app/backend_test_results.json")
        
        # Return exit code based on test results
        failed_count = sum(1 for result in results if not result['success'])
        return failed_count

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)