const elements = {
    loading: document.getElementById('loading'),
    error: document.getElementById('error'),
    articlesSection: document.getElementById('articles-section'),
    articlesGrid: document.getElementById('articles-grid')
};

async function fetchArticles() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/articles`);
        const data = await response.json();
        
        if (data.success) {
            displayArticles(data.articles);
        } else {
            showError(data.error || 'Error loading articles');
        }
    } catch (error) {
        showError('Error loading articles from database');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

function displayArticles(articlesData) {
    elements.articlesGrid.innerHTML = '';
    
    if (articlesData.length === 0) {
        elements.articlesGrid.innerHTML = '<p>No articles found.</p>';
        return;
    }
    
    articlesData.forEach(article => {
        const card = createArticleCard(article);
        elements.articlesGrid.appendChild(card);
    });
}

function createArticleCard(article) {
    const card = document.createElement('a');
    card.className = 'article-card';
    card.href = article.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    
    card.innerHTML = `
        <div class="article-category">${escapeHtml(article.category)}</div>
        <div class="article-title">${escapeHtml(article.title)}</div>
        <div class="article-description">${escapeHtml(article.description)}</div>
    `;
    
    return card;
}

function showLoading(show) {
    elements.loading.style.display = show ? 'block' : 'none';
}

function showError(message) {
    elements.error.textContent = message;
    elements.error.style.display = 'block';
}

function hideError() {
    elements.error.style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

window.addEventListener('DOMContentLoaded', () => {
    fetchArticles();
});
