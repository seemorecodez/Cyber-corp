# Tests Directory

This directory contains all automated test cases for the Cyber-corp project, including unit tests and integration tests for both frontend and backend components.

## Structure

```
tests/
├── __init__.py          # Python package initialization
├── test_backend.py      # Backend API and server tests
├── test_frontend.py     # Frontend component and integration tests (placeholder)
└── README.md           # This file
```

## Backend Tests

**File:** `test_backend.py`

Contains comprehensive tests for the backend API, including:
- Agent system endpoints (`/api/agents`)
- Task management endpoints (`/api/tasks`)
- Security scanning endpoints (`/api/security/scan`)
- Metrics and analytics endpoints (`/api/metrics`)
- Real-time WebSocket connections
- Database operations and data integrity

### Running Backend Tests

```bash
# From the project root
python tests/test_backend.py
```

Or using pytest:
```bash
pytest tests/test_backend.py -v
```

## Frontend Tests

**File:** `test_frontend.py`

Currently contains placeholder stubs. Frontend tests should be implemented to cover:
- React component rendering and behavior
- User interactions and event handling
- API integration and data fetching
- State management
- Routing and navigation

### Running Frontend Tests

For frontend-specific tests, use the React testing framework:

```bash
cd frontend
npm test
```

## Test-Driven Development (TDD)

We encourage test-driven development practices:

1. **Write tests first**: Before implementing new features, write tests that define expected behavior
2. **Run tests frequently**: Ensure existing tests pass before committing changes
3. **Maintain test coverage**: Add tests for new features and bug fixes
4. **Keep tests isolated**: Each test should be independent and not rely on external state

## Adding New Tests

### Backend Tests

Add new test methods to `test_backend.py` following the existing pattern:

```python
async def test_new_feature(self):
    """Test description"""
    # Test implementation
    pass
```

### Frontend Tests

For frontend, create test files alongside components or in a dedicated test folder:

```javascript
// frontend/src/components/__tests__/Component.test.js
import { render, screen } from '@testing-library/react';
import Component from '../Component';

test('renders component correctly', () => {
  render(<Component />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

## Continuous Integration

Tests are automatically run as part of the CI/CD pipeline. Ensure all tests pass before merging pull requests.

## Test Data and Fixtures

- Use mock data for testing to avoid dependencies on external services
- Store test fixtures in a dedicated `fixtures/` subdirectory if needed
- Clean up test data after test execution

## Coverage Reports

Generate test coverage reports to identify untested code:

```bash
# Python backend
pytest --cov=backend tests/

# JavaScript frontend
cd frontend
npm run test -- --coverage
```
