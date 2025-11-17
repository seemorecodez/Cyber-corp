# Security Posture Improvements

This document describes the security enhancements implemented in the Cyber-corp repository.

## Overview

Three major security improvements have been implemented:

1. **GitHub Dependabot** - Automated dependency vulnerability monitoring and updates
2. **License Scanning** - Automated license compliance checking for all dependencies
3. **Secure Coding Standards** - Automated security linting for Python and JavaScript code

## 1. GitHub Dependabot

### Location
`.github/dependabot.yml`

### What It Does
- Automatically scans for security vulnerabilities in dependencies
- Creates pull requests to update vulnerable dependencies
- Monitors three package ecosystems:
  - **npm** (frontend JavaScript dependencies)
  - **pip** (backend Python dependencies)
  - **GitHub Actions** (workflow dependencies)

### Configuration
- Runs weekly on Mondays at 9:00 AM
- Groups minor and patch updates to reduce PR noise
- Limits to 10 open PRs for npm/pip and 5 for GitHub Actions
- Automatically labels PRs with `dependencies` and `security` tags
- Assigns PRs to repository owner for review

### How to Use
Dependabot runs automatically. When it finds a security vulnerability:
1. It will create a pull request with the update
2. Review the PR and test the changes
3. Merge if tests pass and changes are acceptable

## 2. License Scanning

### Location
`.github/workflows/license-scan.yml`

### What It Does
Scans all project dependencies for license compliance:
- **Frontend**: Uses `license-checker` for npm packages
- **Backend**: Uses `pip-licenses` for Python packages
- Checks for restrictive licenses (GPL, AGPL) that might conflict with project goals
- Generates detailed license reports as artifacts

### When It Runs
- On pull requests that modify dependencies
- On pushes to main/master/develop branches
- Can be triggered manually via workflow_dispatch

### How to Review Results
1. Check the workflow run in GitHub Actions
2. Download the license report artifacts:
   - `frontend-license-report` - JSON format
   - `backend-license-report` - JSON and Markdown formats
3. Review any warnings about restrictive licenses
4. Ensure all licenses comply with your organization's policies

### Approved Licenses (Default)
The workflow checks for these permissive licenses in production dependencies:
- MIT
- Apache-2.0
- BSD-2-Clause
- BSD-3-Clause
- ISC
- CC0-1.0
- Unlicense
- Python-2.0

## 3. Secure Coding Standards

### Location
`.github/workflows/security-scan.yml`

### What It Does
Performs automated security scanning on all code:

#### Python Security (Bandit)
- Scans Python code for common security issues
- Configuration: `.bandit`
- Checks for:
  - SQL injection vulnerabilities
  - Use of insecure functions
  - Hardcoded passwords
  - Shell injection risks
  - And 100+ other security patterns

#### Python Code Quality (Flake8)
- Checks Python code style and quality
- Identifies syntax errors and undefined names
- Measures code complexity

#### JavaScript Security (ESLint)
- Scans JavaScript/JSX code for security issues
- Configuration: `frontend/eslint.config.mjs`
- Uses `eslint-plugin-security` to detect:
  - Unsafe regular expressions
  - eval() usage
  - Timing attacks
  - Object injection
  - Non-literal file system operations
  - And many other security patterns

### When It Runs
- On pull requests that modify Python or JavaScript files
- On pushes to main/master/develop branches
- Can be triggered manually

### How to Review Results
1. Check the workflow run in GitHub Actions
2. Review the console output for any HIGH severity issues
3. Download security report artifacts:
   - `bandit-security-report` - JSON format
   - `eslint-security-report` - JSON format
4. Address HIGH severity issues before merging

### Security Reports
All scans generate reports uploaded as artifacts:
- Retained for 30 days
- Can be downloaded from the Actions tab
- Include detailed information about each issue

## Dependencies Added

### Backend (Python)
- `bandit==1.8.0` - Security linting tool

### Frontend (JavaScript)
- `eslint-plugin-security` - ESLint security rules

## Running Scans Locally

### Python (Bandit)
```bash
cd backend
pip install bandit
bandit -r . -c ../.bandit
```

### Python (Flake8)
```bash
cd backend
pip install flake8
flake8 .
```

### JavaScript (ESLint)
```bash
cd frontend
npm install
npx eslint . --ext .js,.jsx
```

## Best Practices

1. **Review Dependabot PRs promptly** - Security updates should be applied quickly
2. **Don't ignore HIGH severity issues** - Address them before merging code
3. **Review license reports** - Ensure compliance with your organization's policies
4. **Run linters locally** - Catch issues before pushing code
5. **Keep security tools updated** - Regularly update bandit, eslint-plugin-security, etc.

## Continuous Improvement

These security measures are a foundation. Consider adding:
- SAST (Static Application Security Testing) tools like CodeQL
- Dependency scanning in pre-commit hooks
- Security policy documentation (SECURITY.md)
- Automated security testing in CI/CD pipeline
- Regular security audits

## Support

For issues or questions about security scanning:
1. Check the workflow logs in GitHub Actions
2. Review the security reports in artifacts
3. Consult the tool documentation:
   - [Bandit](https://bandit.readthedocs.io/)
   - [ESLint Security Plugin](https://github.com/eslint-community/eslint-plugin-security)
   - [Dependabot](https://docs.github.com/en/code-security/dependabot)
