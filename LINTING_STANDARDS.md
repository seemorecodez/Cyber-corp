# Code Quality and Linting Standards

This document outlines the code quality standards and linting configurations for the Cyber-corp project.

## Python Code Standards

### Linting Tool: flake8

We use `flake8` for Python code linting with the following configuration:

- **Max line length**: 120 characters
- **Style guide**: PEP 8

### Running Python Linting Locally

```bash
cd backend
python -m flake8 --max-line-length=120 --count --statistics *.py
```

### Fixing Python Issues Automatically

```bash
cd backend
python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 *.py
```

### Python Best Practices

1. **Remove unused imports**: Keep imports clean and remove any unused ones
2. **Follow PEP 8**: Use 2 blank lines between top-level definitions
3. **No trailing whitespace**: Clean up whitespace at the end of lines
4. **Use descriptive variable names**: Avoid single-letter variables except in loops

## JavaScript Code Standards

### Linting Tool: ESLint

We use ESLint v9 with the following plugins:
- `eslint-plugin-react` - React-specific linting rules
- `eslint-plugin-react-hooks` - Rules for React Hooks
- `eslint-plugin-jsx-a11y` - Accessibility rules
- `eslint-plugin-import` - Import/export syntax validation

### Running JavaScript Linting Locally

```bash
cd frontend
npx eslint src/**/*.js src/*.js
```

### ESLint Configuration

The ESLint configuration is defined in `frontend/eslint.config.js` with:
- React 17+ support (no need for React in scope)
- Prop-types disabled (we use TypeScript or runtime validation elsewhere)
- Unused variables prefixed with `_` are allowed
- Console statements are allowed

### JavaScript Best Practices

1. **Use `const` and `let`**: Avoid `var`
2. **Remove unused variables**: Clean up unused code
3. **Follow React Hooks rules**: Ensure hooks are used correctly
4. **Accessibility**: Follow a11y guidelines for accessible UI

## Code Duplication

We use `jscpd` to detect code duplication across Python and JavaScript files.

### Running Duplication Check Locally

```bash
jscpd --min-lines 5 --min-tokens 50 backend/ frontend/src/ -f "**/*.py" -f "**/*.js"
```

### Duplication Thresholds

- **Minimum lines**: 5 lines of duplicated code
- **Minimum tokens**: 50 tokens

If duplication is detected, refactor common code into:
- **Python**: Utility functions or classes in separate modules
- **JavaScript**: Custom hooks, utility functions, or components

## Dependency Management

### Python Dependencies

Python dependencies are managed in `backend/requirements.txt`.

**Check for unused dependencies:**
```bash
cd backend
pipdeptree
```

### JavaScript Dependencies

JavaScript dependencies are managed in `frontend/package.json`.

**Check for unused dependencies:**
```bash
cd frontend
npx depcheck
```

**Known unused dependencies** (to be removed or justified):
- `@hookform/resolvers` - Form validation resolvers
- `cra-template` - Create React App template (dev only)
- `jspdf` and `jspdf-autotable` - PDF generation (if not used)
- `socket.io-client` - Real-time communication (verify usage)
- `zod` - Schema validation

## Continuous Integration

All code quality checks are automated in our CI pipeline via GitHub Actions (`.github/workflows/ci.yml`).

The CI pipeline runs on every push and pull request to `main` and `develop` branches:

1. **Python Linting**: Runs flake8 on all Python files
2. **JavaScript Linting**: Runs ESLint on all JavaScript files
3. **Code Duplication**: Checks for duplicated code
4. **Dependency Audit**: Audits npm dependencies for security issues and unused packages
5. **Python Tests**: Runs pytest for backend tests

### Local Pre-commit Hooks (Optional)

You can set up pre-commit hooks to run linting before committing:

```bash
# Install pre-commit
pip install pre-commit

# Set up pre-commit hooks (if .pre-commit-config.yaml exists)
pre-commit install
```

## Editor Configuration

### VS Code

Recommended VS Code extensions:
- Python (Microsoft)
- ESLint
- Prettier

### PyCharm / IntelliJ

Enable:
- PEP 8 code style
- ESLint integration
- Auto-formatting on save

## Fixing All Issues

To fix all linting issues at once:

```bash
# Python
cd backend
python -m autopep8 --in-place --aggressive --aggressive --max-line-length=120 *.py

# JavaScript
cd frontend
npx eslint src/**/*.js src/*.js --fix
```

## Summary of Changes Made

### Python Files
- ✅ Fixed all flake8 issues (195 issues resolved)
  - Removed unused imports
  - Fixed whitespace and blank lines
  - Fixed line length issues
  - Fixed syntax errors in f-strings

### JavaScript Files
- ✅ Created ESLint configuration
- ✅ Fixed unused variable in `use-toast.js`
- ✅ All ESLint checks passing

### CI/CD
- ✅ Created GitHub Actions workflow for automated checks
- ✅ Added linting, duplication, and dependency audit jobs

### Documentation
- ✅ This standards document for future reference

## Next Steps

1. Remove unused JavaScript dependencies after verification
2. Consider adding TypeScript for better type safety
3. Add more comprehensive tests
4. Consider adding code coverage requirements
