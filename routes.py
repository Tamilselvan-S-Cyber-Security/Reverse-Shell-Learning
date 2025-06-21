from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, UserProgress, CodeExecution
from code_executor import CodeExecutor
from educational_content import get_languages, get_lessons, get_lesson_content
from gemini_service import analyze_code_with_gemini, enhance_code_output, debug_code_with_gemini
import logging

@app.route('/')
def index():
    """Home page with modern glassy design"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if password and len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        login_field = request.form.get('login_field')
        password = request.form.get('password')
        
        if not login_field or not password:
            flash('Email/Username and password are required.', 'error')
            return render_template('login.html')
        
        # Check if login field is email or username
        if '@' in login_field:
            user = User.query.filter_by(email=login_field).first()
        else:
            user = User.query.filter_by(username=login_field).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            # Handle redirect parameter
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email/username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """User dashboard with progress tracking"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    languages = get_languages()
    user_progress = {}
    
    for lang in languages:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id, 
            language=lang['id']
        ).all()
        total_lessons = len(get_lessons(lang['id']))
        completed_lessons = len([p for p in progress if p.completed])
        user_progress[lang['id']] = {
            'completed': completed_lessons,
            'total': total_lessons,
            'percentage': (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        }
    
    recent_executions = CodeExecution.query.filter_by(
        user_id=current_user.id
    ).order_by(CodeExecution.executed_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         languages=languages, 
                         user_progress=user_progress,
                         recent_executions=recent_executions)

@app.route('/tutorials')
def tutorials():
    """Programming tutorials page"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    languages = get_languages()
    selected_lang = request.args.get('lang', 'python')
    lessons = get_lessons(selected_lang)
    
    # Get user progress for this language
    user_progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        language=selected_lang
    ).all() if current_user.is_authenticated else []
    
    completed_lessons = {p.lesson_id for p in user_progress if p.completed}
    
    return render_template('tutorials.html', 
                         languages=languages,
                         selected_lang=selected_lang,
                         lessons=lessons,
                         completed_lessons=completed_lessons)

@app.route('/editor')
def editor():
    """Interactive code editor"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    language = request.args.get('lang', 'python')
    lesson_id = request.args.get('lesson')
    
    languages = get_languages()
    lesson_content = None
    
    if lesson_id:
        lesson_content = get_lesson_content(language, lesson_id)
    
    # Get last execution result from session without clearing it initially
    result = session.get('last_execution')
    
    return render_template('editor.html', 
                         languages=languages,
                         selected_lang=language,
                         lesson_content=lesson_content,
                         result=result)

@app.route('/execute_code', methods=['POST'])
def execute_code():
    """Execute code in a sandboxed environment"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    language = request.form.get('language', 'python')
    code = request.form.get('code', '')
    
    try:
        if not code.strip():
            flash('Please enter some code to execute.', 'error')
            return redirect(request.referrer or url_for('editor', lang=language))
        
        executor = CodeExecutor()
        result = executor.execute(language, code)
        
        # Save execution to database if user is authenticated
        if current_user.is_authenticated:
            execution = CodeExecution()
            execution.user_id = current_user.id
            execution.language = language
            execution.code = code
            execution.output = result.get('output', '')
            execution.error = result.get('error', '')
            execution.execution_time = result.get('execution_time', 0)
            db.session.add(execution)
            db.session.commit()
        
        # Get AI analysis using Gemini
        ai_analysis = None
        if result.get('error'):
            # Debug analysis for errors
            ai_analysis = debug_code_with_gemini(language, code, result.get('error', ''))
        elif result.get('output'):
            # Enhancement analysis for successful execution
            ai_analysis = enhance_code_output(language, code, result.get('output', ''))
        else:
            # General code analysis
            ai_analysis = analyze_code_with_gemini(language, code, result.get('output', ''), result.get('error', ''))
        
        # Add AI analysis to result
        if ai_analysis:
            result['ai_analysis'] = ai_analysis
        
        # Store result in session
        session['last_execution'] = result
        
        if result.get('output') or result.get('error'):
            flash('Code executed successfully with AI analysis!', 'success')
        else:
            flash('Code executed with no output - AI analysis available', 'info')
        
    except Exception as e:
        logging.error(f"Code execution error: {str(e)}")
        flash(f'Execution error: {str(e)}', 'error')
        session['last_execution'] = {
            'output': '',
            'error': f'Execution error: {str(e)}',
            'execution_time': 0
        }
    
    return redirect(request.referrer or url_for('editor', lang=language))

@app.route('/ai_analyze', methods=['POST'])
def ai_analyze():
    """Get AI analysis for code without execution"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    language = request.form.get('language', 'python')
    code = request.form.get('code', '')
    
    if not code.strip():
        flash('Please enter some code to analyze.', 'error')
        return redirect(request.referrer or url_for('editor', lang=language))
    
    try:
        # Get AI analysis without execution
        ai_analysis = analyze_code_with_gemini(language, code)
        
        # Store result in session
        session['last_execution'] = {
            'output': '',
            'error': '',
            'execution_time': 0,
            'ai_analysis': ai_analysis
        }
        
        flash('AI analysis completed!', 'success')
        
    except Exception as e:
        logging.error(f"AI analysis error: {str(e)}")
        flash(f'AI analysis error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('editor', lang=language))

@app.route('/mark_lesson_complete', methods=['POST'])
def mark_lesson_complete():
    """Mark a lesson as completed"""
    # Auto-login if not authenticated
    if not current_user.is_authenticated:
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            login_user(test_user)
    
    language = request.form.get('language')
    lesson_id = request.form.get('lesson_id')
    
    if not language or not lesson_id:
        flash('Invalid lesson data.', 'error')
        return redirect(request.referrer)
    
    if current_user.is_authenticated:
        # Check if progress already exists
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            language=language,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress()
            progress.user_id = current_user.id
            progress.language = language
            progress.lesson_id = lesson_id
            db.session.add(progress)
        
        progress.completed = True
        progress.completed_at = db.func.now()
        db.session.commit()
    
    flash('Lesson marked as completed!', 'success')
    return redirect(request.referrer or url_for('tutorials'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
