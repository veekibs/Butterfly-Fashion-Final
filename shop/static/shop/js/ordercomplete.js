// This event listener ensures the script runs only after the HTML document has been fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Find the optional "Create Account" form on the page
    const createAccountForm = document.getElementById('create-account-form');

    // If the form exists, add an event listener to handle its submission
    if (createAccountForm) {
        createAccountForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            // Get the necessary data from the form fields
            const orderId = document.getElementById('order-id').value;
            const password = document.getElementById('password').value;
            const passwordConfirm = document.getElementById('password-confirm').value;

            // CLIENT SIDE VALIDATION
            if (password !== passwordConfirm) {
                alert('Passwords do not match.');
                return; // Stop the function if passwords don't match 
            }
            if (password.length < 8) {
                alert('Password must be at least 8 characters long.');
                return; // Stop the function if the password is too short 
            }

            // Get the CSRF token for the secure POST request
            const csrftoken = getCookie('csrftoken');

            // Send the order ID + new password to the account creation API
            const response = await fetch('/api/create-account/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    order_id: orderId,
                    password: password
                })
            });

            // Handle the response from the server 
            if (response.ok) {
                alert('Account created successfully! You can now log in with your email and new password.');
                // Hide the form after successful creation so the user cannot submit it again
                createAccountForm.style.display = 'none';  
            } else {
                // If there's an error (e.g. email already in use!), show the error message from the API
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        });
    }
});

// Helper function to get a specific cookie by its name (needed for the CSRF token)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}