// This event listener ensures that the code inside it only runs after the entire HTML document has been loaded + parsed
document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * A helper function to get a specific cookie by its name
     * This is necessary to retrieve the CSRF token for making secure POST requests to Django
     * @param {string} name - The name of the cookie to retrieve (e.g., 'csrftoken')
     * @returns {string|null} The value of the cookienull if it's not found
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Get the CSRF token once + store it in a variable
    const csrftoken = getCookie('csrftoken');

    // --- Registration Form Logic ---
    // Find the registration form on the page
    const registerForm = document.getElementById('register-form');
    // If the form exists, add an event listener to handle its submission
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            // Prevent the default browser action of refreshing the page on form submission
            event.preventDefault();
            
            // Collect all the data from the input fields
            const formData = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                username: document.getElementById('email').value, // Use the email as the username for simplicity
                password: document.getElementById('password').value
            };

            // Send the collected data to the backend registration API endpoint
            const response = await fetch('/api/auth/register/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // Include the CSRF token for security
                },
                body: JSON.stringify(formData)
            });

            // If the backend responds with a success status, redirect to the dashboard
            if (response.ok) {
                window.location.href = '/dashboard/';
            } else {
                // If there's an error, show an alert to the user
                alert('Registration failed. An account with this email may already exist.');
            }
        });
    }

    // --- Login Form Logic ---
    // Find the login form on the page
    const loginForm = document.getElementById('login-form');
    // If the form exists, add an event listener to handle its submission
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Collect the username (email) + password from the form
            const formData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };

            // Send the data to the backend login API endpoint
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken 
                },
                body: JSON.stringify(formData)
            });

            // If the login is successful, redirect to the dashboard
            if (response.ok) {
                window.location.href = '/dashboard/';
            } else {
                // If the credentials are incorrect, show an alert
                alert('Login failed. Please check your email and password.');
            }
        });
    }
});