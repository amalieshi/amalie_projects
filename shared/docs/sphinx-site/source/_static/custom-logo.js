// Custom JavaScript to redirect logo clicks to main portfolio site
document.addEventListener('DOMContentLoaded', function() {
    // Find the logo link and override its href
    const logoLink = document.querySelector('.sidebar-brand, .navbar-brand, a[href="index.html"], a[href="./"], a[href="../"]');
    
    if (logoLink) {
        logoLink.href = 'https://amalieshi.github.io/';
        logoLink.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'https://amalieshi.github.io/';
        });
    }
    
    // Also try to find logo by looking for img elements with logo in the src
    const logoImages = document.querySelectorAll('img[src*="logo"], .sidebar-brand img, .navbar-brand img');
    logoImages.forEach(function(img) {
        const parentLink = img.closest('a');
        if (parentLink) {
            parentLink.href = 'https://amalieshi.github.io/';
            parentLink.addEventListener('click', function(e) {
                e.preventDefault();
                window.location.href = 'https://amalieshi.github.io/';
            });
        }
    });
});