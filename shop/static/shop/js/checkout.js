document.addEventListener('DOMContentLoaded', function() {
    // --- Display Cart Summary on Page Load ---
    async function displayCheckoutSummary() {
        const response = await fetch('/api/cart/');
        if (!response.ok) return;

        const cartData = await response.json();
        const summaryBody = document.getElementById('checkout-summary-body');
        const totalSpan = document.getElementById('summary-total');

        if (summaryBody) {
            summaryBody.innerHTML = '';
            if (cartData && cartData.items) {
                cartData.items.forEach(item => {
                    summaryBody.innerHTML += `
                        <tr>
                            <td>${item.product.name} (x${item.quantity})</td>
                            <td>£${item.total_price}</td>
                        </tr>
                    `;
                });
            }
        }

        if (totalSpan) {
            totalSpan.textContent = cartData.grand_total || '0.00';
        }
    }
    
    displayCheckoutSummary(); // Run the function as soon as the page loads

    // --- Handle Form Submission ---
const checkoutForm = document.getElementById('checkout-form');
if (checkoutForm) {
    checkoutForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        // Collect form data
        const formData = {
            first_name: document.getElementById('fname').value,
            last_name: document.getElementById('lname').value,
            email: document.getElementById('email').value,
            address: document.getElementById('address1').value,
            city: document.getElementById('city').value,
            postcode: document.getElementById('postcode').value,
        };

        // Add validation for the pretend payment fields 
        const cardNumber = document.getElementById('card-number').value;
        const expiry = document.getElementById('expiry').value;
        const cvv = document.getElementById('cvv').value;

        // Basic validation
        for (const field in formData) {
            if (!formData[field]) {
                alert(`Please fill out the ${field.replace('_', ' ')} field.`);
                return;
            }
        }

        // Pretend payment validation
        if (!cardNumber || !expiry || !cvv) {
            alert('Please fill out all payment details.');
            return;
        }

        const csrftoken = getCookie('csrftoken');

        // Send ONLY the shipping data to the checkout API
        const response = await fetch('/api/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(formData) // NEVER send the card details
        });

        if (response.ok) {
            alert('Order placed successfully!');
            window.location.href = '/order-complete/'; 
        } else {
            const errorData = await response.json();
            console.error('Checkout failed:', errorData);
            alert('There was an error placing your order.');
        }
    });
}
});