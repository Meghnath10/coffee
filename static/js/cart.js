// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the cart
    updateCartDisplay();
    
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', addToCart);
    });
    
    // Clear cart button
    const clearCartButton = document.querySelector('.clear-cart');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', clearCart);
    }
    
    // Quantity update buttons in cart
    const quantityInputs = document.querySelectorAll('.cart-quantity');
    if (quantityInputs) {
        quantityInputs.forEach(input => {
            input.addEventListener('change', updateCartItemQuantity);
        });
    }
    
    // Remove item buttons
    const removeButtons = document.querySelectorAll('.remove-item');
    if (removeButtons) {
        removeButtons.forEach(button => {
            button.addEventListener('click', removeCartItem);
        });
    }
});

// Add item to cart
function addToCart(event) {
    event.preventDefault();
    
    const button = event.target.closest('.add-to-cart');
    const productId = parseInt(button.dataset.id);
    const productName = button.dataset.name;
    const productPrice = parseFloat(button.dataset.price);
    const quantity = 1; // Default quantity
    
    // API call to add to cart
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: productId,
            name: productName,
            price: productPrice,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showToast(`${productName} added to cart!`);
            // Update cart display
            updateCartDisplay();
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        showToast('Error adding item to cart', 'error');
    });
}

// Update cart item quantity
function updateCartItemQuantity(event) {
    const input = event.target;
    const productId = parseInt(input.dataset.id);
    const quantity = parseInt(input.value);
    
    if (quantity < 1) {
        input.value = 1;
        return;
    }
    
    // API call to update cart
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartDisplay();
            updateCartTable();
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
        showToast('Error updating cart', 'error');
    });
}

// Remove item from cart
function removeCartItem(event) {
    event.preventDefault();
    
    const button = event.target.closest('.remove-item');
    const productId = parseInt(button.dataset.id);
    
    // API call to update cart (quantity = 0 removes item)
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: productId,
            quantity: 0
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartDisplay();
            updateCartTable();
        }
    })
    .catch(error => {
        console.error('Error removing item:', error);
        showToast('Error removing item', 'error');
    });
}

// Clear entire cart
function clearCart(event) {
    if (event) event.preventDefault();
    
    // Confirm before clearing
    if (!confirm('Are you sure you want to clear your cart?')) {
        return;
    }
    
    // API call to clear cart
    fetch('/api/cart/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartDisplay();
            updateCartTable();
            showToast('Cart cleared');
        }
    })
    .catch(error => {
        console.error('Error clearing cart:', error);
        showToast('Error clearing cart', 'error');
    });
}

// Update cart count in navbar and totals if on cart page
function updateCartDisplay() {
    fetch('/api/cart')
    .then(response => response.json())
    .then(data => {
        // Update cart count badge
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            const count = data.cart.reduce((total, item) => total + item.quantity, 0);
            cartCount.textContent = count;
            
            // Show/hide based on count
            if (count > 0) {
                cartCount.classList.remove('d-none');
            } else {
                cartCount.classList.add('d-none');
            }
        }
        
        // Update cart table if on cart page
        updateCartTable(data.cart);
    })
    .catch(error => {
        console.error('Error fetching cart:', error);
    });
}

// Update cart table if on cart page
function updateCartTable(cartData) {
    const cartTable = document.querySelector('.cart-table');
    const cartEmpty = document.querySelector('.cart-empty');
    const cartSummary = document.querySelector('.cart-summary');
    
    if (!cartTable) return; // Not on cart page
    
    // If we don't have cartData, fetch it
    if (!cartData) {
        fetch('/api/cart')
        .then(response => response.json())
        .then(data => {
            updateCartTable(data.cart);
        })
        .catch(error => {
            console.error('Error fetching cart data:', error);
        });
        return;
    }
    
    // Empty cart message
    if (!cartData.length) {
        cartTable.classList.add('d-none');
        cartSummary.classList.add('d-none');
        cartEmpty.classList.remove('d-none');
        return;
    }
    
    // Show cart table, hide empty message
    cartTable.classList.remove('d-none');
    cartSummary.classList.remove('d-none');
    cartEmpty.classList.add('d-none');
    
    // Update cart items
    const tableBody = cartTable.querySelector('tbody');
    tableBody.innerHTML = '';
    
    let subtotal = 0;
    
    cartData.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>
                <input type="number" min="1" value="${item.quantity}" 
                  class="form-control form-control-sm cart-quantity" 
                  style="width: 70px;" data-id="${item.id}">
            </td>
            <td>$${itemTotal.toFixed(2)}</td>
            <td>
                <button class="btn btn-sm btn-danger remove-item" data-id="${item.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Update quantity change event listeners
    const quantityInputs = document.querySelectorAll('.cart-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', updateCartItemQuantity);
    });
    
    // Update remove buttons
    const removeButtons = document.querySelectorAll('.remove-item');
    removeButtons.forEach(button => {
        button.addEventListener('click', removeCartItem);
    });
    
    // Update summary
    const subtotalElement = document.querySelector('.cart-subtotal');
    const taxElement = document.querySelector('.cart-tax');
    const totalElement = document.querySelector('.cart-total');
    
    const tax = subtotal * 0.1; // Assuming 10% tax
    const total = subtotal + tax;
    
    if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    if (taxElement) taxElement.textContent = `$${tax.toFixed(2)}`;
    if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
}

// Show toast message
function showToast(message, type = 'success') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = `toast-${Date.now()}`;
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'error' ? 'bg-danger text-white' : 'bg-success text-white'}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.setAttribute('id', toastId);
    
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${type === 'error' ? 'Error' : 'Success'}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const toastElement = new bootstrap.Toast(toast);
    toastElement.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
