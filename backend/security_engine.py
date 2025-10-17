"""
Advanced AI-powered security and threat analysis system
Provides real vulnerability scanning, threat detection, and security analysis
"""
import asyncio
import re
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

class SecurityAnalyzer:
    """Advanced security analysis engine"""
    
    # Real vulnerability patterns (simplified for MVP, expandable)
    VULNERABILITY_PATTERNS = {
        'sql_injection': [
            r'SELECT.*FROM.*WHERE',
            r'INSERT\s+INTO',
            r'UPDATE.*SET',
            r'DELETE\s+FROM',
            r'DROP\s+TABLE',
            r'UNION\s+SELECT'
        ],
        'xss': [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'onerror\s*=',
            r'onload\s*=',
            r'<iframe'
        ],
        'command_injection': [
            r'\|.*ls',
            r'\|.*cat',
            r'&&.*rm',
            r';.*wget',
            r'`.*`'
        ],
        'path_traversal': [
            r'\.\./\.\.',
            r'%2e%2e%2f',
            r'\.\.\\\\',
        ],
        'weak_crypto': [
            r'md5\(',
            r'sha1\(',
            r'des\(',
            r'rc4\('
        ]
    }
    
    THREAT_SIGNATURES = {
        'brute_force': {'threshold': 5, 'timeframe': 60},
        'ddos': {'threshold': 100, 'timeframe': 10},
        'port_scan': {'threshold': 20, 'timeframe': 30},
        'malware': {'patterns': ['eval(', 'exec(', 'system(', 'shell_exec(']}
    }
    
    def __init__(self):
        self.vulnerability_cache = {}
        self.threat_history = []
        self.blocked_ips = set()
        
    async def scan_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """Scan code for security vulnerabilities"""
        vulnerabilities = []
        
        for vuln_type, patterns in self.VULNERABILITY_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    vulnerabilities.append({
                        'type': vuln_type,
                        'severity': self._calculate_severity(vuln_type),
                        'line': code[:match.start()].count('\n') + 1,
                        'pattern': pattern,
                        'matched_text': match.group(0),
                        'recommendation': self._get_recommendation(vuln_type)
                    })
        
        # Calculate security score
        security_score = 100 - min(len(vulnerabilities) * 5, 50)
        
        return {
            'vulnerabilities': vulnerabilities,
            'total_found': len(vulnerabilities),
            'security_score': security_score,
            'scan_timestamp': datetime.utcnow().isoformat(),
            'language': language
        }
    
    async def detect_threats(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Real-time threat detection"""
        threats = []
        
        ip = request_data.get('ip', 'unknown')
        user_agent = request_data.get('user_agent', '')
        payload = request_data.get('payload', '')
        
        # Check for known malware patterns
        for pattern in self.THREAT_SIGNATURES['malware']['patterns']:
            if pattern in payload:
                threats.append({
                    'type': 'malware',
                    'severity': 'critical',
                    'description': f'Malicious pattern detected: {pattern}',
                    'action': 'blocked'
                })
                self.blocked_ips.add(ip)
        
        # Check for brute force attempts
        recent_attempts = [t for t in self.threat_history 
                          if t.get('ip') == ip and 
                          (datetime.utcnow() - t['timestamp']).seconds < 60]
        
        if len(recent_attempts) >= 5:
            threats.append({
                'type': 'brute_force',
                'severity': 'high',
                'description': f'Multiple failed attempts from {ip}',
                'action': 'rate_limited'
            })
        
        # Store in history
        self.threat_history.append({
            'ip': ip,
            'timestamp': datetime.utcnow(),
            'threats': len(threats)
        })
        
        return {
            'threats_detected': len(threats),
            'threats': threats,
            'blocked': ip in self.blocked_ips,
            'risk_level': self._calculate_risk_level(threats)
        }
    
    async def analyze_network_traffic(self, traffic_data: List[Dict]) -> Dict[str, Any]:
        """Analyze network traffic for anomalies"""
        anomalies = []
        total_requests = len(traffic_data)
        
        if not traffic_data:
            return {
                'anomalies': [],
                'total_analyzed': 0,
                'risk_score': 0
            }
        
        # Analyze patterns
        ip_frequency = {}
        for request in traffic_data:
            ip = request.get('ip', 'unknown')
            ip_frequency[ip] = ip_frequency.get(ip, 0) + 1
        
        # Detect suspicious IPs
        avg_requests = sum(ip_frequency.values()) / len(ip_frequency) if ip_frequency else 0
        for ip, count in ip_frequency.items():
            if count > avg_requests * 3:  # 3x average is suspicious
                anomalies.append({
                    'type': 'suspicious_activity',
                    'ip': ip,
                    'request_count': count,
                    'severity': 'medium'
                })
        
        return {
            'anomalies': anomalies,
            'total_analyzed': total_requests,
            'unique_ips': len(ip_frequency),
            'risk_score': min(len(anomalies) * 10, 100)
        }
    
    async def check_compliance(self, system_config: Dict[str, Any], standards: List[str]) -> Dict[str, Any]:
        """Check compliance with security standards"""
        compliance_results = {}
        
        for standard in standards:
            if standard == 'GDPR':
                compliance_results['GDPR'] = self._check_gdpr_compliance(system_config)
            elif standard == 'HIPAA':
                compliance_results['HIPAA'] = self._check_hipaa_compliance(system_config)
            elif standard == 'SOC2':
                compliance_results['SOC2'] = self._check_soc2_compliance(system_config)
            elif standard == 'ISO27001':
                compliance_results['ISO27001'] = self._check_iso27001_compliance(system_config)
        
        # Calculate overall compliance score
        total_checks = sum(r['total_checks'] for r in compliance_results.values())
        passed_checks = sum(r['passed_checks'] for r in compliance_results.values())
        
        return {
            'standards': compliance_results,
            'overall_score': (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'assessment_date': datetime.utcnow().isoformat()
        }
    
    def _calculate_severity(self, vuln_type: str) -> str:
        """Calculate vulnerability severity"""
        severity_map = {
            'sql_injection': 'critical',
            'xss': 'high',
            'command_injection': 'critical',
            'path_traversal': 'high',
            'weak_crypto': 'medium'
        }
        return severity_map.get(vuln_type, 'low')
    
    def _get_recommendation(self, vuln_type: str) -> str:
        """Get remediation recommendation"""
        recommendations = {
            'sql_injection': 'Use parameterized queries or prepared statements',
            'xss': 'Implement input sanitization and output encoding',
            'command_injection': 'Avoid using shell commands with user input',
            'path_traversal': 'Validate and sanitize file paths',
            'weak_crypto': 'Use modern cryptographic algorithms (AES-256, SHA-256)'
        }
        return recommendations.get(vuln_type, 'Review and update security measures')
    
    def _calculate_risk_level(self, threats: List[Dict]) -> str:
        """Calculate overall risk level"""
        if not threats:
            return 'low'
        
        critical = sum(1 for t in threats if t.get('severity') == 'critical')
        high = sum(1 for t in threats if t.get('severity') == 'high')
        
        if critical > 0:
            return 'critical'
        elif high > 0:
            return 'high'
        elif len(threats) > 2:
            return 'medium'
        return 'low'
    
    def _check_gdpr_compliance(self, config: Dict) -> Dict:
        """Check GDPR compliance"""
        checks = {
            'data_encryption': config.get('encryption_enabled', False),
            'data_retention_policy': config.get('retention_policy', False),
            'user_consent': config.get('consent_management', False),
            'data_portability': config.get('data_export', False),
            'right_to_erasure': config.get('data_deletion', False)
        }
        passed = sum(1 for v in checks.values() if v)
        return {
            'passed_checks': passed,
            'total_checks': len(checks),
            'checks': checks,
            'compliant': passed >= len(checks) * 0.8
        }
    
    def _check_hipaa_compliance(self, config: Dict) -> Dict:
        """Check HIPAA compliance"""
        checks = {
            'access_controls': config.get('access_controls', False),
            'audit_logging': config.get('audit_logs', False),
            'data_encryption': config.get('encryption_enabled', False),
            'backup_recovery': config.get('backup_enabled', False)
        }
        passed = sum(1 for v in checks.values() if v)
        return {
            'passed_checks': passed,
            'total_checks': len(checks),
            'checks': checks,
            'compliant': passed >= len(checks) * 0.8
        }
    
    def _check_soc2_compliance(self, config: Dict) -> Dict:
        """Check SOC 2 compliance"""
        checks = {
            'security_monitoring': config.get('monitoring_enabled', False),
            'availability': config.get('high_availability', False),
            'processing_integrity': config.get('data_validation', False),
            'confidentiality': config.get('encryption_enabled', False),
            'privacy': config.get('privacy_controls', False)
        }
        passed = sum(1 for v in checks.values() if v)
        return {
            'passed_checks': passed,
            'total_checks': len(checks),
            'checks': checks,
            'compliant': passed >= len(checks) * 0.8
        }
    
    def _check_iso27001_compliance(self, config: Dict) -> Dict:
        """Check ISO 27001 compliance"""
        checks = {
            'risk_assessment': config.get('risk_assessment', False),
            'security_policy': config.get('security_policy', False),
            'incident_response': config.get('incident_response', False),
            'access_management': config.get('access_controls', False)
        }
        passed = sum(1 for v in checks.values() if v)
        return {
            'passed_checks': passed,
            'total_checks': len(checks),
            'checks': checks,
            'compliant': passed >= len(checks) * 0.8
        }

# Global security analyzer instance
security_analyzer = SecurityAnalyzer()
