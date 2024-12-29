document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme from localStorage or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);

    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');

    if (query && document.querySelector('input')) {
        document.querySelector('input').value = query;
    }

    if (query && document.getElementById('results-grid')) {
        displayResults(query);
    }
});

async function displayResults(query) {
    const resultsGrid = document.getElementById('results-grid');
    try {
        const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        resultsGrid.innerHTML = results.map((result, index) => `
            <div class="result-card" style="animation: fadeIn 0.5s ease-out ${index * 0.1}s forwards">
                <h2>${result.title}</h2>
                <p>${result.description}</p>
            </div>
        `).join('');
    } catch (error) {
        resultsGrid.innerHTML = '<div class="error">Error loading results</div>';
    }
}

function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Source filter update function
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sourceSelect = document.querySelector('select[name="source"]');
    const langSelect = document.querySelector('select[name="lang"]');
    const sourceInput = document.getElementById('sourceInput');
    const langInput = document.getElementById('langInput');
    
    // Get values from URL or localStorage
    const source = urlParams.get('source') || localStorage.getItem('source') || 'all';
    const lang = urlParams.get('lang') || localStorage.getItem('lang') || 'english';
    
    // Update selects and inputs
    if (sourceSelect) sourceSelect.value = source;
    if (langSelect) langSelect.value = lang;
    if (sourceInput) sourceInput.value = source;
    if (langInput) langInput.value = lang;
    
    // Form submission handler
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = searchForm.querySelector('input[name="q"]').value;
            const currentSource = sourceSelect.value;
            const currentLang = langSelect.value;
            window.location.href = `/results?q=${encodeURIComponent(query)}&source=${currentSource}&lang=${currentLang}`;
        });
    }
});

function updateSourceInput(value) {
    const sourceInput = document.getElementById('sourceInput');
    const sourceValue = value || 'all';
    if (sourceInput) {
        sourceInput.value = sourceValue;
        localStorage.setItem('source', sourceValue);
    }
}

function updateSource(value) {
    const sourceValue = value || 'all';
    localStorage.setItem('source', sourceValue);
    // Don't reload page, just update hidden input
    updateSourceInput(sourceValue);
}

function updateLang(value) {
    const langInput = document.getElementById('langInput');
    const langValue = value || 'english';
    if (langInput) {
        langInput.value = langValue;
        localStorage.setItem('lang', langValue);
    }
}