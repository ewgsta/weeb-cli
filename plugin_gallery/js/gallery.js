const translations = {
    en: {
        install: "Install",
        details: "Details",
        downloads: "downloads",
        rating: "rating",
        search: "Search plugins...",
        all: "All",
        provider: "Providers",
        utility: "Utilities",
        ui: "UI Themes",
        sort_downloads: "Most Downloaded",
        sort_rating: "Highest Rated",
        sort_recent: "Newest",
        hero_title: "Discover and Extend",
        hero_desc: "Custom providers and tools for Weeb CLI with secure sandboxing.",
        no_results: "No plugins found matching your criteria.",
        install_success: "Plugin installed successfully!",
        install_error: "Failed to install plugin.",
        close: "Close"
    },
    pl: {
        install: "Zainstaluj",
        details: "Szczegóły",
        downloads: "pobrań",
        rating: "ocena",
        search: "Szukaj wtyczek...",
        all: "Wszystkie",
        provider: "Dostawcy",
        utility: "Narzędzia",
        ui: "Motywy",
        sort_downloads: "Najczęściej pobierane",
        sort_rating: "Najwyżej oceniane",
        sort_recent: "Najnowsze",
        hero_title: "Odkrywaj i Rozszerzaj",
        hero_desc: "Niestandardowi dostawcy i narzędzia dla Weeb CLI z bezpieczną piaskownicą.",
        no_results: "Nie znaleziono wtyczek spełniających kryteria.",
        install_success: "Wtyczka zainstalowana pomyślnie!",
        install_error: "Błąd podczas instalacji wtyczki.",
        close: "Zamknij"
    }
};

// State
let currentLang = 'pl'; // Default to Polish as requested
let plugins = [];
let currentFilter = 'all';
let currentSort = 'downloads';
let searchQuery = '';

// DOM Elements
const grid = document.getElementById('plugins-grid');
const searchInput = document.getElementById('search-input');
const filterBtns = document.querySelectorAll('.filter-btn');
const sortSelect = document.getElementById('sort-select');
const modal = document.getElementById('plugin-modal');
const modalBody = document.getElementById('modal-body');
const closeModal = document.querySelector('.close-modal');
const themeToggle = document.getElementById('theme-toggle');
const toast = document.getElementById('toast');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    setupEventListeners();
    fetchPlugins();
});

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

function setupEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Search
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        renderPlugins();
    });

    // Filters
    filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentFilter = e.target.dataset.filter;
            renderPlugins();
        });
    });

    // Sort
    sortSelect.addEventListener('change', (e) => {
        currentSort = e.target.value;
        renderPlugins();
    });

    // Modal close
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Mock data fetch - In production, this would be an API call
async function fetchPlugins() {
    try {
        // Simulating API delay
        await new Promise(resolve => setTimeout(resolve, 800));
        
        plugins = [
            {
                id: 'ornek_plugin',
                name: 'Örnek Sağlayıcı',
                author: 'Weeb Team',
                version: '1.0.0',
                description: 'Przykładowa wtyczka demonstrująca nowy system.',
                category: 'provider',
                downloads: 1250,
                rating: 4.8,
                tags: ['anime', 'tr'],
                image: 'https://via.placeholder.com/300x160/1a1c2c/00bcd4?text=Weeb+CLI',
                readme: '# Örnek Sağlayıcı\n\nTo jest szczegółowy opis wtyczki.\n\n## Funkcje\n- Szybkie wyszukiwanie\n- Wysoka jakość streamów'
            },
            {
                id: 'anilist_sync',
                name: 'AniList Auto-Sync',
                author: 'Community',
                version: '2.1.0',
                description: 'Automatycznie synchronizuje postęp z AniList w tle.',
                category: 'utility',
                downloads: 8400,
                rating: 4.9,
                tags: ['tracker', 'sync'],
                image: 'https://via.placeholder.com/300x160/1a1c2c/ff4081?text=AniList',
                readme: '# AniList Auto-Sync\n\nSynchronizacja w czasie rzeczywistym.'
            },
            {
                id: 'discord_rpc_pro',
                name: 'Discord RPC Pro',
                author: 'Gamer123',
                version: '1.0.5',
                description: 'Rozszerzony status Discord z obrazkami i czasem odcinka.',
                category: 'ui',
                downloads: 3200,
                rating: 4.5,
                tags: ['social', 'discord'],
                image: 'https://via.placeholder.com/300x160/1a1c2c/7289da?text=Discord',
                readme: '# Discord RPC Pro\n\nPokaż znajomym, co oglądasz!'
            }
        ];
        
        renderPlugins();
    } catch (error) {
        grid.innerHTML = `<div class="error">Błąd ładowania wtyczek. Spróbuj ponownie później.</div>`;
    }
}

// Utility to prevent XSS
function escapeHTML(str) {
    if (!str) return '';
    return str.toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function getFilteredAndSortedPlugins() {
    let result = plugins.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery) || 
                              p.description.toLowerCase().includes(searchQuery) ||
                              p.author.toLowerCase().includes(searchQuery);
        const matchesFilter = currentFilter === 'all' || p.category === currentFilter;
        return matchesSearch && matchesFilter;
    });

    result.sort((a, b) => {
        if (currentSort === 'downloads') return b.downloads - a.downloads;
        if (currentSort === 'rating') return b.rating - a.rating;
        // Mock recent sort (just reverse id for now)
        return b.id.localeCompare(a.id);
    });

    return result;
}

function renderPlugins() {
    const filteredPlugins = getFilteredAndSortedPlugins();
    
    if (filteredPlugins.length === 0) {
        grid.innerHTML = `<div class="no-results">${translations[currentLang].no_results}</div>`;
        return;
    }

    grid.innerHTML = filteredPlugins.map(p => `
        <div class="card">
            <img src="${escapeHTML(p.image)}" alt="${escapeHTML(p.name)}" class="card-img">
            <div class="card-content">
                <div class="card-header">
                    <h3 class="card-title">${escapeHTML(p.name)}</h3>
                    <span class="version">v${escapeHTML(p.version)}</span>
                </div>
                <p class="author">by ${escapeHTML(p.author)}</p>
                <p class="desc">${escapeHTML(p.description)}</p>
                
                <div class="tags">
                    ${p.tags.map(t => `<span class="tag">${escapeHTML(t)}</span>`).join('')}
                </div>
                
                <div class="stats">
                    <span><i class="fas fa-download"></i> ${escapeHTML(p.downloads)}</span>
                    <span><i class="fas fa-star" style="color: #ffd700;"></i> ${escapeHTML(p.rating)}</span>
                </div>
            </div>
            <div class="card-actions">
                <button class="btn btn-outline" onclick="openDetails('${escapeHTML(p.id)}')">
                    <i class="fas fa-info-circle"></i> ${escapeHTML(translations[currentLang].details)}
                </button>
                <button class="btn btn-primary" onclick="installPlugin('${escapeHTML(p.id)}')">
                    <i class="fas fa-download"></i> ${escapeHTML(translations[currentLang].install)}
                </button>
            </div>
        </div>
    `).join('');
}

function openDetails(id) {
    const plugin = plugins.find(p => p.id === id);
    if (!plugin) return;

    // Simple markdown to HTML parser for demo
    // Note: In production, use a library like marked.js to safely render markdown
    let htmlReadme = escapeHTML(plugin.readme);
    htmlReadme = htmlReadme
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    // Bug 0002: Fixed 'p' variable error, using 'plugin'
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/\n\n/g, '<br><br>');

    modalBody.innerHTML = `
        <div class="modal-header">
            <img src="${escapeHTML(plugin.image)}" alt="${escapeHTML(plugin.name)}">
            <div class="modal-title-area">
                <h2>${escapeHTML(plugin.name)} <span class="version">v${escapeHTML(plugin.version)}</span></h2>
                <p class="author">by ${escapeHTML(plugin.author)}</p>
                <div class="stats">
                    <span><i class="fas fa-download"></i> ${escapeHTML(plugin.downloads)} pobrań</span>
                    <span><i class="fas fa-star" style="color: #ffd700;"></i> ${escapeHTML(plugin.rating)}</span>
                </div>
                <div class="tags" style="margin-top: 10px;">
                    ${plugin.tags.map(t => `<span class="tag">${escapeHTML(t)}</span>`).join('')}
                </div>
            </div>
        </div>
        <div class="modal-actions" style="margin: 20px 0; display: flex; gap: 10px;">
            <button class="btn btn-primary" onclick="installPlugin('${escapeHTML(plugin.id)}')" style="flex: 1;">
                <i class="fas fa-download"></i> Zainstaluj z Weeb CLI
            </button>
        </div>
        <div class="markdown-body">
            ${htmlReadme}
        </div>
    `;

    modal.style.display = 'block';
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Mock installation flow via custom protocol handler
function installPlugin(id) {
    const plugin = plugins.find(p => p.id === id);
    if (!plugin) return;
    
    // In a real app, this would use a custom protocol handler like weeb-cli://install/plugin_id
    // For the demo, we'll simulate the process
    showToast(`Inicjowanie instalacji ${plugin.name}...`, 'success');
    
    setTimeout(() => {
        alert(`Otwórz Weeb CLI i uruchom:\n\nweeb-cli plugin install ${id}\n\nlub wklej ten adres URL w ustawieniach wtyczek:\nhttps://raw.githubusercontent.com/ewgsta/weeb-cli/main/data/${id}/plugin.weeb`);
    }, 1000);
}
