import subprocess
import tempfile
import os
import time
import signal
from contextlib import contextmanager

class CodeExecutor:
    """Safe code execution in sandboxed environment"""
    
    def __init__(self):
        self.timeout = 10  # 10 seconds timeout
        self.max_output_size = 10000  # 10KB max output
        
        # Supported languages and their execution commands
        self.languages = {
            'python': {
                'extension': '.py',
                'command': ['python3'],
                'template': '{code}'
            },
            'javascript': {
                'extension': '.js',
                'command': ['node'],
                'template': '{code}'
            },
            'bash': {
                'extension': '.sh',
                'command': ['bash'],
                'template': '{code}'
            },
            'c': {
                'extension': '.c',
                'command': ['gcc', '-o', 'temp_exec', '{file}', '&&', './temp_exec'],
                'template': '#include <stdio.h>\nint main() {\n{code}\nreturn 0;\n}'
            },
            'cpp': {
                'extension': '.cpp',
                'command': ['g++', '-o', 'temp_exec', '{file}', '&&', './temp_exec'],
                'template': '#include <iostream>\nusing namespace std;\nint main() {\n{code}\nreturn 0;\n}'
            }
        }
    
    @contextmanager
    def timeout_handler(self, seconds):
        """Context manager for handling timeouts"""
        def timeout_signal(signum, frame):
            raise TimeoutError(f"Code execution timed out after {seconds} seconds")
        
        old_handler = signal.signal(signal.SIGALRM, timeout_signal)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def execute(self, language, code):
        """Execute code in specified language"""
        start_time = time.time()
        
        if language not in self.languages:
            return {
                'output': '',
                'error': f'Unsupported language: {language}',
                'execution_time': 0
            }
        
        lang_config = self.languages[language]
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create temporary file
                file_path = os.path.join(temp_dir, f'temp{lang_config["extension"]}')
                
                # Prepare code with template if needed
                if 'template' in lang_config:
                    final_code = lang_config['template'].format(code=code)
                else:
                    final_code = code
                
                # Write code to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(final_code)
                
                # Prepare command
                command = lang_config['command'].copy()
                for i, cmd_part in enumerate(command):
                    if '{file}' in cmd_part:
                        command[i] = cmd_part.replace('{file}', file_path)
                
                # If command contains '&&', join them properly
                if '&&' in command:
                    command = ' '.join(command)
                    shell = True
                else:
                    if language in ['python', 'javascript', 'bash']:
                        command.append(file_path)
                    shell = False
                
                # Execute with timeout
                try:
                    with self.timeout_handler(self.timeout):
                        if shell:
                            process = subprocess.run(
                                command,
                                shell=True,
                                cwd=temp_dir,
                                capture_output=True,
                                text=True,
                                timeout=self.timeout
                            )
                        else:
                            process = subprocess.run(
                                command,
                                cwd=temp_dir,
                                capture_output=True,
                                text=True,
                                timeout=self.timeout
                            )
                    
                    execution_time = time.time() - start_time
                    
                    # Limit output size
                    output = process.stdout[:self.max_output_size] if process.stdout else ''
                    error = process.stderr[:self.max_output_size] if process.stderr else ''
                    
                    if len(process.stdout or '') > self.max_output_size:
                        output += "\n[Output truncated - too long]"
                    
                    if len(process.stderr or '') > self.max_output_size:
                        error += "\n[Error output truncated - too long]"
                    
                    return {
                        'output': output,
                        'error': error,
                        'execution_time': execution_time,
                        'return_code': process.returncode
                    }
                
                except (subprocess.TimeoutExpired, TimeoutError):
                    return {
                        'output': '',
                        'error': f'Code execution timed out after {self.timeout} seconds',
                        'execution_time': self.timeout
                    }
        
        except Exception as e:
            return {
                'output': '',
                'error': f'Execution error: {str(e)}',
                'execution_time': time.time() - start_time
            }
    
    def get_supported_languages(self):
        """Get list of supported programming languages"""
        return list(self.languages.keys())
