// --- MAIN APP INITIALIZATION & ROUTER ---

/**
 * This is the main entry point. It runs when the HTML document is FULLY loaded.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Always get the initial cart count on every page load
    onLoadCartNumbers(); 

    const page = document.body.dataset.page;
    if (page === 'cart') {
        // On the cart page, display the cart + then set up its listeners
        displayCart();
        setupEventListeners();
    } else if (document.querySelector('.fprocontainer, .fpcontainer')) {
        // On pages with products, let initializePage handle everything
        // It will set up its own listeners AFTER the products are loaded
        initializePage();
    } else {
        // On simple static pages (like About), just set up the basic listeners
        setupEventListeners();
    }
});

// This is the corresponding initializePage function that now handles its own event listeners
async function initializePage() {
    const products = await fetchProducts();
    if (products) {
        renderProducts(products);
        // Event listeners are set up here, only AFTER products are on the page
        setupEventListeners();
    }
}

// --- UI EFFECTS ---

/**
 * Adds a scroll effect to the header, making it solid after scrolling down.
 */
window.addEventListener('scroll', () => {
    const header = document.getElementById('header');
    if (header) { // Check if header exists
        if (window.scrollY > 50) { // If scrolled more than 50px
            header.classList.add('header-scrolled');
        } else {
            header.classList.remove('header-scrolled');
        }
    }
});

// --- PRODUCT FETCHING & RENDERING ---

/**
 * Fetches the entire product catalog from the backend API
 * @returns {Promise<Array|null>} A promise that resolves to an array of products/null on error
 */
async function fetchProducts() {
    try {
        const response = await fetch('/api/products/');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Could not fetch products:', error);
        displayErrorMessage();
        return null;
    }
}

/**
 * Renders the correct products into the correct containers based on the current page
 * @param {Array} products - The array of all product objects
 */
function renderProducts(products) {
    const page = document.body.dataset.page;
    switch (page) {
        case 'home':
            const preteenContainerHome = document.querySelector('#fproduct .fprocontainer');
            const teenContainerHome = document.querySelector('#fproductt .fpcontainer');
            if (preteenContainerHome) renderProductList(products.filter(p => p.category === 'preteen' && p.is_featured), preteenContainerHome, 'fpro');
            if (teenContainerHome) renderProductList(products.filter(p => p.category === 'teen' && p.is_featured), teenContainerHome, 'fp');
            break;
        case 'preteens':
            const preteenContainer = document.querySelector('.fprocontainer');
            if (preteenContainer) renderProductList(products.filter(p => p.category === 'preteen' && !p.is_new_arrival), preteenContainer, 'fpro');
            break;
        case 'teens':
            const teenContainer = document.querySelector('.fpcontainer');
            if (teenContainer) renderProductList(products.filter(p => p.category === 'teen' && !p.is_new_arrival), teenContainer, 'fp');
            break;
        case 'newarrivals':
            const preteenContainerNA = document.querySelector('#fproduct .fprocontainer');
            const teenContainerNA = document.querySelector('#fproductt .fpcontainer');
            if (preteenContainerNA) renderProductList(products.filter(p => p.category === 'preteen' && p.is_new_arrival), preteenContainerNA, 'fpro');
            if (teenContainerNA) renderProductList(products.filter(p => p.category === 'teen' && p.is_new_arrival), teenContainerNA, 'fp');
            break;
    }
}

/**
 * Renders a list of products into a given HTML container
 */
function renderProductList(productList, container, proClass) {
    if (!container) return;
    container.innerHTML = '';
    productList.forEach(product => {
        container.innerHTML += createProductHtml(product, proClass);
    });
}

/**
 * Creates the HTML string for a single product card, including two images for the hover effect
 */
function createProductHtml(product, proClass) {
    const productImage = `/static/${product.image_url}`;
    const modelImage = product.model_image_url ? `/static/${product.model_image_url}` : productImage;

    // This now correctly includes both the proClass (fpro/fp) + the sub_category for filtering 
    return `
        <div class="${proClass} ${product.sub_category}" data-product-id="${product.id}">
            <div class="image-container">
                <img class="product-shot" src="${productImage}" alt="${product.name}">
                <img class="model-shot" src="${modelImage}" alt="${product.name} worn by model">
            </div>
            <div class="card-body">
                <div class="info">
                    <h5>${product.name}</h5>
                    <h4>£${product.price}</h4>
                </div>
                <a class="cart"><ion-icon name="cart-outline"></ion-icon></a>
            </div>
        </div>
    `;
}

/**
 * Displays a generic error message in product containers if the API fails
 */
function displayErrorMessage() {
    const containers = document.querySelectorAll('.fprocontainer, .fpcontainer');
    containers.forEach(container => {
        if (container) {
            container.innerHTML = '<p style="text-align:center; color:red;">Oops! Could not load products.</p>';
        }
    });
}

// --- EVENT LISTENERS & CSRF TOKEN ---

/**
 * Sets up global event listeners for the entire application
 */
function setupEventListeners() {
    // This listener is now set up only ONCE per page load
    document.body.addEventListener('click', function(event) {
        const addToCartBtn = event.target.closest('.cart');
        if (addToCartBtn) {
            const productElement = addToCartBtn.closest('[data-product-id]');
            if (productElement) addToCart(productElement.dataset.productId);
        }
        const removeFromCartBtn = event.target.closest('.remove-item');
        if (removeFromCartBtn) {
            removeFromCart(removeFromCartBtn.dataset.itemId);
        }
    });

    // Specific listener for the checkout form
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        console.log("Checkout form submitted!"); // <- debug
        await validateCart(event);
    });
    }

    // Specific listeners for the homepage UX popup
    const popupContainer = document.getElementById('popup');
    if (popupContainer) {
        const arrowUp = popupContainer.querySelector('.arrow-up');
        const arrowDown = popupContainer.querySelector('.arrow-down');
        const sendButton = popupContainer.querySelector('.sendbutton');
        const inputField = popupContainer.querySelector('input[type="text"]');

        if(arrowUp) arrowUp.addEventListener('click', () => popupContainer.classList.remove('minimized'));
        if(arrowDown) arrowDown.addEventListener('click', () => popupContainer.classList.add('minimized'));
        if(sendButton) sendButton.addEventListener('click', () => {
            if (inputField.value.trim() === "") {
                alert("Please enter a message.");
            } else {
                alert('Message sent. Thank you!');
                inputField.value = '';
                popupContainer.classList.add('minimized');
            }
        });
    }

    // --- Charity Selector Listener ---
    const charitySelect = document.getElementById('charity-select');
    if (charitySelect) {
        charitySelect.addEventListener('change', function() {
            const selectedCharity = this.options[this.selectedIndex].text;
            if (this.value !== "0") {
                localStorage.setItem('selectedCharity', selectedCharity);
            } else {
                localStorage.removeItem('selectedCharity');
            }
        });
    }

    // --- Product Filter Logic ---
    const filterItems = document.querySelectorAll('.product-filter .filter-item');
    if (filterItems.length > 0) {
        filterItems.forEach(item => {
            item.addEventListener('click', function() {
                filterItems.forEach(i => i.classList.remove('active-filter'));
                this.classList.add('active-filter');

                const filterValue = this.dataset.filter;
                // MUST find the product boxes *inside* the click event
                const productBoxes = document.querySelectorAll('.fpro, .fp'); 
                
                productBoxes.forEach(box => {
                    if (filterValue === 'all' || box.classList.contains(filterValue)) {
                        box.style.display = 'block'; // Show
                    } else {
                        box.style.display = 'none'; // Hide
                    }
                });
            });
        });
    }
}

/**
 * A helper function to get the CSRF token from the page's cookies
 */
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
const csrftoken = getCookie('csrftoken');

// --- CART LOGIC (API DRIVEN) ---

/**
 * Adds a product to the server-side cart
 */
async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ product_id: productId })
        });
        if (response.ok) {
            await onLoadCartNumbers(); // Re-fetch cart state to update icon
        } else {
            throw new Error('Failed to add item.');
        }
    } catch (error) {
        console.error(error);
        alert('Could not add item. Please try again.');
    }
}

/**
 * Removes an item from the server-side cart
 */
async function removeFromCart(itemId) {
    try {
        const response = await fetch('/api/cart/remove/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify({ item_id: itemId })
        });
        if (response.ok) {
            await displayCart(); // Re-render the cart item list
            await onLoadCartNumbers(); // Re-fetch the total for the header icon
        } else {
            throw new Error('Failed to remove item.');
        }
    } catch (error) {
        console.error(error);
        alert('Could not remove item. Please try again.');
    }
}

/**
 * Fetches the current cart state from the API to update the cart icon
 */
async function onLoadCartNumbers() {
    try {
        const response = await fetch('/api/cart/');
        if (response.ok) {
            const cartData = await response.json();
            updateCartIcon(cartData);
        }
    } catch (error) {
        console.error("Could not fetch cart count.", error);
    }
}

/**
 * Updates the cart number in the header
 */
function updateCartIcon(cartData) {
    const cartSpan = document.getElementById("cart-count");
    if (cartSpan) {
        let totalQuantity = 0;
        if (cartData && cartData.items) {
            totalQuantity = cartData.items.reduce((sum, item) => sum + item.quantity, 0);
        }
        cartSpan.textContent = totalQuantity;
    }
}

/**
 * Fetches the full cart details from the API + renders them on the cart page
 */
async function displayCart() {
    try {
        const response = await fetch('/api/cart/');
        if (!response.ok) throw new Error("Failed to fetch cart data.");
        
        const cartData = await response.json();
        const cartBody = document.querySelector('#cart-table-body');
        if (!cartBody) return;

        cartBody.innerHTML = '';

        if (cartData && cartData.items && cartData.items.length > 0) {
            cartData.items.forEach(item => {
                const imagePath = `/static/${item.product.image_url}`;
                cartBody.innerHTML += `
                    <tr>
                        <td><a class="remove-item" data-item-id="${item.id}"><ion-icon name="trash-outline"></ion-icon></a></td>
                        <td><img src="${imagePath}" alt="${item.product.name}" style="width: 80px;"></td>
                        <td>${item.product.name}</td>
                        <td>£${item.product.price}</td>
                        <td>${item.quantity}</td>
                        <td>£${item.total_price}</td>
                    </tr>
                `;
            });
        } else {
            cartBody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Your cart is empty.</td></tr>';
        }
        updateCartTotals(cartData);
    } catch (error) {
        console.error(error);
    }
}

/**
 * Updates the totals table on the cart page
 */
function updateCartTotals(cartData) {
    const subtotalEl = document.getElementById("subtotal");
    const charityEl = document.getElementById("charity-amount");
    const totalEl = document.getElementById("cart-total");

    if (subtotalEl && charityEl && totalEl) {
        const subtotal = parseFloat(cartData.grand_total || '0').toFixed(2);
        const charityAmount = (subtotal * 0.1).toFixed(2);
        subtotalEl.textContent = subtotal;
        charityEl.textContent = charityAmount;
        totalEl.textContent = subtotal;
    }
}

/**
 * Validates the cart before allowing the user to proceed to checkout
 */
async function validateCart(event) {
    event.preventDefault();
    const form = event.target;
    const checkoutUrl = form.dataset.checkoutUrl;

    try {
        const response = await fetch('/api/cart/');
        const cartData = await response.json();
        const charitySelect = document.getElementById('charity-select');
        
        if (!cartData.items || cartData.items.length === 0) {
          alert('Please add at least one item to your cart before proceeding!');
        } else if (charitySelect.value === "0") {
          alert('Please select a charity before proceeding!');
        } else {
          window.location.href = checkoutUrl; 
        }
    } catch (error) {
        console.error("Validation failed:", error);
    }
}