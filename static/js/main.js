// Wolf Shell Generator (WSG) - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize theme handling
    initializeTheme();
    
    // Initialize animations
    initializeAnimations();
    
    // Auto-dismiss alerts
    autoDismissAlerts();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize theme handling
 */
function initializeTheme() {
    // Add glass effect to cards on scroll
    window.addEventListener('scroll', function() {
        const cards = document.querySelectorAll('.glass-card');
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
            
            if (isVisible) {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }
        });
    });
}

/**
 * Initialize scroll animations
 */
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate
    document.querySelectorAll('.feature-card, .stats-card, .language-card').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    if (!element) return;
    
    const originalContent = element.innerHTML;
    element.setAttribute('data-original-content', originalContent);
    element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    element.disabled = true;
}

/**
 * Hide loading spinner
 */
function hideLoading(element) {
    if (!element) return;
    
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
    }
    element.disabled = false;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast glass-card" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="fas fa-${getIconForType(type)} text-${type} me-2"></i>
                <strong class="me-auto">WSG</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Create toast container if it doesn't exist
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Get icon for toast type
 */
function getIconForType(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle',
        danger: 'exclamation-triangle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        showToast('Failed to copy to clipboard', 'error');
    });
}

/**
 * Format code for display
 */
function formatCode(code, language) {
    // Basic code formatting - in a real app, you might use a syntax highlighter
    return code.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
}

/**
 * Validate form inputs
 */
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

/**
 * Handle form submission with loading states
 */
function handleFormSubmission(form, onSubmit) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!validateForm(form)) {
            showToast('Please fill in all required fields', 'error');
            return;
        }
        
        const submitBtn = form.querySelector('button[type="submit"]');
        showLoading(submitBtn);
        
        // Call the provided submit handler
        Promise.resolve(onSubmit(form)).finally(() => {
            hideLoading(submitBtn);
        });
    });
}

/**
 * Initialize progress tracking
 */
function initializeProgressTracking() {
    // Track page views and interactions for learning analytics
    const startTime = Date.now();
    
    window.addEventListener('beforeunload', function() {
        const timeSpent = Date.now() - startTime;
        // In a real app, you might send this data to your analytics service
        console.log(`Time spent on page: ${timeSpent}ms`);
    });
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to run code (if in editor)
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const runButton = document.querySelector('.btn-success[onclick*="executeCode"]');
        if (runButton) {
            e.preventDefault();
            runButton.click();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) modal.hide();
        }
    }
});

// Initialize progress tracking
initializeProgressTracking();

// Export functions for use in other scripts
window.WSG = {
    showLoading,
    hideLoading,
    showToast,
    copyToClipboard,
    formatCode,
    validateForm,
    handleFormSubmission
};
