// This event listener ensures the script runs only after the HTML document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // --- Helper function to get CSRF token from the browser's cookies ---
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
    // An asynchronous function to fetch cart data + populate the order summary
    async function displayCheckoutSummary() {
        const response = await fetch('/api/cart/');
        if (!response.ok) return;

        const cartData = await response.json();
        const summaryBody = document.getElementById('checkout-summary-body');
        const totalSpan = document.getElementById('summary-total');
        const charityDisplay = document.getElementById('charity-donation-display');
        // Get the charity choice that was saved on the previous page
        const selectedCharity = localStorage.getItem('selectedCharity');
        const charityAmount = (parseFloat(cartData.grand_total || '0') * 0.1).toFixed(2);

         // Populate the table with a summary of items in the cart
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
        // Update the total price
        if (totalSpan) {
            totalSpan.textContent = cartData.grand_total || '0.00';
        }

        // If a charity was selected (it should be, you cannot proceed to cart without doing so!), create + display the confirmation message 
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
            event.preventDefault(); // Stop the form from refreshing the page

            const selectedCharity = localStorage.getItem('selectedCharity');
            const csrftoken = getCookie('csrftoken');

            // Collect all the shipping details from the form inputs
            const formData = {
                first_name: document.getElementById('fname').value,
                last_name: document.getElementById('lname').value,
                email: document.getElementById('email').value,
                address: document.getElementById('address1').value,
                city: document.getElementById('city').value,
                postcode: document.getElementById('postcode').value,
                charity_choice: selectedCharity // Include the saved charity choice
            };

            // Basic validation to ensure fields are NOT empty!!
            for (const field in formData) {
                if (field !== 'charity_choice' && !formData[field]) {
                    alert(`Please fill out the ${field.replace('_', ' ')} field.`);
                    return;
                }
            }

            // Send the form data to the backend checkout API
            const response = await fetch('/api/checkout/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify(formData)
            });

            // If the order is created successfully, redirect to the confirmation page
            if (response.ok) {
                localStorage.removeItem('selectedCharity'); // Clean up the saved charity
                window.location.href = '/order-complete/'; 
            } else {
                alert('There was an error placing your order.');
            }
        });
    }
});