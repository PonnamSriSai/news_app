// PSLVNews JavaScript Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeHeaderEffects();
    initializeMobileMenu();
    initializeModals();
    initializeForms();
    initializeCarousel();
    initializeDashboard();
});

// Header scroll effects
function initializeHeaderEffects() {
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
}

// Mobile menu toggle
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
        mobileMenu.classList.toggle('show');
    }
}

// Modal functionality
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function switchToRegister() {
    closeModal('login-modal');
    showModal('register-modal');
}

function switchToLogin() {
    closeModal('register-modal');
    showModal('login-modal');
}

function showLoginPage() {
    showModal('login-modal');
}

function showRegisterPage() {
    showModal('register-modal');
}

// Initialize modals
function initializeModals() {
    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal(e.target.id);
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal-overlay[style*="flex"]');
            if (activeModal) {
                closeModal(activeModal.id);
            }
        }
    });
}

// Form handling and validation
function initializeForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Password visibility toggle
    initializePasswordToggles();
}


// function handleLogin(e) {
//     e.preventDefault();
//     const formData = new FormData(e.target);
//     const email = formData.get('email');
//     const password = formData.get('password');

//     // Basic validation
//     if (!email || !password) {
//         showError('login-form', 'Please fill in all fields');
//         return;
//     }

//     if (!isValidEmail(email)) {
//         showError('login-form', 'Please enter a valid email address');
//         return;
//     }

//     // Simulate login process
//     showSuccess('login-form', 'Login successful! Redirecting...');
    
//     setTimeout(() => {
//         closeModal('login-modal');
//         // In a real app, redirect to dashboard
//         console.log('User logged in:', email);
//     }, 1500);
// }

// function handleRegister(e) {
//     e.preventDefault();
//     const formData = new FormData(e.target);
//     const firstName = formData.get('first_name');
//     const lastName = formData.get('last_name');
//     const email = formData.get('email');
//     const password = formData.get('password');
//     const confirmPassword = formData.get('confirm_password');
//     const age = formData.get('age');
//     const location = formData.get('location');
//     const role = formData.get('role');

//     // Validation
//     if (!firstName || !lastName || !email || !password || !confirmPassword || !age || !location || !role) {
//         showError('register-form', 'Please fill in all fields');
//         return;
//     }

//     if (!isValidEmail(email)) {
//         showError('register-form', 'Please enter a valid email address');
//         return;
//     }

//     if (password !== confirmPassword) {
//         showError('register-form', 'Passwords do not match');
//         return;
//     }

//     if (parseInt(age) < 13 || parseInt(age) > 120) {
//         showError('register-form', 'Please enter a valid age (13-120)');
//         return;
//     }

//     // Simulate registration process
//     showSuccess('register-form', 'Registration successful! Redirecting...');
    
//     setTimeout(() => {
//         closeModal('register-modal');
//         // In a real app, redirect to dashboard or login
//         console.log('User registered:', { firstName, lastName, email, role });
//     }, 1500);
// }

function showError(formId, message) {
    const form = document.getElementById(formId);
    let errorDiv = form.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        form.insertBefore(errorDiv, form.firstChild);
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide error after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showSuccess(formId, message) {
    const form = document.getElementById(formId);
    let successDiv = form.querySelector('.success-message');
    
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.style.cssText = `
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            color: #4ADE80;
            padding: 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            margin-bottom: 1rem;
        `;
        form.insertBefore(successDiv, form.firstChild);
    }
    
    successDiv.textContent = message;
    successDiv.style.display = 'block';
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function initializePasswordToggles() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        const container = input.parentElement;
        if (!container.classList.contains('password-input-container')) {
            container.classList.add('password-input-container');
        }
        
        let toggleBtn = container.querySelector('.password-toggle');
        if (!toggleBtn) {
            toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'password-toggle';
            toggleBtn.innerHTML = `
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
            `;
            container.appendChild(toggleBtn);
        }
        
        toggleBtn.addEventListener('click', function() {
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Toggle icon
            if (type === 'text') {
                toggleBtn.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                    </svg>
                `;
            } else {
                toggleBtn.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                    </svg>
                `;
            }
        });
    });
}

// Phone carousel functionality
function initializeCarousel() {
    const carousel = document.querySelector('.phone-carousel');
    if (carousel) {
        // Auto-advance slides
        let currentSlide = 0;
        const slides = carousel.querySelectorAll('.phone-slide');
        const totalSlides = slides.length;
        
        setInterval(() => {
            currentSlide = (currentSlide + 1) % totalSlides;
            const transform = `translateX(-${currentSlide * 100}%)`;
            const phoneSlides = carousel.querySelector('.phone-slides');
            if (phoneSlides) {
                phoneSlides.style.transform = transform;
            }
        }, 3000);
    }
}

// Utility functions for navigation
function navigateToPage(page) {
    // In a real app, this would handle proper navigation
    console.log('Navigating to:', page);
    
    switch(page) {
        case 'login':
            showLoginPage();
            break;
        case 'register':
            showRegisterPage();
            break;
        case 'dashboard':
            // Redirect to dashboard route
            window.location.href = '/user/dashboard';
            break;
        default:
            console.log('Unknown page:', page);
    }
}

// Add smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Add loading states for buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    
    setTimeout(() => {
        button.textContent = originalText;
        button.disabled = false;
    }, 2000);
}

// Dashboard specific functionality
function initializeDashboard() {
    // Only initialize dashboard functionality if we're on the dashboard page
    if (document.querySelector('.dashboard-page')) {
        initializeDashboardMobileMenu();
        initializeSidebarNavigation();
        initializeCategoriesCollapse();
        initializeNewsNavigation();
        initializeSearchFunctionality();
        initializeChatbot();
        initializeNewsInteractions();
    }
}

// Dashboard mobile menu toggle
function initializeDashboardMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
        });
    }
}

// Sidebar navigation with active state
function initializeSidebarNavigation() {
    const sidebarLinks = document.querySelectorAll('.sidebar-nav-button');
    const currentPath = window.location.pathname;
    
    sidebarLinks.forEach(link => {
        // Add active class to current page link
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
        
        link.addEventListener('click', function() {
            // Remove active class from all links
            sidebarLinks.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get the category name from href or text
            const href = this.getAttribute('href');
            const category = href ? href.split('/').pop() : this.textContent.trim();
            console.log('Navigating to category:', category);
            
            // Navigation will be handled by the link itself
        });
    });
}

// Categories collapse functionality
function initializeCategoriesCollapse() {
    const sidebarButton = document.querySelector('.sidebar-button');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarButton && sidebar) {
        sidebarButton.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            
            // Update button icon and text for better UX
            const icon = this.querySelector('.sidebar-icon');
            const text = this.querySelector('span') || this.childNodes[this.childNodes.length - 1];
            
            if (sidebar.classList.contains('collapsed')) {
                // Show expand icon when collapsed
                if (icon) {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>';
                }
            } else {
                // Show collapse icon when expanded
                if (icon) {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"></path>';
                }
            }
        });
    }
}

// News navigation (previous/next)
function initializeNewsNavigation() {
    // This function is now handled by the navigateNews function that's called directly from HTML
    console.log('News navigation initialized');
}

// Global variables for news navigation
let currentNewsIndex = 0;
let totalNewsCount = 0;

// Initialize news navigation when page loads
document.addEventListener('DOMContentLoaded', function() {
    updateNewsCount();
});

// Function to update news count
function updateNewsCount() {
    const newsArticles = document.querySelectorAll('.news-article');
    totalNewsCount = newsArticles.length;
    console.log(`Total news articles: ${totalNewsCount}`);
}

// Navigate between news articles
function navigateNews(direction) {
    const newsArticles = document.querySelectorAll('.news-article');
    
    if (newsArticles.length === 0) {
        console.log('No news articles found');
        return;
    }
    
    // Hide current article
    newsArticles[currentNewsIndex].style.display = 'none';
    
    // Calculate new index
    if (direction === 'prev') {
        currentNewsIndex = (currentNewsIndex - 1 + totalNewsCount) % totalNewsCount;
    } else if (direction === 'next') {
        currentNewsIndex = (currentNewsIndex + 1) % totalNewsCount;
    }
    
    // Show new article with animation
    const newArticle = newsArticles[currentNewsIndex];
    newArticle.style.display = 'block';
    newArticle.style.opacity = '0';
    newArticle.style.transform = 'translateX(20px)';
    
    // Animate in
    setTimeout(() => {
        newArticle.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        newArticle.style.opacity = '1';
        newArticle.style.transform = 'translateX(0)';
    }, 50);
    
    console.log(`Navigated to news article ${currentNewsIndex + 1} of ${totalNewsCount}`);
    
    // Update navigation button states
    updateNavigationButtons();
}

// Update navigation button states
function updateNavigationButtons() {
    const prevButton = document.querySelector('.news-navigation.prev');
    const nextButton = document.querySelector('.news-navigation.next');
    
    if (prevButton && nextButton) {
        // Add visual feedback for button states
        if (totalNewsCount <= 1) {
            prevButton.style.opacity = '0.5';
            nextButton.style.opacity = '0.5';
            prevButton.disabled = true;
            nextButton.disabled = true;
        } else {
            prevButton.style.opacity = '1';
            nextButton.style.opacity = '1';
            prevButton.disabled = false;
            nextButton.disabled = false;
        }
    }
}

// Search functionality with tags and Flask integration
let searchTags = [];

function initializeSearchFunctionality() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (searchForm && searchInput) {
        // Handle form submission
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            
            if (!query) {
                e.preventDefault();
                showSearchError('Please enter a search term');
                return;
            }
            
            // Add loading state
            const submitButton = this.querySelector('button[type="submit"]') || searchInput;
            const originalText = submitButton.textContent;
            submitButton.innerHTML = '<svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Searching...';
            submitButton.disabled = true;
            
            console.log('Search submitted:', query);
        });
        
        // Handle Enter key in search input
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = this.value.trim();
                
                if (query) {
                    // Add search tag for UI feedback
                    addSearchTag(query);
                    
                    // Submit the form
                    searchForm.submit();
                } else {
                    showSearchError('Please enter a search term');
                }
            }
        });
        
        // Clear search when clicking on search icon
        const searchIcon = searchForm.querySelector('.search-icon');
        if (searchIcon) {
            searchIcon.addEventListener('click', function() {
                const currentQuery = searchInput.value.trim();
                if (currentQuery) {
                    searchInput.value = '';
                    searchTags = [];
                    renderSearchTags();
                    
                    // If we're on search results page, go back to dashboard
                    if (window.location.pathname.includes('/search')) {
                        window.location.href = '/user/dashboard/breakingnews';
                    }
                }
            });
        }
    }
}

// Add search tag
function addSearchTag(query) {
    // Don't add duplicate tags
    if (searchTags.includes(query)) {
        return;
    }
    
    searchTags.push(query);
    renderSearchTags();
}

// Remove search tag
function removeSearchTag(query) {
    const index = searchTags.indexOf(query);
    if (index > -1) {
        searchTags.splice(index, 1);
        renderSearchTags();
    }
}

// Render search tags
function renderSearchTags() {
    const container = document.querySelector('.search-tags-container');
    if (!container) return;
    
    container.innerHTML = '';
    
    searchTags.forEach(tag => {
        const tagElement = document.createElement('div');
        tagElement.className = 'search-tag';
        tagElement.innerHTML = `
            <span class="search-tag-text">${tag}</span>
            <button class="search-tag-remove" onclick="removeSearchTag('${tag}')">×</button>
        `;
        container.appendChild(tagElement);
    });
    
    console.log('Current search tags:', searchTags);
}

// Chatbot functionality
function initializeChatbot() {
    const chatbotButton = document.querySelector('.chatbot-button');
    
    if (chatbotButton) {
        chatbotButton.addEventListener('click', function() {
            console.log('Chatbot opened');
            // In a real app, this would open a chat interface
            alert('Chatbot feature coming soon!');
        });
    }
}

// News interaction buttons
function initializeNewsInteractions() {
    console.log('News interactions initialized');
}

// Like a news article
function likeNews(newsId) {
    console.log('Liking news article:', newsId);
    
    const newsArticle = document.querySelector(`[data-news-id="${newsId}"]`);
    if (!newsArticle) {
        console.log('News article not found');
        return;
    }
    
    const likeButton = newsArticle.querySelector('.action-button');
    const likeCountSpan = likeButton.querySelector('.like-count');
    
    if (likeCountSpan) {
        let currentCount = parseInt(likeCountSpan.textContent) || 0;
        currentCount++;
        likeCountSpan.textContent = currentCount;
        
        // Add visual feedback
        likeButton.style.transform = 'scale(1.1)';
        likeButton.style.color = '#ef4444';
        
        setTimeout(() => {
            likeButton.style.transform = 'scale(1)';
            likeButton.style.color = '';
        }, 200);
        
        console.log(`Liked article ${newsId}. New count: ${currentCount}`);
        
        // In a real app, you would make an API call here:
        // fetch('/api/like-news', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({newsId: newsId})
        // });
    }
}

// Save a news article
function saveNews(newsId) {
    console.log('Saving news article:', newsId);
    
    const newsArticle = document.querySelector(`[data-news-id="${newsId}"]`);
    if (!newsArticle) {
        console.log('News article not found');
        return;
    }
    
    const saveButton = newsArticle.querySelector('.action-button:nth-child(2)');
    
    if (saveButton) {
        // Toggle save state
        const isSaved = saveButton.classList.contains('saved');
        
        if (isSaved) {
            saveButton.classList.remove('saved');
            saveButton.style.color = '';
            console.log(`Un-saved article ${newsId}`);
        } else {
            saveButton.classList.add('saved');
            saveButton.style.color = '#3b82f6';
            
            // Add visual feedback
            saveButton.style.transform = 'scale(1.1)';
            setTimeout(() => {
                saveButton.style.transform = 'scale(1)';
            }, 200);
            
            console.log(`Saved article ${newsId}`);
        }
        
        // In a real app, you would make an API call here:
        // fetch('/api/save-news', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({newsId: newsId, action: isSaved ? 'unsave' : 'save'})
        // });
    }
}

// Share a news article
function shareNews(newsId) {
    console.log('Sharing news article:', newsId);
    
    const newsArticle = document.querySelector(`[data-news-id="${newsId}"]`);
    if (!newsArticle) {
        console.log('News article not found');
        return;
    }
    
    const shareButton = newsArticle.querySelector('.action-button:nth-child(3)');
    
    if (shareButton) {
        // Add visual feedback
        shareButton.style.transform = 'scale(1.1)';
        shareButton.style.color = '#10b981';
        
        setTimeout(() => {
            shareButton.style.transform = 'scale(1)';
            shareButton.style.color = '';
        }, 200);
        
        // In a real app, you would open a share dialog or copy link
        if (navigator.share) {
            navigator.share({
                title: 'Check out this news article',
                url: window.location.href
            }).catch(console.error);
        } else {
            // Fallback: copy URL to clipboard
            navigator.clipboard.writeText(window.location.href).then(() => {
                console.log('Link copied to clipboard');
                // You could show a toast notification here
            }).catch(err => {
                console.error('Failed to copy link:', err);
            });
        }
        
        console.log(`Shared article ${newsId}`);
        
        // In a real app, you would make an API call here:
        // fetch('/api/share-news', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({newsId: newsId})
        // });
    }
}

// Navigate to specific news article by index
function navigateToNews(index) {
    const newsArticles = document.querySelectorAll('.news-article');
    
    if (newsArticles.length === 0) {
        console.log('No news articles found');
        return;
    }
    
    // Validate index
    if (index < 0 || index >= newsArticles.length) {
        console.log(`Invalid news index: ${index}`);
        return;
    }
    
    // Hide current article
    newsArticles[currentNewsIndex].style.display = 'none';
    
    // Update current index
    currentNewsIndex = index;
    
    // Show target article with animation
    const targetArticle = newsArticles[currentNewsIndex];
    targetArticle.style.display = 'block';
    targetArticle.style.opacity = '0';
    targetArticle.style.transform = 'translateX(20px)';
    
    // Animate in
    setTimeout(() => {
        targetArticle.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        targetArticle.style.opacity = '1';
        targetArticle.style.transform = 'translateX(0)';
    }, 50);
    
    console.log(`Navigated to news article ${currentNewsIndex + 1} of ${totalNewsCount}`);
    
    // Update navigation button states
    updateNavigationButtons();
}

// Breaking news items click handler (enhanced)
document.addEventListener('DOMContentLoaded', function() {
    const breakingNewsItems = document.querySelectorAll('.breaking-news-item');
    
    breakingNewsItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            const newsText = this.querySelector('.breaking-news-text').textContent;
            console.log(`Breaking news ${index} clicked:`, newsText);
            
            // Add visual feedback
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            // Navigate to the corresponding article
            navigateToNews(index);
        });
    });
});

// Show search error function
function showSearchError(message) {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    
    if (searchInput) {
        searchInput.classList.add('error');
        searchInput.style.borderColor = '#ef4444';
        
        // Create or update error message
        let errorDiv = searchForm.querySelector('.search-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'search-error';
            errorDiv.style.cssText = `
                color: #ef4444;
                font-size: 0.875rem;
                margin-top: 0.5rem;
                padding: 0.5rem;
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: 0.375rem;
                display: none;
            `;
            searchForm.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Remove error styling after 3 seconds
        setTimeout(() => {
            searchInput.classList.remove('error');
            searchInput.style.borderColor = '';
            if (errorDiv) {
                errorDiv.style.display = 'none';
            }
        }, 3000);
    }
}

// ==================== Toast Notification System ====================
class ToastManager {
    constructor() {
        this.container = null;
        this.toasts = [];
        this.init();
    }

    init() {
        // Create toast container if it doesn't exist
        this.container = document.querySelector('.toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'info', options = {}) {
        const {
            title = '',
            duration = 5000,
            closable = true,
            progress = true,
            position = 'top-right'
        } = options;

        const toast = this.createToast(message, type, title, closable, progress);
        this.container.appendChild(toast);
        this.toasts.push(toast);

        // Animate in
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }

        return toast;
    }

    createToast(message, type, title, closable, progress) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = this.getIcon(type);
        
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            ${closable ? '<button class="toast-close" onclick="toastManager.remove(this.parentElement)">×</button>' : ''}
            ${progress ? '<div class="toast-progress"></div>' : ''}
        `;

        // Add event listeners
        if (closable) {
            toast.querySelector('.toast-close').addEventListener('click', () => {
                this.remove(toast);
            });
        }

        return toast;
    }

    getIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'i'
        };
        return icons[type] || icons.info;
    }

    remove(toast) {
        toast.classList.add('hide');
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            
            const index = this.toasts.indexOf(toast);
            if (index > -1) {
                this.toasts.splice(index, 1);
            }
        }, 300);
    }

    clear() {
        this.toasts.forEach(toast => {
            this.remove(toast);
        });
    }

    // Convenience methods
    success(message, title, options) {
        return this.show(message, 'success', { title, ...options });
    }

    error(message, title, options) {
        return this.show(message, 'error', { title, duration: 7000, ...options });
    }

    warning(message, title, options) {
        return this.show(message, 'warning', { title, ...options });
    }

    info(message, title, options) {
        return this.show(message, 'info', { title, ...options });
    }
}

// Initialize toast manager
const toastManager = new ToastManager();

// ==================== Enhanced Loading States ====================
class LoadingManager {
    static show(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (!element) return;

        element.classList.add('loading');
        
        // Add loading spinner for buttons
        if (element.tagName === 'BUTTON' || element.classList.contains('btn')) {
            element.classList.add('btn-loading');
        }
        
        // Store original text
        if (element.tagName === 'BUTTON' || element.classList.contains('btn')) {
            element.dataset.originalText = element.textContent;
            element.textContent = '';
        }
    }

    static hide(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (!element) return;

        element.classList.remove('loading');
        
        if (element.tagName === 'BUTTON' || element.classList.contains('btn')) {
            element.classList.remove('btn-loading');
            if (element.dataset.originalText) {
                element.textContent = element.dataset.originalText;
                delete element.dataset.originalText;
            }
        }
    }

    static toggle(element, isLoading, text = 'Loading...') {
        if (isLoading) {
            this.show(element, text);
        } else {
            this.hide(element);
        }
    }
}

// ==================== Enhanced Form Validation ====================
class FormValidator {
    constructor(form) {
        this.form = typeof form === 'string' ? document.querySelector(form) : form;
        this.rules = {};
        this.init();
    }

    init() {
        if (!this.form) return;

        // Add event listeners for real-time validation
        this.form.addEventListener('input', (e) => {
            this.validateField(e.target);
        });

        this.form.addEventListener('blur', (e) => {
            if (e.target.matches('input, select, textarea')) {
                this.validateField(e.target);
            }
        }, true);

        this.form.addEventListener('submit', (e) => {
            if (!this.validate()) {
                e.preventDefault();
            }
        });
    }

    addRule(fieldName, rule, message) {
        if (!this.rules[fieldName]) {
            this.rules[fieldName] = [];
        }
        this.rules[fieldName].push({ rule, message });
        return this;
    }

    validate() {
        let isValid = true;
        
        for (const [fieldName, rules] of Object.entries(this.rules)) {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                for (const { rule, message } of rules) {
                    if (!rule(field.value)) {
                        this.showError(field, message);
                        isValid = false;
                        break;
                    } else {
                        this.clearError(field);
                    }
                }
            }
        }
        
        return isValid;
    }

    validateField(field) {
        const fieldName = field.name;
        if (this.rules[fieldName]) {
            for (const { rule, message } of this.rules[fieldName]) {
                if (!rule(field.value)) {
                    this.showError(field, message);
                    return false;
                } else {
                    this.clearError(field);
                }
            }
        }
        return true;
    }

    showError(field, message) {
        field.classList.add('error');
        field.classList.remove('success');
        
        let errorDiv = field.parentNode.querySelector('.form-error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'form-error-message';
            field.parentNode.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
    }

    clearError(field) {
        field.classList.remove('error');
        field.classList.add('success');
        
        const errorDiv = field.parentNode.querySelector('.form-error-message');
        if (errorDiv) {
            errorDiv.classList.remove('show');
        }
    }

    static email(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    static required(value) {
        return value.trim().length > 0;
    }

    static minLength(value, min) {
        return value.length >= min;
    }

    static maxLength(value, max) {
        return value.length <= max;
    }

    static password(value) {
        return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/.test(value);
    }
}

// ==================== Enhanced Mobile Interactions ====================
class MobileEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.setupTouchTargets();
        this.setupSwipeGestures();
        this.setupMobileOptimizations();
    }

    setupTouchTargets() {
        // Ensure all interactive elements have minimum 44px touch targets
        const elements = document.querySelectorAll('button, .btn, .action-button, .sidebar-nav-button');
        
        elements.forEach(element => {
            const style = getComputedStyle(element);
            const minHeight = parseInt(style.minHeight) || 0;
            const minWidth = parseInt(style.minWidth) || 0;
            
            if (minHeight < 44 || minWidth < 44) {
                element.style.minHeight = '44px';
                element.style.minWidth = '44px';
            }
        });
    }

    setupSwipeGestures() {
        let startX = 0;
        let startY = 0;
        let startTime = 0;

        document.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            startX = touch.clientX;
            startY = touch.clientY;
            startTime = Date.now();
        });

        document.addEventListener('touchend', (e) => {
            if (!startTime) return;

            const touch = e.changedTouches[0];
            const endX = touch.clientX;
            const endY = touch.clientY;
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const deltaTime = Date.now() - startTime;

            // Check if it's a swipe gesture
            if (deltaTime < 300 && Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY)) {
                const direction = deltaX > 0 ? 'right' : 'left';
                this.handleSwipe(direction, e.target);
            }

            startX = startY = startTime = 0;
        });
    }

    handleSwipe(direction, target) {
        // Check if we're swiping on news cards for navigation
        const newsCard = target.closest('.news-card');
        if (newsCard) {
            if (direction === 'left') {
                // Swipe left - next news
                const nextBtn = newsCard.querySelector('.news-navigation.next');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.click();
                }
            } else if (direction === 'right') {
                // Swipe right - previous news
                const prevBtn = newsCard.querySelector('.news-navigation.prev');
                if (prevBtn && !prevBtn.disabled) {
                    prevBtn.click();
                }
            }
        }
    }

    setupMobileOptimizations() {
        // Improve mobile scrolling
        document.addEventListener('touchmove', (e) => {
            // Prevent bounce effect on iOS for better UX
            if (e.target.closest('.sidebar')) {
                e.stopPropagation();
            }
        }, { passive: true });

        // Better mobile modal handling
        this.setupMobileModals();
    }

    setupMobileModals() {
        const modals = document.querySelectorAll('.modal-overlay');
        
        modals.forEach(modal => {
            modal.addEventListener('touchmove', (e) => {
                // Prevent background scrolling when modal is open
                if (e.target === modal) {
                    e.preventDefault();
                }
            });
        });
    }
}

// ==================== Enhanced Accessibility ====================
class AccessibilityEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.addKeyboardNavigation();
        this.addFocusManagement();
        this.addAriaLabels();
        this.addScreenReaderSupport();
    }

    addKeyboardNavigation() {
        // Add keyboard navigation for custom components
        document.addEventListener('keydown', (e) => {
            // Escape key to close modals
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal-overlay.show');
                if (activeModal) {
                    const closeBtn = activeModal.querySelector('.modal-close, .btn-close');
                    if (closeBtn) {
                        closeBtn.click();
                    }
                }
            }

            // Enter key to activate focused elements
            if (e.key === 'Enter') {
                const focused = document.activeElement;
                if (focused && focused.matches('.action-button, .sidebar-nav-button')) {
                    focused.click();
                }
            }
        });
    }

    addFocusManagement() {
        // Improve focus indicators
        const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        
        document.addEventListener('focus', (e) => {
            if (e.target.matches(focusableElements)) {
                e.target.classList.add('focused');
            }
        }, true);

        document.addEventListener('blur', (e) => {
            if (e.target.matches(focusableElements)) {
                e.target.classList.remove('focused');
            }
        }, true);
    }

    addAriaLabels() {
        // Add ARIA labels to buttons without text
        const buttons = document.querySelectorAll('button:not([aria-label]):not([title])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                // Try to infer purpose from classes or context
                const classes = button.className;
                if (classes.includes('like')) {
                    button.setAttribute('aria-label', 'Like this article');
                } else if (classes.includes('save')) {
                    button.setAttribute('aria-label', 'Save this article');
                } else if (classes.includes('share')) {
                    button.setAttribute('aria-label', 'Share this article');
                } else if (classes.includes('navigation')) {
                    button.setAttribute('aria-label', 'Navigate to next article');
                }
            }
        });
    }

    addScreenReaderSupport() {
        // Add live regions for dynamic content updates
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
        document.body.appendChild(liveRegion);

        // Function to announce updates to screen readers
        window.announceToScreenReader = (message) => {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        };
    }
}

// ==================== Enhanced Performance ====================
class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.setupLazyLoading();
        this.setupImageOptimization();
        this.setupResourceHints();
    }

    setupLazyLoading() {
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                            observer.unobserve(img);
                        }
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    setupImageOptimization() {
        // Add loading="lazy" to images
        document.querySelectorAll('img').forEach(img => {
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }
        });
    }

    setupResourceHints() {
        // Add resource hints for better performance
        const head = document.head;
        
        // DNS prefetch for external resources
        const dnsPrefetch = document.createElement('link');
        dnsPrefetch.rel = 'dns-prefetch';
        dnsPrefetch.href = '//fonts.googleapis.com';
        head.appendChild(dnsPrefetch);

        // Preconnect for fonts
        const preconnect = document.createElement('link');
        preconnect.rel = 'preconnect';
        preconnect.href = 'https://fonts.gstatic.com';
        preconnect.crossOrigin = '';
        head.appendChild(preconnect);
    }
}

// ==================== Enhanced Error Handling ====================
class ErrorHandler {
    constructor() {
        this.init();
    }

    init() {
        this.setupGlobalErrorHandling();
        this.setupNetworkErrorHandling();
    }

    setupGlobalErrorHandling() {
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            this.showUserFriendlyError('Something went wrong. Please try again.');
        });

        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
            this.showUserFriendlyError('Network error. Please check your connection.');
        });
    }

    setupNetworkErrorHandling() {
        // Monitor fetch requests for network errors
        const originalFetch = window.fetch;
        window.fetch = (...args) => {
            return originalFetch(...args).catch(error => {
                console.error('Fetch error:', error);
                this.showUserFriendlyError('Network error. Please try again.');
                throw error;
            });
        };
    }

    showUserFriendlyError(message) {
        toastManager.error(message, 'Error');
    }

    showNetworkError() {
        toastManager.error('Network error. Please check your connection and try again.', 'Connection Error');
    }

    showValidationError(message) {
        toastManager.warning(message, 'Validation Error');
    }
}

// ==================== Initialize All Enhancements ====================
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all enhancement classes
    new MobileEnhancer();
    new AccessibilityEnhancer();
    new PerformanceOptimizer();
    new ErrorHandler();

    // Enhanced form validation setup
    setupEnhancedFormValidation();
    
    // Enhanced loading states for forms
    setupEnhancedFormLoading();
    
    // Enhanced mobile interactions
    setupEnhancedMobileInteractions();
    
    // Show welcome message for new features
    setTimeout(() => {
        if (localStorage.getItem('pslvnews_welcome') !== 'true') {
            toastManager.success(
                'Welcome to PSLVNews! Enjoy our enhanced user experience with better loading states, notifications, and mobile optimization.',
                'Welcome!'
            );
            localStorage.setItem('pslvnews_welcome', 'true');
        }
    }, 1000);
});

// ==================== Enhanced Form Validation Setup ====================
function setupEnhancedFormValidation() {
    // Login form validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        const validator = new FormValidator(loginForm);
        validator
            .addRule('email', FormValidator.email, 'Please enter a valid email address')
            .addRule('password', FormValidator.required, 'Password is required');
    }

    // Registration form validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        const validator = new FormValidator(registerForm);
        validator
            .addRule('first_name', FormValidator.required, 'First name is required')
            .addRule('last_name', FormValidator.required, 'Last name is required')
            .addRule('email', FormValidator.email, 'Please enter a valid email address')
            .addRule('password', FormValidator.password, 'Password must be at least 8 characters with uppercase, lowercase, and number')
            .addRule('age', (value) => parseInt(value) >= 13 && parseInt(value) <= 120, 'Age must be between 13 and 120')
            .addRule('location', FormValidator.required, 'Location is required')
            .addRule('role', FormValidator.required, 'Please select a role');
    }
}

// ==================== Enhanced Form Loading ====================
function setupEnhancedFormLoading() {
    // Enhanced form submission with loading states
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                LoadingManager.show(submitBtn, 'Processing...');
                
                // Reset loading state after form processing
                setTimeout(() => {
                    LoadingManager.hide(submitBtn);
                }, 3000);
            }
        });
    });
}

// ==================== Enhanced Mobile Interactions ====================
function setupEnhancedMobileInteractions() {
    // Enhanced mobile menu interactions
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
            
            // Announce to screen readers
            const isOpen = mobileMenu.classList.contains('show');
            window.announceToScreenReader(isOpen ? 'Mobile menu opened' : 'Mobile menu closed');
        });
    }

    // Enhanced sidebar for mobile
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (sidebar && menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
            
            // Close sidebar when clicking outside on mobile
            if (window.innerWidth <= 1024) {
                document.addEventListener('click', closeSidebarOnOutsideClick);
            }
        });
    }

    function closeSidebarOnOutsideClick(e) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('mobile-open');
            document.removeEventListener('click', closeSidebarOnOutsideClick);
        }
    }
}

// ==================== Enhanced API Integration ====================
class APIManager {
    constructor() {
        this.baseURL = window.location.origin;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    async get(endpoint, options = {}) {
        return this.request(endpoint, { method: 'GET', ...options });
    }

    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            ...options
        });
    }

    async put(endpoint, data, options = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
            ...options
        });
    }

    async delete(endpoint, options = {}) {
        return this.request(endpoint, { method: 'DELETE', ...options });
    }
}

// Global API manager instance
const apiManager = new APIManager();

// ==================== Enhanced Search with API Integration ====================
class EnhancedSearch {
    constructor() {
        this.init();
    }

    init() {
        this.setupSearchAPI();
        this.setupSearchSuggestions();
        this.setupSearchHistory();
    }

    setupSearchAPI() {
        const searchForm = document.querySelector('.search-form');
        const searchInput = document.querySelector('.search-input');
        
        if (searchForm && searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performLiveSearch(e.target.value);
                }, 300);
            });

            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performSearch(searchInput.value);
            });
        }
    }

    async performLiveSearch(query) {
        if (query.length < 2) return;

        try {
            const response = await apiManager.get(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
            this.displaySearchSuggestions(response.suggestions || []);
        } catch (error) {
            console.error('Live search failed:', error);
        }
    }

    async performSearch(query) {
        if (!query.trim()) {
            toastManager.warning('Please enter a search term', 'Search');
            return;
        }

        const searchBtn = document.querySelector('.search-form button[type="submit"]');
        LoadingManager.show(searchBtn, 'Searching...');

        try {
            // Add to search history
            this.addToSearchHistory(query);
            
            // Perform search
            const response = await apiManager.get(`/api/search?q=${encodeURIComponent(query)}`);
            
            if (response.success) {
                toastManager.success(`Found ${response.results.length} results`, 'Search Complete');
                
                // Update URL without page reload
                const newURL = `${window.location.pathname}?search=${encodeURIComponent(query)}`;
                window.history.pushState({ search: query }, '', newURL);
            } else {
                throw new Error(response.message || 'Search failed');
            }
        } catch (error) {
            console.error('Search failed:', error);
            toastManager.error('Search failed. Please try again.', 'Search Error');
        } finally {
            LoadingManager.hide(searchBtn);
        }
    }

    displaySearchSuggestions(suggestions) {
        // Implementation for search suggestions dropdown
        // This would integrate with the search suggestions API
        console.log('Search suggestions:', suggestions);
    }

    addToSearchHistory(query) {
        let history = JSON.parse(localStorage.getItem('pslvnews_search_history') || '[]');
        history = history.filter(item => item !== query);
        history.unshift(query);
        history = history.slice(0, 10); // Keep only last 10 searches
        localStorage.setItem('pslvnews_search_history', JSON.stringify(history));
    }
}

// Initialize enhanced search
const enhancedSearch = new EnhancedSearch();
