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

async function fetchContent() {
    const urlInput = document.getElementById('link');
    const errorElement = document.getElementById('url-error');
    const url = urlInput.value;

    // Clear previous error
    errorElement.textContent = '';
    
    if (!url) {
        errorElement.textContent = 'Please enter a URL';
        return;
    }

    try {
        // Validate URL format
        new URL(url);
        
        const response = await fetch(`/api/fetch-content?url=${encodeURIComponent(url)}`);
        const data = await response.json();
        
        if (data.error) {
            if (data.error.includes('HTTPError')) {
                errorElement.textContent = 'Website does not allow content fetching';
            } else if (data.error.includes('Invalid URL')) {
                errorElement.textContent = 'Invalid URL format';
            } else {
                errorElement.textContent = "Failed to fetch content. This Website doesn't allow content fetching";
            }
            return;
        }
        
        // Update form fields
        document.getElementById('title').value = data.title || '';
        document.getElementById('description').value = data.description || '';
        document.getElementById('content').value = data.content || '';
        
    } catch (error) {
        if (error instanceof TypeError) {
            errorElement.textContent = 'Invalid URL format';
        } else {
            errorElement.textContent = 'Failed to fetch content';
        }
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    
    const formData = {
        url: document.getElementById('link').value,
        title: document.getElementById('title').value,
        description: document.getElementById('description').value || '',
        content: document.getElementById('content').value || ''
    };

    const errorElement = document.getElementById('url-error');
    errorElement.textContent = ''; // Clear previous errors

    try {
        const response = await fetch('/api/add-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Content added successfully!');
            window.location.href = '/';
        } else {
            // Check for duplicate URL error
            if (data.error && data.error.includes('URL already exists')) {
                errorElement.textContent = 'This URL has already been added to the dataset';
            } else {
                errorElement.textContent = data.error || 'Failed to add content';
            }
        }
    } catch (error) {
        errorElement.textContent = 'Error adding content: ' + error.message;
    }
}

function handleSearch(event) {
    event.preventDefault();
    const query = document.getElementById('searchInput').value;
    const source = document.getElementById('sourceSelect').value;
    const lang = document.getElementById('langSelect').value;
    
    if (query) {
        window.location.href = `/results?q=${encodeURIComponent(query)}&page=1&source=${source}&lang=${lang}`;
    }
}