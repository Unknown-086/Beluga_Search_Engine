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