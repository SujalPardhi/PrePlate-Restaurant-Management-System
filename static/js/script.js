// PrePlate - Restaurant Management System JavaScript

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavbar();
    initializeForms();
    initializeStatusUpdates();
    
    // Check if we need real-time updates
    if (window.location.pathname.includes('kitchen') || window.location.pathname.includes('dashboard')) {
        startRealTimeUpdates();
    }
});

// Real-time updates for kitchen and dashboard
let updateInterval;
let lastOrderCount = 0;

function startRealTimeUpdates() {
    // Poll every 5 seconds for new orders
    updateInterval = setInterval(function() {
        if (window.location.pathname.includes('kitchen/orders')) {
            updateKitchenOrders();
        } else if (window.location.pathname.includes('dashboard')) {
            updateDashboardStats();
        }
    }, 5000);
}

function stopRealTimeUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

function updateKitchenOrders() {
    fetch('/api/kitchen/orders')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching kitchen orders:', data.error);
                return;
            }
            
            const activeOrders = data.active_orders || [];
            const readyOrders = data.ready_orders || [];
            
            // Check if order count changed
            const currentOrderCount = activeOrders.length + readyOrders.length;
            if (currentOrderCount !== lastOrderCount) {
                // Orders changed, refresh the page or update DOM
                location.reload();
            }
            
            lastOrderCount = currentOrderCount;
        })
        .catch(error => console.error('Error fetching kitchen orders:', error));
}

function updateDashboardStats() {
    fetch('/api/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error fetching dashboard stats:', data.error);
                return;
            }
            
            // Update statistics on the page
            updateStatCards(data);
        })
        .catch(error => console.error('Error fetching dashboard stats:', error));
}

function updateStatCards(data) {
    // Update today's orders
    const todayOrdersEl = document.querySelector('[data-stat="today_orders"]');
    if (todayOrdersEl && data.today_orders !== undefined) {
        todayOrdersEl.textContent = data.today_orders;
    }
    
    // Update pending orders
    const pendingOrdersEl = document.querySelector('[data-stat="pending_orders"]');
    if (pendingOrdersEl && data.pending_orders !== undefined) {
        pendingOrdersEl.textContent = data.pending_orders;
    }
    
    // Update preparing orders
    const preparingOrdersEl = document.querySelector('[data-stat="preparing_orders"]');
    if (preparingOrdersEl && data.preparing_orders !== undefined) {
        preparingOrdersEl.textContent = data.preparing_orders;
    }
    
    // Update ready orders
    const readyOrdersEl = document.querySelector('[data-stat="ready_orders"]');
    if (readyOrdersEl && data.ready_orders !== undefined) {
        readyOrdersEl.textContent = data.ready_orders;
    }
    
    // Update completed orders
    const completedOrdersEl = document.querySelector('[data-stat="completed_orders"]');
    if (completedOrdersEl && data.completed_orders !== undefined) {
        completedOrdersEl.textContent = data.completed_orders;
    }
    
    // Update today's sales
    const todaySalesEl = document.querySelector('[data-stat="today_sales"]');
    if (todaySalesEl && data.today_sales !== undefined) {
        todaySalesEl.textContent = '₹' + data.today_sales.toFixed(2);
    }
    
    // Update total stock
    const totalStockEl = document.querySelector('[data-stat="total_stock"]');
    if (totalStockEl && data.total_stock !== undefined) {
        totalStockEl.textContent = data.total_stock;
    }
}

// Navbar functionality
function initializeNavbar() {
    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            if (!navbarCollapse.contains(event.target) && !navbarToggler.contains(event.target)) {
                navbarCollapse.classList.remove('show');
            }
        }
    });
}

// Form validation and enhancements
function initializeForms() {
    // Add form validation styles
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                form.classList.add('was-validated');
            }
        });
    });
}

// Status update functionality
function initializeStatusUpdates() {
    const statusSelects = document.querySelectorAll('select[name="status"]');
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const form = select.closest('form');
            if (form) {
                // Auto-submit on status change for smoother UX
                form.submit();
            }
        });
    });
}

// Helper function to format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Helper function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Helper function to format time
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const formattedHour = hour % 12 || 12;
    return `${formattedHour}:${minutes} ${ampm}`;
}

// Loading indicator
function showLoading(element) {
    element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// Toast notification helper
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">PrePlate</strong>
                <small>Just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    const toastContainer = document.querySelector('.toast-container');
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Confirm delete action
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Image preview for file uploads
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Quantity selector helper
function updateQuantity(input, change) {
    let currentValue = parseInt(input.value) || 0;
    let newValue = currentValue + change;
    
    if (newValue >= input.min && newValue <= input.max) {
        input.value = newValue;
    }
}

// Auto-resize textarea
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Initialize auto-resize for all textareas
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        autoResizeTextarea(this);
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        showToast('Failed to copy to clipboard', 'danger');
    });
}

// Print function for orders
function printOrder(orderId) {
    const printContent = document.getElementById(`order-${orderId}`);
    if (printContent) {
        const originalContents = document.body.innerHTML;
        document.body.innerHTML = printContent.innerHTML;
        window.print();
        document.body.innerHTML = originalContents;
        location.reload();
    }
}

// Refresh page functionality
function refreshPage() {
    location.reload();
}

// Stop real-time updates when leaving the page
window.addEventListener('beforeunload', function() {
    stopRealTimeUpdates();
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/dropdowns
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Console welcome message
console.log('%cPrePlate - Restaurant Management System', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with Flask, Bootstrap 5, and MySQL', 'color: #6c757d; font-size: 12px;');
