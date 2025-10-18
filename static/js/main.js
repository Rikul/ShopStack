// ShopStack Dashboard JavaScript

$(document).ready(function() {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Add loading states to buttons
    $('.btn').click(function() {
        var $btn = $(this);
        if (!$btn.hasClass('no-loading')) {
            $btn.addClass('loading');
            setTimeout(function() {
                $btn.removeClass('loading');
            }, 2000);
        }
    });
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if( target.length ) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 1000);
        }
    });
    
    // Add active state to navigation
    var currentPath = window.location.pathname;
    $('.nav-link').each(function() {
        var href = $(this).attr('href');
        if (href && currentPath.includes(href.split('?')[0])) {
            $(this).closest('.nav-item').addClass('active');
        }
    });
    
    // Format numbers with commas
    $('.format-number').each(function() {
        var number = parseFloat($(this).text());
        if (!isNaN(number)) {
            $(this).text(number.toLocaleString());
        }
    });
    
    // Dashboard card hover effects
    $('.card').hover(
        function() {
            $(this).addClass('shadow-lg');
        },
        function() {
            $(this).removeClass('shadow-lg');
        }
    );
    
    // Confirmation dialogs for delete actions
    $('.btn-danger').click(function(e) {
        if ($(this).data('confirm')) {
            if (!confirm($(this).data('confirm'))) {
                e.preventDefault();
            }
        }
    });
    
    // Auto-refresh data every 5 minutes for dashboard
    if (window.location.pathname.includes('dashboard')) {
        setInterval(function() {
            // Only refresh if page is visible
            if (!document.hidden) {
                refreshDashboardData();
            }
        }, 300000); // 5 minutes
    }
    
    // Search functionality for tables
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $("#dataTable tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});

// Function to refresh dashboard data
function refreshDashboardData() {
    // This would typically make an AJAX call to refresh dashboard stats
    console.log('Refreshing dashboard data...');
    // You can implement actual AJAX calls here based on your needs
}

// Function to show notifications
function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var notification = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
    `;
    
    $('.container-fluid').prepend(notification);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').first().fadeOut('slow');
    }, 5000);
}

// Function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Function to format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Utility function to get CSRF token
function getCSRFToken() {
    return $('[name=csrfmiddlewaretoken]').val();
}