"""Educational content for programming languages"""

def get_languages():
    """Get list of supported programming languages"""
    return [
        {
            'id': 'python',
            'name': 'Python',
            'description': 'A versatile, beginner-friendly language',
            'icon': '🐍'
        },
        {
            'id': 'javascript',
            'name': 'JavaScript',
            'description': 'The language of the web',
            'icon': '🌐'
        },
        {
            'id': 'c',
            'name': 'C',
            'description': 'Low-level programming fundamentals',
            'icon': '⚡'
        },
        {
            'id': 'cpp',
            'name': 'C++',
            'description': 'Object-oriented programming with C',
            'icon': '⚙️'
        },
        {
            'id': 'bash',
            'name': 'Bash',
            'description': 'Shell scripting and automation',
            'icon': '💻'
        }
    ]

def get_lessons(language):
    """Get lessons for a specific language"""
    lessons = {
        'python': [
            {
                'id': 'python-basics',
                'title': 'Python Basics',
                'description': 'Variables, data types, and basic operations',
                'difficulty': 'Beginner'
            },
            {
                'id': 'python-control',
                'title': 'Control Structures',
                'description': 'If statements, loops, and conditionals',
                'difficulty': 'Beginner'
            },
            {
                'id': 'python-functions',
                'title': 'Functions',
                'description': 'Creating and using functions',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'python-classes',
                'title': 'Object-Oriented Programming',
                'description': 'Classes, objects, and inheritance',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'python-security',
                'title': 'Security Concepts',
                'description': 'Basic cybersecurity principles in Python',
                'difficulty': 'Advanced'
            }
        ],
        'javascript': [
            {
                'id': 'js-basics',
                'title': 'JavaScript Fundamentals',
                'description': 'Variables, functions, and basic syntax',
                'difficulty': 'Beginner'
            },
            {
                'id': 'js-dom',
                'title': 'DOM Manipulation',
                'description': 'Interacting with web pages',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'js-async',
                'title': 'Asynchronous JavaScript',
                'description': 'Promises, async/await, and callbacks',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'js-security',
                'title': 'Web Security',
                'description': 'XSS prevention and secure coding',
                'difficulty': 'Advanced'
            }
        ],
        'c': [
            {
                'id': 'c-basics',
                'title': 'C Programming Basics',
                'description': 'Syntax, variables, and basic I/O',
                'difficulty': 'Beginner'
            },
            {
                'id': 'c-pointers',
                'title': 'Pointers and Memory',
                'description': 'Understanding memory management',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'c-security',
                'title': 'Buffer Overflows',
                'description': 'Understanding memory vulnerabilities',
                'difficulty': 'Advanced'
            }
        ],
        'cpp': [
            {
                'id': 'cpp-basics',
                'title': 'C++ Fundamentals',
                'description': 'Basic syntax and features',
                'difficulty': 'Beginner'
            },
            {
                'id': 'cpp-oop',
                'title': 'Object-Oriented Programming',
                'description': 'Classes, inheritance, and polymorphism',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'cpp-security',
                'title': 'Secure C++ Programming',
                'description': 'Best practices and vulnerability prevention',
                'difficulty': 'Advanced'
            }
        ],
        'bash': [
            {
                'id': 'bash-basics',
                'title': 'Shell Scripting Basics',
                'description': 'Basic commands and scripting',
                'difficulty': 'Beginner'
            },
            {
                'id': 'bash-automation',
                'title': 'System Automation',
                'description': 'Automating system tasks',
                'difficulty': 'Intermediate'
            },
            {
                'id': 'bash-security',
                'title': 'Security Scripting',
                'description': 'Security auditing and monitoring scripts',
                'difficulty': 'Advanced'
            }
        ]
    }
    
    return lessons.get(language, [])

def get_lesson_content(language, lesson_id):
    """Get detailed content for a specific lesson"""
    content = {
        'python-basics': {
            'title': 'Python Basics',
            'theory': '''
# Python Basics

Python is a high-level, interpreted programming language known for its simplicity and readability.

## Variables and Data Types

```python
# String
name = "WSG Learner"
print(name)

# Integer
age = 25
print(age)

# Float
height = 5.9
print(height)

# Boolean
is_student = True
print(is_student)

# List
languages = ["Python", "JavaScript", "C++"]
print(languages)
```

## Basic Operations

Python supports various operations on different data types:

```python
# String operations
greeting = "Hello" + " " + "World"
repeated = "WSG " * 3

# Arithmetic operations
sum_result = 10 + 5
difference = 10 - 5
product = 10 * 5
division = 10 / 3

# List operations
languages.append("Bash")
languages.remove("JavaScript")
```
''',
            'example_code': '''# WSG Python Basics Example
print("Welcome to Wolf Shell Generator!")

# Variable declarations
name = "Cybersecurity Student"
age = 22
skills = ["Python", "Networking", "Security"]

# Display information
print(f"Name: {name}")
print(f"Age: {age}")
print("Skills:")
for skill in skills:
    print(f"- {skill}")

# Basic calculation
years_experience = 2
total_knowledge = len(skills) * years_experience
print(f"Knowledge Score: {total_knowledge}")''',
            'exercise': 'Create variables for your name, age, and favorite programming languages. Display them in a formatted output and calculate how many years you\'ve been learning programming.'
        },
        
        'python-control': {
            'title': 'Control Structures',
            'theory': '''
# Control Structures in Python

Control structures allow you to control the flow of your program execution.

## Conditional Statements

```python
# If-elif-else structure
age = 18
if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")
```

## Loops

### For Loops
```python
# Iterating over a list
languages = ["Python", "JavaScript", "C++"]
for language in languages:
    print(f"Learning {language}")

# Range-based loops
for i in range(5):
    print(f"Count: {i}")
```

### While Loops
```python
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```
''',
            'example_code': '''# WSG Control Structures Example
print("WSG Security Level Checker")

# User input simulation
security_level = 7
access_attempts = 3

# Conditional access control
if security_level >= 8:
    print("HIGH SECURITY: Full access granted")
elif security_level >= 5:
    print("MEDIUM SECURITY: Limited access granted")
else:
    print("LOW SECURITY: Access denied")

# Loop through security protocols
protocols = ["Firewall", "Encryption", "Authentication", "Monitoring"]
print("\nActivating security protocols:")
for i, protocol in enumerate(protocols, 1):
    print(f"{i}. {protocol} - ACTIVATED")

# Attempt counter
attempt = 1
while attempt <= access_attempts:
    print(f"Access attempt {attempt}/{access_attempts}")
    attempt += 1''',
            'exercise': 'Create a simple security checker that evaluates a password strength (1-10) and uses loops to check multiple passwords from a list.'
        },
        
        'javascript-basics': {
            'title': 'JavaScript Fundamentals',
            'theory': '''
# JavaScript Fundamentals

JavaScript is a versatile programming language primarily used for web development.

## Variables and Data Types

```javascript
// Variable declarations
let name = "WSG Developer";
const age = 25;
var isStudent = true;

// Data types
let number = 42;
let string = "Hello World";
let boolean = true;
let array = [1, 2, 3, 4, 5];
let object = {name: "WSG", type: "Educational Platform"};
```

## Functions

```javascript
// Function declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow functions
const add = (a, b) => a + b;

// Function with multiple parameters
function createUser(name, age, skills) {
    return {
        name: name,
        age: age,
        skills: skills
    };
}
```
''',
            'example_code': '''// WSG JavaScript Basics Example
console.log("Welcome to Wolf Shell Generator - JavaScript Edition!");

// Variable declarations
const platformName = "WSG";
let userCount = 1250;
const features = ["Code Editor", "Tutorials", "Progress Tracking"];

// Function to display platform info
function displayPlatformInfo() {
    console.log(`Platform: ${platformName}`);
    console.log(`Active Users: ${userCount}`);
    console.log("Features:");
    features.forEach((feature, index) => {
        console.log(`${index + 1}. ${feature}`);
    });
}

// Function to calculate learning progress
const calculateProgress = (completed, total) => {
    const percentage = (completed / total) * 100;
    return `Progress: ${percentage.toFixed(1)}%`;
};

// Execute functions
displayPlatformInfo();
console.log(calculateProgress(7, 10));''',
            'exercise': 'Create functions to manage a simple user profile system with name, skills array, and experience level calculation.'
        },
        
        'bash-basics': {
            'title': 'Shell Scripting Basics',
            'theory': '''
# Bash Shell Scripting

Bash (Bourne Again Shell) is a command-line interpreter and scripting language.

## Variables

```bash
#!/bin/bash

# Variable assignment (no spaces around =)
name="WSG User"
age=25
skills=("bash" "python" "security")

# Using variables
echo "Hello, $name"
echo "Age: ${age}"
```

## Basic Commands

```bash
# File operations
ls -la                    # List files
mkdir my_directory        # Create directory
cd my_directory          # Change directory
touch new_file.txt       # Create empty file
echo "content" > file.txt # Write to file

# System information
whoami                   # Current user
pwd                      # Current directory
date                     # Current date and time
```

## Conditional Statements

```bash
if [ "$age" -gt 18 ]; then
    echo "Adult user"
elif [ "$age" -gt 12 ]; then
    echo "Teen user"
else
    echo "Young user"
fi
```
''',
            'example_code': '''#!/bin/bash
# WSG Bash Basics Example

echo "=== Wolf Shell Generator - System Check ==="

# Variables
platform="WSG"
version="1.0"
check_date=$(date +"%Y-%m-%d %H:%M:%S")

# System information
echo "Platform: $platform v$version"
echo "Check performed: $check_date"
echo "Current user: $(whoami)"
echo "System: $(uname -s)"

# Create WSG directory structure
echo "Setting up WSG workspace..."
mkdir -p wsg_workspace/{scripts,logs,config}

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✓ Python3 is available: $(python3 --version)"
else
    echo "✗ Python3 not found"
fi

# List created directories
echo "Created directories:"
ls -la wsg_workspace/

echo "=== WSG System Check Complete ==="''',
            'exercise': 'Create a bash script that checks system requirements for a cybersecurity toolkit and creates necessary directories.'
        }
    }
    
    return content.get(lesson_id, {})
