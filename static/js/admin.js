// Admin Dashboard JavaScript

// Global variables
let currentPage = 1;
let currentLimit = 20;
let isLoading = false;

// Initialize admin dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminDashboard();
});

function initializeAdminDashboard() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize mobile menu
    initializeMobileMenu();
    
    // Initialize notifications
    initializeNotifications();
    
    // Initialize modal functionality
    initializeModalHandlers();
    
    // Auto-refresh dashboard data
    if (window.location.pathname.includes('/admin/dashboard')) {
        startAutoRefresh();
    }
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Mobile menu functionality
function initializeMobileMenu() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebar = document.querySelector('.admin-sidebar');
    
    if (mobileMenuToggle && sidebar) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');
        });
    }
}

// Notification system
function initializeNotifications() {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
}

// Initialize modal event handlers
function initializeModalHandlers() {
    // ESC key to close modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            const modal = document.getElementById('news-details-modal');
            if (modal && modal.style.display === 'flex') {
                closeNewsModal();
            }
        }
    });
    
    // Click outside modal to close
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('news-details-modal');
        if (modal && event.target === modal) {
            closeNewsModal();
        }
    });
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, duration);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Loading states
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
    isLoading = true;
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
    isLoading = false;
}

// API helper functions
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API request failed:', error);
        showNotification('Request failed: ' + error.message, 'error');
        throw error;
    }
}

// Dashboard refresh
function refreshData() {
    if (isLoading) return;
    
    showLoading();
    setTimeout(() => {
        location.reload();
    }, 1000);
}

// Auto-refresh functionality
function startAutoRefresh(interval = 300000) { // 5 minutes default
    setInterval(() => {
        if (!isLoading && document.visibilityState === 'visible') {
            refreshData();
        }
    }, interval);
}

// News management functions
async function loadNewsData(page = 1, limit = 20, category = 'all', search = '') {
    if (isLoading) return;
    
    showLoading();
    try {
        const params = new URLSearchParams({
            page: page,
            limit: limit,
            category: category,
            search: search
        });
        
        const data = await apiRequest(`/admin/news/data?${params}`);
        updateNewsTable(data);
        updatePagination(data);
        
    } catch (error) {
        console.error('Failed to load news data:', error);
    } finally {
        hideLoading();
    }
}

function updateNewsTable(data) {
    const tableBody = document.getElementById('news-table-body');
    if (!tableBody) return;
    
    if (!data.articles || data.articles.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">No news articles found</td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = data.articles.map(article => `
        <tr>
            <td>
                <div class="news-title-cell">
                    <strong>${escapeHtml(article.title || 'Untitled')}</strong>
                </div>
            </td>
            <td>
                <span class="badge badge-${getCategoryColor(article.category)}">
                    ${escapeHtml(article.category || 'Unknown')}
                </span>
            </td>
            <td>${escapeHtml(article.source || 'Unknown')}</td>
            <td>
                <div class="credibility-score">
                    ${(article.credibility * 100 || 0).toFixed(1)}%
                </div>
            </td>
            <td>
                <span class="sentiment-score ${getSentimentClass(article.sentiment_score)}">
                    ${(article.sentiment_score || 0).toFixed(2)}
                </span>
            </td>
            <td>
                ${article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : 'Unknown'}
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-outline" onclick="viewNews('${article._id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline" onclick="editNews('${article._id}')">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function updatePagination(data) {
    const paginationContainer = document.getElementById('pagination-container');
    if (!paginationContainer) return;
    
    const { current_page, total_pages, has_next, has_prev } = data;
    
    paginationContainer.innerHTML = `
        <div class="pagination">
            <button class="btn btn-sm" ${!has_prev ? 'disabled' : ''} 
                    onclick="loadNewsData(${current_page - 1})">
                <i class="fas fa-chevron-left"></i> Previous
            </button>
            <span class="pagination-info">
                Page ${current_page} of ${total_pages}
            </span>
            <button class="btn btn-sm" ${!has_next ? 'disabled' : ''} 
                    onclick="loadNewsData(${current_page + 1})">
                Next <i class="fas fa-chevron-right"></i>
            </button>
        </div>
    `;
}

// User management functions
async function loadUsersData(page = 1, limit = 20, role = 'all') {
    if (isLoading) return;
    
    showLoading();
    try {
        const params = new URLSearchParams({
            page: page,
            limit: limit,
            role: role
        });
        
        const data = await apiRequest(`/admin/users/data?${params}`);
        updateUsersTable(data);
        
    } catch (error) {
        console.error('Failed to load users data:', error);
    } finally {
        hideLoading();
    }
}

function updateUsersTable(data) {
    const tableBody = document.getElementById('users-table-body');
    if (!tableBody) return;
    
    if (!data.users || data.users.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">No users found</td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = data.users.map(user => `
        <tr>
            <td>
                <div class="user-info">
                    <strong>${escapeHtml(user.first_name || '')} ${escapeHtml(user.last_name || '')}</strong>
                    <br>
                    <small>${escapeHtml(user.email || '')}</small>
                </div>
            </td>
            <td>${user.age || 'N/A'}</td>
            <td>${escapeHtml(user.location || 'N/A')}</td>
            <td>
                <select class="role-select" onchange="updateUserRole('${user._id}', this.value)">
                    <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                    <option value="news_reporter" ${user.role === 'news_reporter' ? 'selected' : ''}>News Reporter</option>
                    <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                </select>
            </td>
            <td>
                ${user.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
            </td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-outline" onclick="viewUser('${user._id}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteUser('${user._id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// Chart initialization
function initializeCharts(chartData) {
    if (!chartData) return;
    
    // Category Distribution Chart
    if (chartData.category_distribution) {
        initializeCategoryChart(chartData.category_distribution);
    }
    
    // Sentiment Distribution Chart
    if (chartData.sentiment_distribution) {
        initializeSentimentChart(chartData.sentiment_distribution);
    }
    
    // Fake vs Real News Chart
    if (chartData.fake_vs_real_ratio) {
        initializeFakeRealChart(chartData.fake_vs_real_ratio);
    }
    
    // Credibility Distribution Chart
    if (chartData.credibility_distribution) {
        initializeCredibilityChart(chartData.credibility_distribution);
    }
    
    // News per Source Chart
    if (chartData.news_per_source) {
        initializeSourceChart(chartData.news_per_source);
    }
}

function initializeCategoryChart(data) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.map(item => item.category || 'Unknown'),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', 
                    '#4BC0C0', '#9966FF', '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'News by Category'
                }
            }
        }
    });
}

function initializeSentimentChart(data) {
    const ctx = document.getElementById('sentimentChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.sentiment),
            datasets: [{
                label: 'Number of Articles',
                data: data.map(item => item.count),
                backgroundColor: '#36A2EB'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Sentiment Distribution'
                }
            }
        }
    });
}

function initializeFakeRealChart(data) {
    const ctx = document.getElementById('fakeRealChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(item => item.type),
            datasets: [{
                data: data.map(item => item.count),
                backgroundColor: ['#4BC0C0', '#FF6384']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Fake vs Real News Ratio'
                }
            }
        }
    });
}

function initializeCredibilityChart(data) {
    const ctx = document.getElementById('credibilityChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => item.range),
            datasets: [{
                label: 'Number of Articles',
                data: data.map(item => item.count),
                borderColor: '#36A2EB',
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Credibility Score Distribution'
                }
            }
        }
    });
}

function initializeSourceChart(data) {
    const ctx = document.getElementById('sourceChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.source),
            datasets: [{
                label: 'Articles Published',
                data: data.map(item => item.count),
                backgroundColor: '#FFCE56'
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'News per Source'
                }
            }
        }
    });
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getCategoryColor(category) {
    const colors = {
        'politics': 'danger',
        'technology': 'info',
        'sports': 'success',
        'business': 'warning',
        'health': 'primary',
        'science': 'secondary'
    };
    return colors[category?.toLowerCase()] || 'secondary';
}

function getSentimentClass(score) {
    if (score > 0.1) return 'positive';
    if (score < -0.1) return 'negative';
    return 'neutral';
}

// Action handlers
async function updateUserRole(userId, newRole) {
    try {
        const response = await apiRequest('/admin/users/update-role', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, role: newRole })
        });
        
        if (response.success) {
            showNotification('User role updated successfully', 'success');
        } else {
            showNotification(response.message || 'Failed to update user role', 'error');
        }
    } catch (error) {
        showNotification('Failed to update user role', 'error');
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) {
        return;
    }
    
    try {
        const response = await apiRequest('/admin/users/delete', {
            method: 'POST',
            body: JSON.stringify({ user_id: userId })
        });
        
        if (response.success) {
            showNotification('User deleted successfully', 'success');
            loadUsersData(currentPage);
        } else {
            showNotification(response.message || 'Failed to delete user', 'error');
        }
    } catch (error) {
        showNotification('Failed to delete user', 'error');
    }
}

function viewNews(newsId) {
    openNewsModal(newsId);
}

function editNews(newsId) {
    showNotification('Edit functionality coming soon', 'info');
}

// News Modal Functions
async function openNewsModal(newsId) {
    const modal = document.getElementById('news-details-modal');
    const modalBody = document.getElementById('news-modal-body');
    
    if (!modal || !modalBody) {
        console.error('Modal elements not found');
        return;
    }
    
    // Show loading state
    modalBody.innerHTML = `
        <div class="modal-loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Loading article details...</p>
        </div>
    `;
    
    // Show modal
    modal.style.display = 'flex';
    
    try {
        // Fetch news details
        const response = await fetch(`/admin/news/${newsId}`);
        const data = await response.json();
        
        if (data.success && data.article) {
            // Populate modal content
            populateNewsModal(data.article);
        } else {
            // Show error state
            modalBody.innerHTML = `
                <div class="modal-loading">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Failed to load article details</p>
                    <button class="btn btn-sm btn-outline" onclick="closeNewsModal()">
                        <i class="fas fa-times"></i> Close
                    </button>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error fetching news details:', error);
        modalBody.innerHTML = `
            <div class="modal-loading">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Network error loading article details</p>
                <button class="btn btn-sm btn-outline" onclick="closeNewsModal()">
                    <i class="fas fa-times"></i> Close
                </button>
            </div>
        `;
    }
}

function closeNewsModal() {
    const modal = document.getElementById('news-details-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function populateNewsModal(article) {
    const modalBody = document.getElementById('news-modal-body');
    if (!modalBody) return;
    
    // Format date
    const formatDate = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    
    // Format date components
    const formatDateComponent = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return {
            date: date.toLocaleDateString('en-US'),
            time: date.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            }),
            week: date.toLocaleDateString('en-US', { weekday: 'long' }),
            month: date.toLocaleDateString('en-US', { month: 'long' }),
            year: date.getFullYear().toString()
        };
    };
    
    // Format credibility score
    const formatCredibility = (credibility) => {
        if (!credibility) return { score: 0, class: 'credibility-low' };
        const score = (credibility * 100).toFixed(1);
        let className = 'credibility-low';
        if (score >= 70) className = 'credibility-high';
        else if (score >= 40) className = 'credibility-medium';
        return { score, class: className };
    };
    
    // Format sentiment
    const formatSentiment = (sentiment) => {
        if (!sentiment) return { score: 0, class: 'sentiment-neutral', label: 'Neutral' };
        const score = sentiment.toFixed(2);
        let className = 'sentiment-neutral';
        let label = 'Neutral';
        if (sentiment > 0.1) { className = 'sentiment-positive'; label = 'Positive'; }
        else if (sentiment < -0.1) { className = 'sentiment-negative'; label = 'Negative'; }
        return { score, class: className, label };
    };
    
    const dateInfo = formatDateComponent(article.publishedAt);
    const credibility = formatCredibility(article.credibility);
    const sentiment = formatSentiment(article.sentiment_score);
    
    // Build modal content
    modalBody.innerHTML = `
        <div class="news-details-content">
            <!-- Basic Information -->
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-info-circle"></i>
                    Basic Information
                </h3>
                <div class="basic-info-grid">
                    <div class="info-item">
                        <div class="info-label">Title</div>
                        <div class="info-value highlight large">${escapeHtml(article.title || 'Untitled')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Category</div>
                        <div class="info-value">${escapeHtml(article.category || 'General')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Source</div>
                        <div class="info-value">${escapeHtml(article.source || 'Unknown')}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Status</div>
                        <div class="info-value">
                            <span class="badge ${article.status === 'published' ? 'badge-success' : 'badge-warning'}">
                                ${escapeHtml(article.status || 'Unknown')}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Content -->
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-file-alt"></i>
                    Content
                </h3>
                ${article.summary ? `
                <div class="content-item">
                    <div class="content-label">
                        <i class="fas fa-list"></i>
                        Summary
                    </div>
                    <div class="content-text">${escapeHtml(article.summary)}</div>
                </div>
                ` : ''}
                ${article.content ? `
                <div class="content-item">
                    <div class="content-label">
                        <i class="fas fa-align-left"></i>
                        Content
                    </div>
                    <div class="content-text">${escapeHtml(article.content)}</div>
                </div>
                ` : ''}
                ${article.full_text ? `
                <div class="content-item">
                    <div class="content-label">
                        <i class="fas fa-file-text"></i>
                        Full Text
                    </div>
                    <div class="content-text">${escapeHtml(article.full_text)}</div>
                </div>
                ` : ''}
            </div>
            
            <!-- Meta Information -->
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-calendar-alt"></i>
                    Meta Information
                </h3>
                <div class="basic-info-grid">
                    <div class="info-item">
                        <div class="info-label">Published Date</div>
                        <div class="info-value">${formatDate(article.publishedAt)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Date</div>
                        <div class="info-value">${escapeHtml(dateInfo.date)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Time</div>
                        <div class="info-value">${escapeHtml(dateInfo.time)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Week</div>
                        <div class="info-value">${escapeHtml(dateInfo.week)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Month</div>
                        <div class="info-value">${escapeHtml(dateInfo.month)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Year</div>
                        <div class="info-value">${escapeHtml(dateInfo.year)}</div>
                    </div>
                </div>
            </div>
            
            <!-- Analysis -->
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-chart-line"></i>
                    Analysis
                </h3>
                <div class="analysis-grid">
                    <div class="analysis-item">
                        <span class="analysis-value ${credibility.class}">${credibility.score}%</span>
                        <div class="analysis-label">Credibility Score</div>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-value">${article.fake_prob || 0}%</span>
                        <div class="analysis-label">Fake Probability</div>
                    </div>
                    <div class="analysis-item">
                        <span class="analysis-value ${sentiment.class}">${sentiment.score}</span>
                        <div class="analysis-label">Sentiment Score (${sentiment.label})</div>
                    </div>
                    ${article.reliability_score ? `
                    <div class="analysis-item">
                        <span class="analysis-value">${(article.reliability_score * 100).toFixed(1)}%</span>
                        <div class="analysis-label">Reliability Score</div>
                    </div>
                    ` : ''}
                </div>
            </div>
            
            <!-- Reporter Details -->
            ${article.reporter_details ? `
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-user"></i>
                    Reporter Details
                </h3>
                <div class="reporter-grid">
                    ${article.reporter_details.name ? `
                    <div class="info-item">
                        <div class="info-label">Reporter Name</div>
                        <div class="info-value">${escapeHtml(article.reporter_details.name)}</div>
                    </div>
                    ` : ''}
                    ${article.reporter_details.email ? `
                    <div class="info-item">
                        <div class="info-label">Email</div>
                        <div class="info-value">${escapeHtml(article.reporter_details.email)}</div>
                    </div>
                    ` : ''}
                    ${article.reporter_details.phone ? `
                    <div class="info-item">
                        <div class="info-label">Phone</div>
                        <div class="info-value">${escapeHtml(article.reporter_details.phone)}</div>
                    </div>
                    ` : ''}
                    ${article.reporter_details.organization ? `
                    <div class="info-item">
                        <div class="info-label">Organization</div>
                        <div class="info-value">${escapeHtml(article.reporter_details.organization)}</div>
                    </div>
                    ` : ''}
                </div>
            </div>
            ` : ''}
            
            <!-- Evidence Sources -->
            ${article.evidence_sources && article.evidence_sources.length > 0 ? `
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-link"></i>
                    Evidence Sources
                </h3>
                <div class="evidence-sources-list">
                    ${article.evidence_sources.map((source, index) => `
                        <div class="evidence-source">
                            <div class="evidence-title">Source ${index + 1}</div>
                            <a href="${escapeHtml(source)}" target="_blank" class="evidence-link">
                                <i class="fas fa-external-link-alt"></i>
                                ${escapeHtml(source)}
                            </a>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            <!-- Additional Fields -->
            <div class="details-section">
                <h3 class="section-title">
                    <i class="fas fa-database"></i>
                    Additional Information
                </h3>
                <div class="basic-info-grid">
                    ${article.country ? `
                    <div class="info-item">
                        <div class="info-label">Country</div>
                        <div class="info-value">${escapeHtml(article.country)}</div>
                    </div>
                    ` : ''}
                    ${article.language ? `
                    <div class="info-item">
                        <div class="info-label">Language</div>
                        <div class="info-value">${escapeHtml(article.language)}</div>
                    </div>
                    ` : ''}
                    ${article.url ? `
                    <div class="info-item">
                        <div class="info-label">Original URL</div>
                        <div class="info-value">
                            <a href="${escapeHtml(article.url)}" target="_blank" class="evidence-link">
                                <i class="fas fa-external-link-alt"></i>
                                View Original
                            </a>
                        </div>
                    </div>
                    ` : ''}
                    <div class="info-item">
                        <div class="info-label">Article ID</div>
                        <div class="info-value" style="font-family: monospace; font-size: 0.8rem;">
                            ${escapeHtml(article._id)}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function viewUser(userId) {
    showNotification('User details functionality coming soon', 'info');
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const searchTerm = this.value;
            loadNewsData(1, currentLimit, 'all', searchTerm);
        }, 500));
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize search when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});
