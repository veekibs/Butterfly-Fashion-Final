// === MAIN APP LOGIC =================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Uses the body class to identify the cart page
    if (document.body.classList.contains('cart-page')) {
        displayCart();
    } else {
        // On all other pages, display products
        initializePage();
    }

    // These run on every page load
    setupEventListeners();
    onLoadCartNumbers();
});

// === PRODUCT FETCHING + RENDERING ===================================================

/**
 * Initialises a product-displaying page
 */
async function initializePage() {
    const products = await fetchProducts();
    if (products) {
        renderProducts(products);
    }
}

/**
 * Fetches the entire product catalog from the backend API
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
 * Renders products into the correct containers based on the current page
 * @param {Array} products - The array of all product objects
 */
function renderProducts(products) {
    const pageBody = document.body;

    // Homepage logic
    if (document.querySelector('#landing')) { // A simple way to detect the homepage
        const preteenContainer = document.querySelector('#fproduct .fprocontainer');
        const teenContainer = document.querySelector('#fproductt .fpcontainer');
        if (preteenContainer) renderProductList(products.filter(p => p.category === 'preteen' && !p.is_new_arrival).slice(0, 8), preteenContainer, 'fpro');
        if (teenContainer) renderProductList(products.filter(p => p.category === 'teen' && !p.is_new_arrival).slice(0, 8), teenContainer, 'fp');
    }
    // Preteens page logic
    else if (document.querySelector('#preteen-tops')) {
        const topsContainer = document.querySelector('#preteen-tops .fprocontainer');
        const bottomsContainer = document.querySelector('#preteen-bottoms .fpcontainer');
        const preteenProducts = products.filter(p => p.category === 'preteen' && !p.is_new_arrival);
        if (topsContainer) {
            const tops = preteenProducts.filter(p => p.sub_category === 'top');
            renderProductList(tops, topsContainer, 'fpro');
        }
        if (bottomsContainer) {
            const bottoms = preteenProducts.filter(p => p.sub_category === 'bottom');
            renderProductList(bottoms, bottomsContainer, 'fp');
        }
    }
    // Teens page logic
    else if (document.querySelector('#teen-tops')) {
        const topsContainer = document.querySelector('#teen-tops .fpcontainer');
        const bottomsContainer = document.querySelector('#teen-bottoms .fpcontainer');
        const teenProducts = products.filter(p => p.category === 'teen' && !p.is_new_arrival);
        if (topsContainer) {
            const tops = teenProducts.filter(p => p.sub_category === 'top');
            renderProductList(tops, topsContainer, 'fp');
        }
        if (bottomsContainer) {
            const bottoms = teenProducts.filter(p => p.sub_category === 'bottom');
            renderProductList(bottoms, bottomsContainer, 'fp');
        }
    }
    // New Arrivals page logic
    else if (document.querySelector('title').textContent.includes('New Arrivals')) { // Detect by page title
        const preteenContainer = document.querySelector('#fproduct .fprocontainer');
        const teenContainer = document.querySelector('#fproductt .fpcontainer');
        if (preteenContainer) renderProductList(products.filter(p => p.category === 'preteen' && p.is_new_arrival), preteenContainer, 'fpro');
        if (teenContainer) renderProductList(products.filter(p => p.category === 'teen' && p.is_new_arrival), teenContainer, 'fp');
    }
}

function renderProductList(productList, container, proClass) {
    if (!container) return;
    container.innerHTML = '';
    productList.forEach(product => {
        container.innerHTML += createProductHtml(product, proClass);
    });
}

function createProductHtml(product, proClass) {
    const infoClass = (proClass === 'fpro') ? 'info' : 'des';
    const imagePath = `/static/${product.image_url}`;
    return `
        <div class="${proClass}" data-product-id="${product.id}">
            <img src="${imagePath}" alt="${product.name}">
            <div class="${infoClass}">
                <h5>${product.name}</h5>
                <div class="star">
                    <ion-icon name="star-sharp"></ion-icon><ion-icon name="star-sharp"></ion-icon>
                </div>
                <h4>£${product.price}</h4>
            </div>
            <a class="cart"><ion-icon name="cart-outline"></ion-icon></a>
        </div>
    `;
}

function displayErrorMessage() {
    const containers = document.querySelectorAll('.fprocontainer, .fpcontainer');
    containers.forEach(container => {
        if (container) {
            container.innerHTML = '<p style="text-align:center; color:red;">Oops! Could not load products.</p>';
        }
    });
}

// === EVENT LISTENERS + CSRF TOKEN ===================================================

function setupEventListeners() {
    document.body.addEventListener('click', function(event) {
        const addToCartBtn = event.target.closest('.cart');
        if (addToCartBtn) {
            const productElement = addToCartBtn.closest('[data-product-id]');
            if (productElement) {
                addToCart(productElement.dataset.productId);
            }
        }
        const removeFromCartBtn = event.target.closest('.remove-item');
        if (removeFromCartBtn) {
            removeFromCart(removeFromCartBtn.dataset.itemId);
        }
    });
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', validateCart);
    }
}

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

// === CART LOGIC ========================================================

async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ product_id: productId })
        });

        if (response.ok) {
            // Tells the cart icon to update itself
            await onLoadCartNumbers();
            alert('Item added to cart!');
        } else {
            throw new Error('Failed to add item to cart.');
        }
    } catch (error) {
        console.error(error);
        alert('Could not add item. Please try again.');
    }
}

async function removeFromCart(itemId) {
    try {
        const response = await fetch('/api/cart/remove/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ item_id: itemId })
        });

        if (response.ok) {
            // These lines force the page to update after a successful deletion 
            await displayCart(); // Re-renders the cart item list
            await onLoadCartNumbers(); // Re-fetches the total for the header icon
        } else {
            throw new Error('Failed to remove item.');
        }
    } catch (error) {
        console.error(error);
        alert('Could not remove item. Please try again.');
    }
}

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

function updateCartTotals(cartData) {
    const subtotal = parseFloat(cartData.grand_total || '0').toFixed(2);
    const charityAmount = (subtotal * 0.1).toFixed(2);
    
    const subtotalEl = document.getElementById("subtotal");
    const charityEl = document.getElementById("charity-amount");
    const totalEl = document.getElementById("cart-total");

    if (subtotalEl) subtotalEl.textContent = subtotal;
    if (charityEl) charityEl.textContent = charityAmount;
    if (totalEl) totalEl.textContent = subtotal;
}

async function validateCart(event) {
    event.preventDefault();
    try {
        const response = await fetch('/api/cart/');
        const cartData = await response.json();
        const charitySelect = document.getElementById('charity-select');
        
        if (!cartData.items || cartData.items.length === 0) {
            alert('Please add at least one item to your cart before proceeding!');
        } else if (charitySelect.value === "0") {
            alert('Please select a charity before proceeding!');
        } else {
            alert('Proceeding to checkout (Sprint 4)');
        }
    } catch (error) {
        console.error("Validation failed:", error);
    }
}