# Backend Auth Project

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Email Setup (Gmail)](#email-setup-gmail)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication Flow](#authentication-flow)
- [Security Features](#security-features)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

This is a production-ready backend authentication system built with **FastAPI**, providing secure user registration, login, email verification, and password management. The system uses JWT tokens for authentication and includes comprehensive security features.

## ✨ Features

### Core Authentication
- ✅ User registration with email verification
- ✅ Secure login with Session tokens
- ✅ Password reset via email
- ✅ Email verification with OTP
- ✅ Token refresh functionality
- ✅ Account lockout after failed attempts

### Security Features
- 🔐 Password hashing with bcrypt
- 🔑 Session-based authentication
- 📧 Email verification required
- 🛡️ Input validation and sanitization
- 🔒 Secure password requirements

### Additional Features
- 📊 Comprehensive logging
- 🚨 Structured error handling
- 📝 API documentation (Swagger/OpenAPI)
- 🧪 Unit and integration tests


###Features to Add
- 🚫 Rate limiting on sensitive endpoints
- - 🔄 Database migrations with Alembic

## 📋 Requirements

### System Requirements
- **Python**: 3.8+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Email**: SMTP server (Gmail recommended)

### Python Dependencies
```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.11.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
python-decouple>=3.8
pydantic[email]>=2.0.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/backend-auth-project.git
cd backend-auth-project
```

### 2. Create Virtual Environment
```bash
# Using venv (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

### 4. Project Structure
After installation, your project should look like this:
```
backend-auth-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   └── users.py         # User management routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication logic
│   │   └── email_service.py # Email functionality
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # Security utilities
│       └── helpers.py       # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_users.py
├── alembic/                 # Database migrations
├── .env.example             # Environment variables example
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Environment Configuration

### 1. Create Environment File
```bash
# Copy the example environment file
cp .env.example .env
```

### 2. Configure .env File
Create a `.env` file in your project root with the following variables:

```bash
# =============================================================================
# APPLICATION SETTINGS
# =============================================================================
DEBUG=True
SECRET_KEY=your-super-secret-key-min-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# =============================================================================
# DATABASE SETTINGS
# =============================================================================
# For Development (SQLite)
DATABASE_URL=sqlite:///./app.db

# For Production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# =============================================================================
# EMAIL SETTINGS (Gmail SMTP)
# =============================================================================
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_FROM=your-email@gmail.com
EMAIL_FROM_NAME=Your App Name

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
ALGORITHM=HS256
OTP_EXPIRE_MINUTES=15
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30

# =============================================================================
# RATE LIMITING
# =============================================================================
RATE_LIMIT_LOGIN=5/minute
RATE_LIMIT_REGISTER=3/minute
RATE_LIMIT_RESET_PASSWORD=2/minute

# =============================================================================
# LOGGING
# =============================================================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 3. Generate Secret Key
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📧 Email Setup (Gmail)

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the prompts to enable 2FA

### Step 2: Generate App Password
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on **Security** → **2-Step Verification**
3. Scroll down to **App passwords**
4. Click **Select app** → Choose **Mail**
5. Click **Select device** → Choose **Other (custom name)**
6. Enter a name like "FastAPI Auth App"
7. Click **Generate**
8. **Copy the 16-character password** (this is your `EMAIL_PASSWORD`)

### Step 3: Update .env File
```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=abcd-efgh-ijkl-mnop  # The 16-character app password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### Step 4: Test Email Configuration
```bash
# Run the email test script
python -c "
from app.services.email_service import send_test_email
send_test_email('recipient@example.com')
print('Email test completed!')
"
```

## 🗄️ Database Setup

### 1. Initialize Alembic (First Time Only)
```bash
# Initialize migration environment
alembic init alembic
```

### 2. Create Initial Migration
```bash
# Generate first migration
alembic revision --autogenerate -m "Initial migration"
```

### 3. Run Migrations
```bash
# Apply migrations to database
alembic upgrade head
```

### 4. Database Management Commands
```bash
# Check current migration version
alembic current

# View migration history
alembic history

# Downgrade to previous version
alembic downgrade -1

# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"
```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
# Run with auto-reload (recommended for development)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Or with custom host and port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Run with specific log level
uvicorn app.main:app --reload --log-level debug
```

### Production Mode
```bash
# Run with Gunicorn for production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or with uvicorn for production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the Application
- **API Documentation (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Documentation (ReDoc)**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

## 📚 API Endpoints

### Authentication Endpoints

#### POST `/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully. Please verify your email.",
  "email": "john@example.com",
  "verification_required": true
}
```

#### POST `/auth/verify-email`
Verify user email with OTP.

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response (200):**
```json
{
  "message": "Email verified successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### POST `/auth/login`
Login with existing credentials.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

#### POST `/auth/refresh-token`
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST `/auth/forgot-password`
Request password reset email.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

#### POST `/auth/reset-password`
Reset password with OTP.

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456",
  "new_password": "NewSecurePass123!"
}
```

#### POST `/auth/logout`
Logout user (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

### User Management Endpoints

#### GET `/users/profile`
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "is_verified": true,
  "created_at": "2023-01-01T00:00:00Z",
  "last_login": "2023-01-01T12:00:00Z"
}
```

#### PUT `/users/profile`
Update user profile (requires authentication).

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
```

#### POST `/users/change-password`
Change user password (requires authentication).

**Request Body:**
```json
{
  "current_password": "CurrentPass123!",
  "new_password": "NewSecurePass123!"
}
```

## 🔐 Authentication Flow

### Registration Flow
1. User submits registration form
2. System validates input data
3. System checks for existing users
4. Password is hashed and stored
5. OTP is generated and sent via email
6. User verifies email with OTP
7. Account is activated

### Login Flow
1. User submits credentials
2. System validates credentials
3. System checks account status
4. JWT tokens are generated
5. Tokens are returned to client
6. Client stores tokens for subsequent requests

### Password Reset Flow
1. User requests password reset
2. System generates OTP
3. OTP is sent via email
4. User submits OTP with new password
5. Password is updated
6. User can login with new password

## 🛡️ Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Token Security
- JWT tokens with expiration
- Refresh token rotation
- Token blacklisting on logout
- Secure token storage recommendations

### Rate Limiting
- Login attempts: 5 per minute
- Registration: 3 per minute
- Password reset: 2 per minute
- Account lockout after 5 failed attempts

### Input Validation
- Email format validation
- SQL injection prevention
- XSS protection
- CSRF protection

## 🚨 Error Handling

The API returns structured error responses:

```json
{
  "error_type": "validation_error",
  "message": "Invalid input data",
  "details": {
    "field": "email",
    "error": "Invalid email format"
  },
  "timestamp": "2023-01-01T12:00:00Z",
  "path": "/auth/register"
}
```

### Common Error Types
- `validation_error`: Input validation failed
- `authentication_error`: Invalid credentials
- `authorization_error`: Insufficient permissions
- `rate_limit_error`: Too many requests
- `server_error`: Internal server error

## 📝 Logging

### Log Configuration
Logs are written to both console and file with the following levels:
- **DEBUG**: Detailed diagnostic information
- **INFO**: General information about application flow
- **WARNING**: Something unexpected happened
- **ERROR**: Serious problem occurred
- **CRITICAL**: Very serious error occurred

### Log Locations
- **Development**: Console output
- **Production**: `/logs/app.log` with rotation

### Log Format
```
2023-01-01 12:00:00,000 [INFO] app.auth: User johndoe logged in successfully
```

## 🧪 Testing

### Run All Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_login"
```

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test API endpoints
- **Security Tests**: Test authentication and authorization

### Test Environment Setup
```bash
# Set test environment variables
export TEST_DATABASE_URL=sqlite:///./test.db
export TESTING=True

# Or create .env.test file
cp .env .env.test
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run Docker container
docker build -t backend-auth .
docker run -p 8000:8000 backend-auth
```

### Environment Variables for Production
```bash
DEBUG=False
DATABASE_URL=postgresql://user:pass@db:5432/prod_db
SECRET_KEY=production-secret-key
EMAIL_USER=production@yourdomain.com
EMAIL_PASSWORD=production-app-password
```

### Health Checks
```bash
# Add health check endpoint
curl http://your-domain.com/health
```

## 🔧 Troubleshooting

### Common Issues

#### Email Not Sending
```bash
# Check email configuration
python -c "from app.services.email_service import test_email_config; test_email_config()"

# Verify Gmail app password
# Make sure 2FA is enabled and app password is correct
```

#### Database Connection Error
```bash
# Check database URL
echo $DATABASE_URL

# Test database connection
python -c "from app.database import engine; print(engine.url)"

# Run migrations
alembic upgrade head
```

#### JWT Token Issues
```bash
# Check secret key
echo $SECRET_KEY

# Verify token expiration settings
echo $ACCESS_TOKEN_EXPIRE_MINUTES
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG=True

# Run with debug output
uvicorn app.main:app --reload --log-level debug
```

### Performance Issues
```bash
# Check database performance
# Add database query logging
export LOG_LEVEL=DEBUG

# Monitor response times
# Use APM tools like New Relic or DataDog
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write descriptive commit messages
- Add docstrings to functions

### Pull Request Process
1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Request review from maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: Check the `/docs` endpoint when running the app
- **Issues**: Report bugs on the GitHub issues page
- **Email**: contact@yourapp.com
- **Discord**: Join our development community

---

**Happy coding! 🎉**
