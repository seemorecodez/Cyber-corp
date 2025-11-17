# GitHub Actions Workflows

This directory contains the CI/CD workflows for the Cyber-corp project.

## Workflows

### 1. Unit Tests (`unit-tests.yml`)

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

**Note**: Tests continue even if they fail to allow viewing of test results.

### 2. Code Quality Checks (`code-quality.yml`)

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
- Allows up to 50 warnings before failing

#### Flake8 (Backend)
- Runs flake8 on Python files in the backend directory
- Checks for syntax errors and critical issues (E9, F63, F7, F82)
- Performs complexity and line length checks
- Also checks `backend_test.py` file

**Note**: Both jobs continue on error to provide visibility into code quality without blocking deployment.

### 3. Deployment Pipeline (`deploy.yml`)

**Purpose**: Automates deployment to GitHub Pages

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

#### Verify Deployment Job
1. Waits 30 seconds for deployment to propagate
2. Verifies deployment is accessible via HTTP request
3. Continues on error (useful if GitHub Pages isn't enabled yet)

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

### For Deployment
- GitHub Pages must be enabled in repository settings
- Set GitHub Pages source to "GitHub Actions"
- Node.js 20
- Frontend dependencies

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
