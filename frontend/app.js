const elements = {
    loading: document.getElementById('loading'),
    error: document.getElementById('error'),
    categoriesSection: document.getElementById('categories-section'),
    articlesSection: document.getElementById('articles-section'),
    categoriesGrid: document.getElementById('categories-grid'),
    articlesGrid: document.getElementById('articles-grid'),
    backButton: document.getElementById('back-to-categories'),
    categoryName: document.getElementById('category-name'),
    articlesTitle: document.getElementById('articles-title')
};

const CATEGORY_NAMES = {
    1: 'Biología Espacial y Humana',
    2: 'Biotecnología y Biomedicina Avanzada',
    3: 'Microbiología y Biología Molecular',
    4: 'Genética y Epigenética',
    5: 'Exobiología y Astrobiología',
    6: 'Fisiología y Adaptación Biológica',
    7: 'Biología del Desarrollo y Reproducción',
    8: 'Ciencias de la Salud',
    9: 'Ecología y Ecosistemas',
    10: 'Biología de Plantas y Agricultura Espacial',
    11: 'Neurociencia',
    12: 'Biotecnología Aplicada y Sostenibilidad'
};

async function fetchCategories() {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/categories`);
        const data = await response.json();
        
        if (data.success) {
            displayCategories(data.categories);
        } else {
            showError(data.error || 'Error loading categories');
        }
    } catch (error) {
        showError('Error loading categories from database');
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

async function fetchArticlesByCategory(categoryId) {
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch(`${API_BASE_URL}/articles`);
        const data = await response.json();
        
        if (data.success) {
            const filteredArticles = data.articles.filter(article => article.category == categoryId);
            displayArticles(filteredArticles, categoryId);
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

function displayCategories(categories) {
    elements.categoriesGrid.innerHTML = '';
    
    if (categories.length === 0) {
        elements.categoriesGrid.innerHTML = '<p>No categories found.</p>';
        return;
    }
    
    categories.forEach(category => {
        const card = createCategoryCard(category);
        elements.categoriesGrid.appendChild(card);
    });
}

function createCategoryCard(category) {
    const card = document.createElement('div');
    card.className = 'category-card';
    card.onclick = () => showCategoryArticles(category.id);
    
    const categoryName = CATEGORY_NAMES[category.id] || `Category ${category.id}`;
    
    card.innerHTML = `
        <div class="category-icon">📚</div>
        <div class="category-name">${escapeHtml(categoryName)}</div>
        <div class="category-count">${category.article_count} articles</div>
    `;
    
    return card;
}

function showCategoryArticles(categoryId) {
    elements.categoriesSection.style.display = 'none';
    elements.articlesSection.style.display = 'block';
    
    const categoryName = CATEGORY_NAMES[categoryId] || `Category ${categoryId}`;
    elements.categoryName.textContent = categoryName;
    elements.articlesTitle.textContent = `Articles in ${categoryName}`;
    
    fetchArticlesByCategory(categoryId);
}

function displayArticles(articlesData, categoryId) {
    elements.articlesGrid.innerHTML = '';
    
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
    const card = document.createElement('a');
    card.className = 'article-card';
    card.href = article.url;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    
    const categoryName = CATEGORY_NAMES[article.category] || `Category ${article.category}`;
    
    card.innerHTML = `
        <div class="article-category">${escapeHtml(categoryName)}</div>
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

// Event listeners
elements.backButton.addEventListener('click', (e) => {
    e.preventDefault();
    elements.articlesSection.style.display = 'none';
    elements.categoriesSection.style.display = 'block';
});

window.addEventListener('DOMContentLoaded', () => {
    fetchCategories();
});
