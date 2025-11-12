/**
 * Authentication JavaScript for login and registration
 */

// Helper function to show error messages
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');

    errorDiv.textContent = message;
    errorDiv.classList.remove('d-none');
    successDiv.classList.add('d-none');
}

// Helper function to show success messages
function showSuccess(message) {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');

    successDiv.textContent = message;
    successDiv.classList.remove('d-none');
    errorDiv.classList.add('d-none');
}

// Helper function to hide all messages
function hideMessages() {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');

    errorDiv.classList.add('d-none');
    successDiv.classList.add('d-none');
}

// Handle login form submission
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessages();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Store the token in localStorage
                localStorage.setItem('access_token', data.access_token);

                // Show success message
                showSuccess('Login successful! Redirecting...');

                // Redirect to the home page
                setTimeout(() => {
                    window.location.href = '/home';
                }, 1000);
            } else {
                showError(data.detail || 'Login failed. Please try again.');
            }
        } catch (error) {
            showError('An error occurred. Please try again.');
            console.error('Login error:', error);
        }
    });
}

// Handle registration form submission
const registerForm = document.getElementById('register-form');
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessages();

        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Validate password match
        if (password !== confirmPassword) {
            showError('Passwords do not match!');
            return;
        }

        // Validate password length
        if (password.length < 6) {
            showError('Password must be at least 6 characters long!');
            return;
        }

        // Validate username length
        if (username.length < 3) {
            showError('Username must be at least 3 characters long!');
            return;
        }

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                showSuccess('Registration successful! Redirecting to login...');

                // Redirect to login page after 2 seconds
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                showError(data.detail || 'Registration failed. Please try again.');
            }
        } catch (error) {
            showError('An error occurred. Please try again.');
            console.error('Registration error:', error);
        }
    });
}
