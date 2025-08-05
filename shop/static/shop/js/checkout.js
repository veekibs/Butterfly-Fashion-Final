document.addEventListener('DOMContentLoaded', function() {
    
    // --- Helper function to get CSRF token ---
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

    // --- Display Cart + Charity Summary on Page Load ---
    async function displayCheckoutSummary() {
        const response = await fetch('/api/cart/');
        if (!response.ok) return;

        const cartData = await response.json();
        const summaryBody = document.getElementById('checkout-summary-body');
        const totalSpan = document.getElementById('summary-total');
        const charityDisplay = document.getElementById('charity-donation-display');
        const selectedCharity = localStorage.getItem('selectedCharity');
        const charityAmount = (parseFloat(cartData.grand_total || '0') * 0.1).toFixed(2);

        if (summaryBody) {
            summaryBody.innerHTML = '';
            if (cartData && cartData.items) {
                cartData.items.forEach(item => {
                    summaryBody.innerHTML += `
                        <tr>
                            <td>${item.product.name} (x${item.quantity})</td>
                            <td style="text-align:right;">£${item.total_price}</td>
                        </tr>
                    `;
                });
            }
        }
        if (totalSpan) {
            totalSpan.textContent = cartData.grand_total || '0.00';
        }

        // Display the selected charity message 
        if (charityDisplay && selectedCharity && selectedCharity !== "select a charity...") {
            charityDisplay.innerHTML = `you are donating £${charityAmount} to <strong>${selectedCharity}</strong>. thank you!`;
            charityDisplay.style.display = 'block'; // Make it visible
        } else if (charityDisplay) {
            charityDisplay.style.display = 'none'; // Hide it if no charity is selected
        }
    }
    
    displayCheckoutSummary(); // Run the function on page load

    // --- Handle Form Submission ---
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', async function(event) {
            event.preventDefault();

            const selectedCharity = localStorage.getItem('selectedCharity');
            const csrftoken = getCookie('csrftoken');
            const formData = {
                first_name: document.getElementById('fname').value,
                last_name: document.getElementById('lname').value,
                email: document.getElementById('email').value,
                address: document.getElementById('address1').value,
                city: document.getElementById('city').value,
                postcode: document.getElementById('postcode').value,
                charity_choice: selectedCharity
            };

            // Basic validation...
            for (const field in formData) {
                if (field !== 'charity_choice' && !formData[field]) {
                    alert(`Please fill out the ${field.replace('_', ' ')} field.`);
                    return;
                }
            }

            // Send data to the checkout API
            const response = await fetch('/api/checkout/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                localStorage.removeItem('selectedCharity'); // Clean up
                window.location.href = '/order-complete/'; 
            } else {
                alert('There was an error placing your order.');
            }
        });
    }
});