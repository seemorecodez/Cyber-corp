# GitHub Actions Workflows

This directory contains the CI/CD workflows for the Cyber-corp project.

## 🎯 Automation Overview

**7 Workflows** providing comprehensive quality gates, security automation, and deployment:

1. **Unit Tests** - STRICT mode (blocks on failure)
2. **Code Quality** - ZERO tolerance (no warnings allowed)
3. **Security Scanning** - Multi-layer security (5 tools)
4. **Test Coverage** - Coverage tracking with PR comments
5. **PR Quality Gate** - Enforces standards and aggregates checks
6. **Deployment** - Automated with enhanced verification
7. **Scheduled Scans** - Daily security audits

**📚 For complete guide, see [AUTOMATION_GUIDE.md](./AUTOMATION_GUIDE.md)**

---

## Workflows

### 1. Unit Tests (`unit-tests.yml`) ⚠️ STRICT MODE

**Purpose**: Automates testing for `backend_test.py`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual dispatch

**What it does**:
- Sets up Python 3.12 environment
- Installs backend dependencies from `backend/requirements.txt`
- Creates required environment files for tests
- Runs backend unit tests
- Uploads test results as artifacts

**⚠️ BREAKING CHANGE**: Tests now BLOCK the PR if they fail. No `continue-on-error` - all tests must pass.

### 2. Code Quality Checks (`code-quality.yml`) ⚠️ ZERO TOLERANCE

**Purpose**: Ensures code quality standards are maintained

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual dispatch

**What it does**:

#### ESLint (Frontend)
- Runs ESLint on JavaScript/JSX files in the frontend
- Checks for code quality issues, React best practices, and accessibility concerns
- Configured with custom rules in `frontend/eslint.config.js`
- **⚠️ CHANGED**: Now requires ZERO warnings (`--max-warnings 0`)

#### Flake8 (Backend)
- Runs flake8 on Python files in the backend directory
- Checks for syntax errors and critical issues (E9, F63, F7, F82)
- Performs complexity and line length checks
- Also checks `backend_test.py` file
- **⚠️ CHANGED**: Removed `--exit-zero` and `continue-on-error` - violations now BLOCK

### 3. Security Scanning (`security.yml`) 🔒 NEW

**Purpose**: Multi-layer security vulnerability detection

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Daily at 2 AM UTC (scheduled)
- Manual dispatch

**What it does**:

#### Dependency Scanning
- **Python**: Safety tool checks for CVEs in backend dependencies
- **JavaScript**: npm audit scans frontend packages
- Uploads security reports as artifacts

#### CodeQL Analysis
- Static analysis for Python and JavaScript
- Security-and-quality query suite
- Results appear in Security tab
- Checks against OWASP Top 10

#### Secret Detection
- TruffleHog scans entire git history
- Detects accidentally committed secrets
- Only reports verified secrets

#### Bandit Security Linting
- Python-specific security analysis
- Detects SQL injection, weak crypto, hardcoded passwords
- Uploads detailed reports

#### License Compliance
- Scans all dependencies for license compatibility
- Generates compliance reports

### 4. Test Coverage (`test-coverage.yml`) 📊 NEW

**Purpose**: Track test coverage metrics

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual dispatch

**What it does**:

#### Backend Coverage
- pytest with coverage plugin
- Generates XML and HTML reports
- Auto-comments coverage % on PRs
- Thresholds: 🟢 ≥80%, 🟠 60-79%, 🔴 <60%

#### Frontend Coverage
- Jest test coverage for React
- Coverage reports as artifacts
- Tracks statement, branch, function, line coverage

### 5. PR Quality Gate (`pr-quality-gate.yml`) ✅ NEW

**Purpose**: Enforce PR standards and aggregate all checks

**Triggers**:
- Pull requests to `main` or `develop` branches

**What it does**:
- **Conventional Commits**: Validates PR title format (feat:, fix:, etc.)
- **Description Check**: Requires meaningful description (≥20 chars)
- **Large File Detection**: Warns about files >1MB
- **Console Statement Check**: Flags console.log in production code
- **TODO Detection**: Warns about unfinished work
- **Workflow Aggregation**: Waits for all checks to complete
- **Quality Summary**: Auto-generates PR summary with ✅/❌

### 6. Deployment Pipeline (`deploy.yml`) 🚀 ENHANCED

**Purpose**: Automates deployment to GitHub Pages with enhanced verification

**Triggers**:
- Push to `main` branch only
- Manual dispatch

**What it does**:

#### Build Frontend Job
1. Sets up Node.js 20 environment
2. Installs frontend dependencies with legacy peer deps support
3. Fixes ajv dependency issue
4. Builds the React application for production
5. Uploads build artifacts

#### Deploy to Pages Job
1. Downloads build artifacts
2. Configures GitHub Pages
3. Uploads build to GitHub Pages
4. Deploys to GitHub Pages hosting
5. Outputs deployment URL

#### Verify Deployment Job 🆕 ENHANCED
1. **HTTP Status**: Verifies 200/304 response
2. **Resource Check**: Validates main.js, main.css, index.html exist
3. **Performance Test**: Measures page load time (should be <3s)
4. **Link Validation**: Checks critical resources are accessible

#### Rollback on Failure Job
1. Triggers only if deployment or verification fails
2. Provides instructions for manual rollback:
   - Revert the last commit
   - Re-run a previous successful workflow
   - Deploy from a previous release tag

**Permissions**: 
- Read access to repository contents
- Write access to GitHub Pages
- ID token for GitHub Pages deployment

**Concurrency**: 
- Only one deployment at a time
- Doesn't cancel in-progress deployments

---

---

## Setup Requirements

### For Unit Tests
- Python 3.12
- Backend dependencies (installed from `backend/requirements.txt`)
- Environment file with `REACT_APP_BACKEND_URL`

### For Code Quality Checks
- Node.js 20 (for ESLint)
- Python 3.12 (for flake8)
- Frontend dependencies
- ESLint configuration in `frontend/eslint.config.js`

### For Security Scanning 🆕
- Python 3.12 with Safety, Bandit
- Node.js 20 for npm audit
- CodeQL enabled (automatic)
- TruffleHog secret scanning
- GitHub Advanced Security (for CodeQL results in UI)

### For Test Coverage 🆕
- Python: pytest, pytest-cov, pytest-asyncio
- Node.js: Jest (included in react-scripts)
- PR write permissions for coverage comments

### For Deployment
- GitHub Pages must be enabled in repository settings
- Set GitHub Pages source to "GitHub Actions"
- Node.js 20
- Frontend dependencies

---

## 🚨 Breaking Changes

**These workflows now BLOCK PRs instead of just reporting:**

1. **Unit Tests**: Removed `continue-on-error` - tests must pass
2. **ESLint**: Changed from `--max-warnings 50` to `--max-warnings 0`
3. **Flake8**: Removed `--exit-zero` - violations cause failures

**Migration Steps:**
1. Fix all existing test failures before enabling
2. Address all ESLint warnings in codebase
3. Fix all flake8 violations in Python code
4. Then enable branch protection rules

---

## Quick Start

### Enable Branch Protection
1. Go to Settings → Branches → Add rule
2. Apply to `main` branch
3. Enable "Require status checks to pass"
4. Select all workflow checks
5. Enable "Require branches to be up to date"

### Enable GitHub Pages
1. Go to Settings → Pages
2. Source → "GitHub Actions"
3. Save

### View Security Results
1. Security tab → Code scanning alerts (CodeQL)
2. Security tab → Secret scanning alerts (TruffleHog)
3. Actions tab → Download artifact reports

---

## Manual Triggers

All workflows can be triggered manually:
1. Go to the "Actions" tab in GitHub
2. Select the workflow you want to run
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

## Viewing Results

### Test Results
- Check the Actions tab for test execution logs
- Download test result artifacts for detailed analysis
- View `backend_test_results.json` for complete test data

### Code Quality Reports
- View ESLint output in the workflow logs
- Check flake8 output for Python code quality issues
- Both tools provide line numbers and descriptions of issues

### Deployment Status
- Check the deployment URL in workflow output
- Visit `https://[username].github.io/Cyber-corp/` to see deployed site
- Review deployment logs for any issues

## Troubleshooting

### Unit Tests Failing
1. Check if backend service is required (tests may need a running backend)
2. Verify environment variables are correctly set
3. Review test logs for specific failures

### Code Quality Issues
1. Run ESLint locally: `cd frontend && npx eslint "src/**/*.{js,jsx}"`
2. Run flake8 locally: `flake8 backend/`
3. Fix issues before pushing

### Deployment Failures
1. Check build logs for compilation errors
2. Verify GitHub Pages is enabled in repository settings
3. Ensure all dependencies are correctly installed
4. Check for broken links or missing assets

### Dependency Installation Issues
- The workflows use `--legacy-peer-deps` flag to handle peer dependency conflicts
- If issues persist, delete `node_modules` and `package-lock.json` and reinstall
- Consider updating incompatible packages

## Future Enhancements

Potential improvements to consider:
- Add integration tests
- Implement automated security scanning
- Add performance testing
- Set up staging environment deployments
- Add Slack/Discord notifications for deployment status
- Implement automatic rollback on failed health checks
- Add code coverage reporting
- Cache dependencies for faster builds
