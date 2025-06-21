// Wolf Shell Generator (WSG) - Code Editor JavaScript

let codeEditor;
let currentLanguage = 'python';

document.addEventListener('DOMContentLoaded', function() {
    initializeCodeEditor();
    setupLanguageSupport();
    setupEditorControls();
    setupKeyboardShortcuts();
});

/**
 * Initialize CodeMirror editor
 */
function initializeCodeEditor() {
    const textarea = document.getElementById('codeEditor');
    if (!textarea) return;
    
    // Get current language from the page
    const languageInput = document.querySelector('input[name="language"]');
    if (languageInput) {
        currentLanguage = languageInput.value;
    }
    
    codeEditor = CodeMirror.fromTextArea(textarea, {
        lineNumbers: true,
        mode: getCodeMirrorMode(currentLanguage),
        theme: 'material-darker',
        indentUnit: 4,
        lineWrapping: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        showCursorWhenSelecting: true,
        styleActiveLine: true,
        extraKeys: {
            'Ctrl-Enter': executeCode,
            'Cmd-Enter': executeCode,
            'Ctrl-/': 'toggleComment',
            'Cmd-/': 'toggleComment',
            'F11': function(cm) {
                cm.setOption('fullScreen', !cm.getOption('fullScreen'));
            },
            'Esc': function(cm) {
                if (cm.getOption('fullScreen')) cm.setOption('fullScreen', false);
            }
        }
    });
    
    // Set editor size
    codeEditor.setSize('100%', '400px');
    
    // Focus on editor
    setTimeout(() => {
        codeEditor.refresh();
        codeEditor.focus();
    }, 100);
    
    // Auto-save to localStorage
    codeEditor.on('change', function() {
        saveCodeToLocalStorage();
    });
    
    // Load saved code
    loadCodeFromLocalStorage();
}

/**
 * Get CodeMirror mode for language
 */
function getCodeMirrorMode(language) {
    const modes = {
        'python': 'python',
        'javascript': 'javascript',
        'c': 'text/x-csrc',
        'cpp': 'text/x-c++src',
        'bash': 'shell'
    };
    return modes[language] || 'text/plain';
}

/**
 * Setup language-specific support
 */
function setupLanguageSupport() {
    // Language-specific templates
    const templates = {
        'python': `# Python Example
print("Hello, Wolf Shell Generator!")

# Variables and data types
name = "WSG User"
age = 25
languages = ["Python", "JavaScript", "C++"]

# Function example
def greet(name):
    return f"Welcome to WSG, {name}!"

print(greet(name))`,
        
        'javascript': `// JavaScript Example
console.log("Hello, Wolf Shell Generator!");

// Variables and data types
const name = "WSG User";
let age = 25;
const languages = ["Python", "JavaScript", "C++"];

// Function example
function greet(name) {
    return \`Welcome to WSG, \${name}!\`;
}

console.log(greet(name));`,
        
        'c': `// C Example
#include <stdio.h>
#include <string.h>

int main() {
    printf("Hello, Wolf Shell Generator!\\n");
    
    // Variables
    char name[] = "WSG User";
    int age = 25;
    
    printf("Welcome to WSG, %s!\\n", name);
    printf("Age: %d\\n", age);
    
    return 0;
}`,
        
        'cpp': `// C++ Example
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    cout << "Hello, Wolf Shell Generator!" << endl;
    
    // Variables
    string name = "WSG User";
    int age = 25;
    vector<string> languages = {"Python", "JavaScript", "C++"};
    
    cout << "Welcome to WSG, " << name << "!" << endl;
    cout << "Age: " << age << endl;
    
    return 0;
}`,
        
        'bash': `#!/bin/bash
# Bash Script Example

echo "Hello, Wolf Shell Generator!"

# Variables
name="WSG User"
age=25

# Array
languages=("Python" "JavaScript" "C++")

echo "Welcome to WSG, $name!"
echo "Age: $age"

# Loop through languages
for lang in "\${languages[@]}"; do
    echo "Language: $lang"
done`
    };
    
    window.languageTemplates = templates;
}

/**
 * Setup editor controls
 */
function setupEditorControls() {
    // Execute code button
    const executeBtn = document.querySelector('.btn-success[onclick*="executeCode"]');
    if (executeBtn) {
        executeBtn.removeAttribute('onclick');
        executeBtn.addEventListener('click', executeCode);
    }
    
    // Clear editor button
    const clearBtn = document.querySelector('.btn-outline-secondary[onclick*="clearEditor"]');
    if (clearBtn) {
        clearBtn.removeAttribute('onclick');
        clearBtn.addEventListener('click', clearEditor);
    }
    
    // Load example button
    const exampleBtn = document.querySelector('.btn-outline-secondary[onclick*="loadExample"]');
    if (exampleBtn) {
        exampleBtn.removeAttribute('onclick');
        exampleBtn.addEventListener('click', loadExample);
    }
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save (prevent default browser save)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            saveCodeToLocalStorage();
            if (window.WSG && window.WSG.showToast) {
                window.WSG.showToast('Code saved locally!', 'success');
            }
        }
        
        // Ctrl/Cmd + Enter to execute
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            executeCode();
        }
    });
}

/**
 * Execute code
 */
function executeCode() {
    if (!codeEditor) return;
    
    const code = codeEditor.getValue().trim();
    if (!code) {
        if (window.WSG && window.WSG.showToast) {
            window.WSG.showToast('Please enter some code to execute.', 'warning');
        }
        return;
    }
    
    // Update the hidden textarea and submit form
    const textarea = document.getElementById('codeEditor');
    if (textarea) {
        textarea.value = code;
    }
    
    const form = document.getElementById('codeForm');
    if (form) {
        // Show loading state
        const executeBtn = document.querySelector('.btn-success');
        if (executeBtn && window.WSG && window.WSG.showLoading) {
            window.WSG.showLoading(executeBtn);
        }
        
        // Clear previous output
        const outputDiv = document.getElementById('output');
        if (outputDiv) {
            outputDiv.innerHTML = `
                <div class="text-info text-center py-4">
                    <i class="fas fa-spinner fa-spin fa-2x mb-2"></i><br>
                    Executing ${currentLanguage} code...
                </div>
            `;
        }
        
        // Submit form
        form.submit();
    }
}

/**
 * Analyze code with AI
 */
function analyzeCode() {
    if (!codeEditor) return;
    
    const code = codeEditor.getValue().trim();
    if (!code) {
        if (window.WSG && window.WSG.showToast) {
            window.WSG.showToast('Please enter some code to analyze.', 'warning');
        }
        return;
    }
    
    // Update the hidden AI analysis form and submit
    const aiForm = document.getElementById('aiAnalysisForm');
    if (aiForm) {
        const aiTextarea = aiForm.querySelector('textarea[name="code"]');
        if (aiTextarea) {
            aiTextarea.value = code;
        }
        
        // Show loading state
        const analyzeBtn = document.querySelector('.btn-warning');
        if (analyzeBtn && window.WSG && window.WSG.showLoading) {
            window.WSG.showLoading(analyzeBtn);
        }
        
        // Clear previous output
        const outputDiv = document.getElementById('output');
        if (outputDiv) {
            outputDiv.innerHTML = `
                <div class="text-warning text-center py-4">
                    <i class="fas fa-robot fa-spin fa-2x mb-2"></i><br>
                    Analyzing ${currentLanguage} code with Gemini AI...
                </div>
            `;
        }
        
        // Submit AI analysis form
        aiForm.submit();
    }
}

/**
 * Clear editor
 */
function clearEditor() {
    if (!codeEditor) return;
    
    if (confirm('Are you sure you want to clear the editor? This action cannot be undone.')) {
        codeEditor.setValue('');
        codeEditor.focus();
        
        // Clear localStorage
        localStorage.removeItem(`wsg_code_${currentLanguage}`);
        
        if (window.WSG && window.WSG.showToast) {
            window.WSG.showToast('Editor cleared!', 'info');
        }
    }
}

/**
 * Load example code
 */
function loadExample() {
    if (!codeEditor || !window.languageTemplates) return;
    
    const template = window.languageTemplates[currentLanguage];
    if (template) {
        if (codeEditor.getValue().trim() && 
            !confirm('This will replace your current code. Continue?')) {
            return;
        }
        
        codeEditor.setValue(template);
        codeEditor.focus();
        
        if (window.WSG && window.WSG.showToast) {
            window.WSG.showToast(`${currentLanguage.toUpperCase()} example loaded!`, 'success');
        }
    }
}

/**
 * Save code to localStorage
 */
function saveCodeToLocalStorage() {
    if (!codeEditor) return;
    
    const code = codeEditor.getValue();
    const key = `wsg_code_${currentLanguage}`;
    
    try {
        localStorage.setItem(key, code);
    } catch (e) {
        console.warn('Failed to save code to localStorage:', e);
    }
}

/**
 * Load code from localStorage
 */
function loadCodeFromLocalStorage() {
    if (!codeEditor) return;
    
    const key = `wsg_code_${currentLanguage}`;
    
    try {
        const savedCode = localStorage.getItem(key);
        if (savedCode && !codeEditor.getValue().trim()) {
            codeEditor.setValue(savedCode);
        }
    } catch (e) {
        console.warn('Failed to load code from localStorage:', e);
    }
}

/**
 * Change editor language
 */
function changeEditorLanguage(newLanguage) {
    if (!codeEditor) return;
    
    // Save current code
    saveCodeToLocalStorage();
    
    // Update current language
    currentLanguage = newLanguage;
    
    // Change CodeMirror mode
    codeEditor.setOption('mode', getCodeMirrorMode(newLanguage));
    
    // Load saved code for new language
    loadCodeFromLocalStorage();
    
    // Update language input
    const languageInput = document.querySelector('input[name="language"]');
    if (languageInput) {
        languageInput.value = newLanguage;
    }
    
    if (window.WSG && window.WSG.showToast) {
        window.WSG.showToast(`Switched to ${newLanguage.toUpperCase()}`, 'info');
    }
}

/**
 * Format code
 */
function formatCode() {
    if (!codeEditor) return;
    
    // Basic code formatting
    const code = codeEditor.getValue();
    if (!code.trim()) return;
    
    // Simple indentation fix for Python
    if (currentLanguage === 'python') {
        const lines = code.split('\n');
        let indentLevel = 0;
        const formatted = lines.map(line => {
            const trimmed = line.trim();
            if (!trimmed) return '';
            
            // Decrease indent for certain keywords
            if (trimmed.match(/^(except|elif|else|finally):/)) {
                indentLevel = Math.max(0, indentLevel - 1);
            }
            
            const formatted = '    '.repeat(indentLevel) + trimmed;
            
            // Increase indent after certain keywords
            if (trimmed.endsWith(':')) {
                indentLevel++;
            }
            
            return formatted;
        }).join('\n');
        
        codeEditor.setValue(formatted);
    }
    
    if (window.WSG && window.WSG.showToast) {
        window.WSG.showToast('Code formatted!', 'success');
    }
}

/**
 * Insert snippet at cursor
 */
function insertSnippet(snippet) {
    if (!codeEditor) return;
    
    const cursor = codeEditor.getCursor();
    codeEditor.replaceRange(snippet, cursor);
    codeEditor.focus();
}

/**
 * Get editor statistics
 */
function getEditorStats() {
    if (!codeEditor) return null;
    
    const code = codeEditor.getValue();
    const lines = code.split('\n');
    
    return {
        lines: lines.length,
        characters: code.length,
        charactersNoSpaces: code.replace(/\s/g, '').length,
        words: code.trim() ? code.trim().split(/\s+/).length : 0
    };
}

/**
 * Common code snippets for different languages
 */
const codeSnippets = {
    python: {
        'for_loop': 'for i in range(10):\n    print(i)',
        'function': 'def function_name(parameter):\n    return parameter',
        'class': 'class ClassName:\n    def __init__(self):\n        pass',
        'try_catch': 'try:\n    # code here\n    pass\nexcept Exception as e:\n    print(f"Error: {e}")'
    },
    javascript: {
        'for_loop': 'for (let i = 0; i < 10; i++) {\n    console.log(i);\n}',
        'function': 'function functionName(parameter) {\n    return parameter;\n}',
        'arrow_function': 'const functionName = (parameter) => {\n    return parameter;\n};',
        'try_catch': 'try {\n    // code here\n} catch (error) {\n    console.error("Error:", error);\n}'
    },
    bash: {
        'for_loop': 'for i in {1..10}; do\n    echo $i\ndone',
        'function': 'function_name() {\n    echo "Hello, $1!"\n}',
        'if_statement': 'if [ "$variable" = "value" ]; then\n    echo "Match found"\nfi',
        'while_loop': 'while [ $counter -lt 10 ]; do\n    echo $counter\n    counter=$((counter + 1))\ndone'
    }
};

// Export functions for global access
window.WSGEditor = {
    executeCode,
    clearEditor,
    loadExample,
    changeEditorLanguage,
    formatCode,
    insertSnippet,
    getEditorStats,
    codeSnippets
};

// Initialize editor when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        // Re-initialize if needed
        if (!codeEditor) {
            setTimeout(initializeCodeEditor, 100);
        }
    });
}
