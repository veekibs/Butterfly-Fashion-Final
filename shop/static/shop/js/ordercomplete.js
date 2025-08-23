document.addEventListener('DOMContentLoaded', function() {
    const createAccountForm = document.getElementById('create-account-form');

    if (createAccountForm) {
        createAccountForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const orderId = document.getElementById('order-id').value;
            const password = document.getElementById('password').value;
            const passwordConfirm = document.getElementById('password-confirm').value;

            if (password !== passwordConfirm) {
                alert('Passwords do not match.');
                return;
            }
            if (password.length < 8) {
                alert('Password must be at least 8 characters long.');
                return;
            }

            const csrftoken = getCookie('csrftoken');

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

            if (response.ok) {
                alert('Account created successfully! You can now log in with your email and new password.');
                // Hide the form after successful creation
                createAccountForm.style.display = 'none'; 
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        });
    }
});

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