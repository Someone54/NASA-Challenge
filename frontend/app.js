let categories = [];
let currentCategoryId = null;
let currentCategoryName = '';

const elements = {
    loading: document.getElementById('loading'),
    error: document.getElementById('error'),
    categoriesSection: document.getElementById('categories-section'),
    articlesSection: document.getElementById('articles-section'),
    categoriesGrid: document.getElementById('categories-grid'),
    articlesGrid: document.getElementById('articles-grid'),
    categoryTitle: document.getElementById('category-title'),
    backButton: document.getElementById('back-button')
};

async function fetchCategories() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/categories`);
        const data = await response.json();
        
        if (data.success) {
            categories = data.categories;
            displayCategories(categories);
        } else {
            showError(data.error || 'Error loading categories');
        }
    } catch (error) {
        showError('Error connecting to the API. Please check the API_BASE_URL in app.js');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

function displayCategories(categoriesData) {
    elements.categoriesGrid.innerHTML = '';
    
    if (categoriesData.length === 0) {
        elements.categoriesGrid.innerHTML = '<p>No categories found. Please populate the database first.</p>';
        return;
    }
    
    categoriesData.forEach(category => {
        const card = createCategoryCard(category);
        elements.categoriesGrid.appendChild(card);
    });
}

function createCategoryCard(category) {
    const card = document.createElement('div');
    card.className = 'card';
    card.onclick = () => loadArticles(category.id, category.name);
    
    card.innerHTML = `
        <div class="card-title">${escapeHtml(category.name)}</div>
        <span class="card-count">${category.article_count} articles</span>
    `;
    
    return card;
}

async function loadArticles(categoryId, categoryName) {
    try {
        showLoading(true);
        hideError();
        
        currentCategoryId = categoryId;
        currentCategoryName = categoryName;
        
        const response = await fetch(`${API_BASE_URL}/articles?category_id=${categoryId}`);
        const data = await response.json();
        
        if (data.success) {
            displayArticles(data.articles);
            showArticlesView();
        } else {
            showError(data.error || 'Error loading articles');
        }
    } catch (error) {
        showError('Error loading articles from API');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

function displayArticles(articlesData) {
    elements.articlesGrid.innerHTML = '';
    elements.categoryTitle.textContent = currentCategoryName;
    
    if (articlesData.length === 0) {
        elements.articlesGrid.innerHTML = '<p>No articles found in this category.</p>';
        return;
    }
    
    articlesData.forEach(article => {
        const card = createArticleCard(article);
        elements.articlesGrid.appendChild(card);
    });
}

function createArticleCard(article) {
    const card = document.createElement('div');
    card.className = 'article-card';
    
    card.innerHTML = `
        <div class="article-title">${escapeHtml(article.title)}</div>
        <div class="article-description">${escapeHtml(article.description || 'No description available')}</div>
        <a href="${escapeHtml(article.url)}" target="_blank" class="article-link">
            Read Full Article →
        </a>
    `;
    
    return card;
}

function showArticlesView() {
    elements.categoriesSection.style.display = 'none';
    elements.articlesSection.style.display = 'block';
}

function showCategoriesView() {
    elements.categoriesSection.style.display = 'block';
    elements.articlesSection.style.display = 'none';
    currentCategoryId = null;
    currentCategoryName = '';
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

elements.backButton.addEventListener('click', showCategoriesView);

window.addEventListener('DOMContentLoaded', () => {
    fetchCategories();
});
