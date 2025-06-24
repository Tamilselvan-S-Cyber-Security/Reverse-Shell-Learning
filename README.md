# Wolf Shell Generator (WSG) - Replit Configuration

## Overview

Wolf Shell Generator (WSG) is a comprehensive educational programming platform developed by S. Tamilselvan, a cybersecurity professional. The platform combines interactive programming tutorials with a modern web interface, featuring a glassy aesthetic design. WSG serves as both an educational tool for learning multiple programming languages and a platform for cybersecurity-focused coding practice.

The application is built using Flask as the backend framework with SQLAlchemy for database operations, providing user authentication, progress tracking, and an interactive code editor that supports multiple programming languages including Python, JavaScript, C, C++, and Bash.

## System Architecture

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with custom CSS implementing glass morphism design
- **JavaScript Libraries**: CodeMirror for code editing, vanilla JavaScript for interactions
- **Template Engine**: Jinja2 templates with Flask
- **Design System**: Glass morphism aesthetic with gradient backgrounds and blur effects
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Backend Architecture
- **Web Framework**: Flask 3.1.1 with Werkzeug
- **Database ORM**: SQLAlchemy 2.0.41 with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Security**: Password hashing with Werkzeug security utilities
- **Code Execution**: Custom sandboxed code executor with timeout protection
- **WSGI Server**: Gunicorn for production deployment

### Database Design
- **User Management**: User accounts with authentication and admin privileges
- **Progress Tracking**: UserProgress model linking users to completed lessons
- **Code History**: CodeExecution model storing user code submissions and results
- **Unique Constraints**: Preventing duplicate progress entries per user/lesson

## Key Components

### 1. User Authentication System
- Registration and login functionality with form validation
- Password requirements (minimum 6 characters)
- Unique username and email constraints
- Session-based authentication using Flask-Login
- Auto-authentication system for instant platform access

### 2. Interactive Code Editor
- Multi-language support (Python, JavaScript, C, C++, Bash)
- CodeMirror integration with syntax highlighting
- Real-time code execution with output display
- Keyboard shortcuts for enhanced productivity
- Language-specific templates and execution environments

### 3. Educational Content Management
- Structured lesson progression system
- Language-specific tutorial paths
- Progress tracking and completion status
- Difficulty-based lesson organization

### 4. Code Execution Engine
- Sandboxed execution environment with security controls
- 10-second timeout protection
- Output size limitations (10KB max)
- Support for compiled languages (C/C++) with automatic compilation
- Error handling and execution time tracking

### 5. Gemini AI Integration
- Google Gemini AI-powered code analysis and insights
- Real-time code enhancement suggestions
- Educational explanations of code functionality
- Debug assistance for error resolution
- Performance optimization recommendations
- Security consideration analysis

### 6. Dashboard and Analytics
- User progress visualization
- Statistics on completed lessons and code executions
- Language-specific progress tracking
- Recent activity display

## Data Flow

### User Registration/Login Flow
1. User submits registration/login form
2. Server validates input and checks database constraints
3. Password hashing (registration) or verification (login)
4. Session creation and user redirection
5. Dashboard loading with personalized data

### Code Execution Flow
1. User writes code in the web-based editor
2. Code submission triggers server-side validation
3. Language-specific execution environment setup
4. Sandboxed code execution with timeout protection
5. Results capture (output, errors, execution time)
6. Database logging and response to frontend
7. Real-time display of execution results

### Progress Tracking Flow
1. User completes lessons or exercises
2. Progress data stored in UserProgress model
3. Completion status and scores updated
4. Dashboard statistics automatically refreshed
5. Achievement tracking and milestone updates

## External Dependencies

### Production Dependencies
- **Flask Ecosystem**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: PostgreSQL with psycopg2-binary driver
- **Web Server**: Gunicorn for WSGI serving
- **Security**: Werkzeug for password hashing
- **Validation**: email-validator for email format checking

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: UI framework and responsive design
- **Font Awesome 6.4.0**: Icon library
- **CodeMirror 5.65.2**: Code editor with syntax highlighting

### Development Dependencies
- **Python 3.11**: Runtime environment
- **OpenSSL**: Cryptographic operations
- **PostgreSQL**: Database engine

## Deployment Strategy

### Replit Configuration
- **Module**: Python 3.11 environment
- **Nix Channel**: stable-24_05 for reproducible builds
- **Packages**: OpenSSL and PostgreSQL system packages
- **Deployment Target**: Autoscale for dynamic scaling

### Production Server
- **WSGI Server**: Gunicorn with multiple worker processes
- **Port Binding**: 0.0.0.0:5000 for external access
- **Process Management**: Reuse port and reload capabilities
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility

### Database Configuration
- **Development**: SQLite for local development
- **Production**: PostgreSQL with connection pooling
- **Connection Management**: Pool recycling and pre-ping health checks
- **Migration Strategy**: SQLAlchemy table creation on startup

### Security Considerations
- Environment-based configuration for sensitive data
- Session secret key management
- SQL injection prevention through ORM usage
- XSS protection through template escaping
- CSRF protection for form submissions



# Cyber Wolf  
## Cyber Security Interested Students Join Now!

🔗 [Join Here](https://cyberwolf-career-guidance.web.app/)

---

### 🔥 Highlights:
- 🧠 The Best Practical Class – Once Every Week  
- 🏆 Hackathons and Capture The Flag (CTF) Competitions Regularly  
- 👨‍💻 Hands-on Training with Real-world Cyber Security Scenarios  
- 🚀 Boost Your Skills with Weekly Challenges and Projects  

---
 The Devloped By S.Tamilselvan
Join the Cyber Wolf community and become a cyber security expert!
