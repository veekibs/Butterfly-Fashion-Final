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

    // --- MOBILE HAMBURGER MENU ---
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    hamburger.addEventListener('click', (e) => {
        e.stopPropagation(); // prevent click from bubbling to document
        mobileMenu.classList.toggle('active');
    });

    // Click anywhere outside to close
    document.addEventListener('click', (e) => {
        if (!mobileMenu.contains(e.target) && !hamburger.contains(e.target)) {
            mobileMenu.classList.remove('active');
        }
    });
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
        const response = await fetch('/api/products/'); // fetch products from server
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); // check for errors
        return await response.json(); // return JSON if successful
    } catch (error) {
        console.error('Could not fetch products:', error); // log errors
        displayErrorMessage(); // show error message in UI
        return null; // return null on failure
    }
}

/**
 * Renders the correct products into the correct containers based on the current page
 * @param {Array} products - The array of all product objects
 */
function renderProducts(products) {
    const page = document.body.dataset.page; // get current page from body data attribute
    switch (page) {
        case 'home': // homepage shows featured products
            const preteenContainerHome = document.querySelector('#fproduct .fprocontainer');
            const teenContainerHome = document.querySelector('#fproductt .fpcontainer');
            if (preteenContainerHome) renderProductList(products.filter(p => p.category === 'preteen' && p.is_featured), preteenContainerHome, 'fpro');
            if (teenContainerHome) renderProductList(products.filter(p => p.category === 'teen' && p.is_featured), teenContainerHome, 'fp');
            break;
        case 'preteens': // preteens page shows regular preteen products
            const preteenContainer = document.querySelector('.fprocontainer');
            if (preteenContainer) renderProductList(products.filter(p => p.category === 'preteen' && !p.is_new_arrival), preteenContainer, 'fpro');
            break;
        case 'teens': // teens page shows regular teen products
            const teenContainer = document.querySelector('.fpcontainer');
            if (teenContainer) renderProductList(products.filter(p => p.category === 'teen' && !p.is_new_arrival), teenContainer, 'fp');
            break;
        case 'newarrivals': // new arrivals page
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
    if (!container) return; // skip if container doesn't exist 
    container.innerHTML = ''; // clear existing content 
    productList.forEach(product => {
        container.innerHTML += createProductHtml(product, proClass); // add each product card
    });
}

/**
 * Creates the HTML string for a single product card, including two images for the hover effect
 */
function createProductHtml(product, proClass) {
    const productImage = `/static/${product.image_url}`; // main product image
    const modelImage = product.model_image_url ? `/static/${product.model_image_url}` : productImage; // fallback if no model image!

    // This now correctly includes both the proClass (fpro/fp) + the sub_category for filtering 
    // Returns product card HTML
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
    // Listens to clicks anywhere in the body 
    document.body.addEventListener('click', function(event) {
        const addToCartBtn = event.target.closest('.cart'); // Check if clicked element is an add-to-cart button
        if (addToCartBtn) {
            const productElement = addToCartBtn.closest('[data-product-id]');
            if (productElement) addToCart(productElement.dataset.productId);
        }
        const removeFromCartBtn = event.target.closest('.remove-item'); // Check if clicked element is a remove-from-cart button
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
        await validateCart(event); // Validate cart before proceeding
    });
    }

    // --- Popup Feedback Logic ---
    const popup = document.getElementById('popup'); 
    const stripe = document.getElementById('popup-stripe'); // Top handle
    const arrow = document.getElementById('popup-arrow'); // Arrow icon
    const inputField = document.getElementById('feedback-input'); // Feedback input
    const sendButton = document.getElementById('send-feedback'); // Send button
    const feedbackMsg = document.getElementById('feedback-msg'); // Message after sending feedback

    if (popup && stripe && arrow && inputField && sendButton && feedbackMsg) {
       // toggle popup/open minimised on stripe click
        stripe.addEventListener('click', () => {
            popup.classList.toggle('minimized');
            popup.classList.toggle('show');
            arrow.style.transform = popup.classList.contains('minimized') // flip arrow
                ? 'rotate(0deg)'
                : 'rotate(180deg)';
        });

        // Send feedback button click 
        sendButton.addEventListener('click', () => {
            if (!inputField.value.trim()) { // if input empty
                inputField.style.borderColor = '#ff6b6b';
                inputField.style.animation = 'shake 0.3s'; // shake animation
                inputField.addEventListener('animationend', () => inputField.style.animation = '');
                return;
            }
            feedbackMsg.textContent = '🎉 feedback sent!';
            feedbackMsg.classList.remove('hidden');
            sendButton.disabled = true;
            inputField.disabled = true;

            setTimeout(() => { // minimise popup after short delay
                popup.classList.add('minimized');
                popup.classList.remove('show');
                arrow.style.transform = 'rotate(0deg)';
            }, 1200);
        });
    }

    // --- Charity Selector Listener ---
    const charitySelect = document.getElementById('charity-select');
    if (charitySelect) {
        charitySelect.addEventListener('change', function() {
            const selectedCharity = this.options[this.selectedIndex].text;
            if (this.value !== "0") {
                localStorage.setItem('selectedCharity', selectedCharity); // store selection locally 
            } else {
                localStorage.removeItem('selectedCharity'); // remove if 'select' option chosen
            }
        });
    }

    // --- Product Filter Logic ---
    const filterItems = document.querySelectorAll('.product-filter .filter-item');
    if (filterItems.length > 0) {
        filterItems.forEach(item => {
            item.addEventListener('click', function() {
                filterItems.forEach(i => i.classList.remove('active-filter')); // remove active from other
                this.classList.add('active-filter'); // highlight clicked filter

                const filterValue = this.dataset.filter;
                // MUST find the product boxes *inside* the click event
                const productBoxes = document.querySelectorAll('.fpro, .fp');  // ALL PRODUCT CARDS
                
                // show/hide products depending on filter 
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

    // NEW MOBILE MENU LOGIC 
    const menuOpen = document.getElementById('mobile-menu-open');
    const menuClose = document.getElementById('mobile-menu-close');
    const mobileNav = document.getElementById('mobile-nav'); 
    const navbar = document.getElementById('navbar');
    const mobileNavLinks = document.querySelectorAll('#mobile-nav a');

    if (menuOpen && navbar) {
        menuOpen.addEventListener('click', () => {
            navbar.classList.add('active');
        });
    }

    if (menuClose && navbar) {
        menuClose.addEventListener('click', () => {
            navbar.classList.remove('active');
        });
    }

    // CLOSE THE MENU WHEN A LINK IS CLICKED 
    if (mobileNavLinks.length > 0 && mobileNav) {
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('active');
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
const csrftoken = getCookie('csrftoken'); // store csrf token for API requests

// --- CART LOGIC ---

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