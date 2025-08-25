document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * A helper function to get a cookie by name
     * @param {string} name - The name of the cookie to retrieve
     * @returns {string|null} The value of the cookie/null if not found
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const csrftoken = getCookie('csrftoken');
            const formData = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                username: document.getElementById('email').value, // Use email for username
                password: document.getElementById('password').value
            };

            const response = await fetch('/api/auth/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                window.location.href = '/dashboard/'; // Redirect to dashboard on success
            } else {
                alert('Registration failed. An account with this email may already exist.');
            }
        });
    }

    // Login functionality
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };

            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                window.location.href = '/dashboard/'; // Redirect to dashboard on success
            } else {
                alert('Login failed. Please check your email and password.');
            }
        });
    }
});