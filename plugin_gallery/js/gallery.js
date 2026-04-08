const TRANSLATIONS = {
    en: {
        "hero-title": "Discover and Extend",
        "hero-desc": "Custom providers and tools for Weeb CLI.",
        "search-placeholder": "Search plugins...",
        "no-plugins": "No plugins found.",
        "install-btn": "Install",
        "details-btn": "Details",
        "author": "by {author}",
        "version": "v{version}",
        "download-btn": "Download .weeb",
        "back-btn": "Back to Gallery"
    },
    tr: {
        "hero-title": "Keşfet ve Genişlet",
        "hero-desc": "Weeb CLI için özel sağlayıcılar ve araçlar.",
        "search-placeholder": "Eklenti ara...",
        "no-plugins": "Eklenti bulunamadı.",
        "install-btn": "Yükle",
        "details-btn": "Detaylar",
        "author": "Yazar: {author}",
        "version": "v{version}",
        "download-btn": ".weeb İndir",
        "back-btn": "Galeriye Dön"
    },
    de: {
        "hero-title": "Entdecken und Erweitern",
        "hero-desc": "Benutzerdefinierte Anbieter und Tools für Weeb CLI.",
        "search-placeholder": "Plugins suchen...",
        "no-plugins": "Keine Plugins gefunden.",
        "install-btn": "Installieren",
        "details-btn": "Details",
        "author": "von {author}",
        "version": "v{version}",
        "download-btn": ".weeb Herunterladen",
        "back-btn": "Zurück zur Galerie"
    },
    fr: {
        "hero-title": "Découvrir et Étendre",
        "hero-desc": "Fournisseurs et outils personnalisés pour Weeb CLI.",
        "search-placeholder": "Rechercher des plugins...",
        "no-plugins": "Aucun plugin trouvé.",
        "install-btn": "Installer",
        "details-btn": "Détails",
        "author": "par {author}",
        "version": "v{version}",
        "download-btn": "Télécharger .weeb",
        "back-btn": "Retour à la Galerie"
    }
};

let currentLang = localStorage.getItem('weeb-lang') || 'en';
let currentTheme = localStorage.getItem('weeb-theme') || 'dark';

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLanguage();
    fetchPlugins();
});

function initTheme() {
    document.documentElement.setAttribute('data-theme', currentTheme);
    const themeBtn = document.getElementById('theme-toggle');
    themeBtn.addEventListener('click', () => {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', currentTheme);
        localStorage.setItem('weeb-theme', currentTheme);
    });
}

function initLanguage() {
    const langSelect = document.getElementById('lang-select');
    langSelect.value = currentLang;
    langSelect.addEventListener('change', (e) => {
        currentLang = e.target.value;
        localStorage.setItem('weeb-lang', currentLang);
        updateUI();
    });
    updateUI();
}

function updateUI() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (TRANSLATIONS[currentLang][key]) {
            el.textContent = TRANSLATIONS[currentLang][key];
        }
    });
}

async function fetchPlugins() {
    const grid = document.getElementById('plugins-grid');
    const loader = document.getElementById('loader');
    
    try {
        // In a real scenario, this would fetch from a JSON file generated from PRs
        // For now, let's use some mock data
        const plugins = [
            {
                id: "sample-plugin",
                name: "Sample Plugin",
                version: "1.0.0",
                author: "Weeb CLI Team",
                description: "A basic sample plugin to demonstrate the plugin system.",
                image: "https://via.placeholder.com/300x180?text=Sample+Plugin"
            },
            {
                id: "anilist-enhanced",
                name: "AniList Enhanced",
                version: "1.2.5",
                author: "Community",
                description: "Better synchronization and extra info for AniList users.",
                image: "https://via.placeholder.com/300x180?text=AniList+Enhanced"
            }
        ];
        
        loader.style.display = 'none';
        
        plugins.forEach(plugin => {
            const card = document.createElement('div');
            card.className = 'plugin-card';
            card.innerHTML = `
                <div class="image-container">
                    <img src="${plugin.image}" alt="${plugin.name}">
                </div>
                <div class="content">
                    <h3>${plugin.name}</h3>
                    <div class="meta">${TRANSLATIONS[currentLang].author.replace('{author}', plugin.author)} | ${TRANSLATIONS[currentLang].version.replace('{version}', plugin.version)}</div>
                    <p>${plugin.description}</p>
                </div>
                <div class="actions">
                    <a href="#" class="btn btn-primary" onclick="installPlugin('${plugin.id}')">${TRANSLATIONS[currentLang]['install-btn']}</a>
                    <a href="#" class="btn btn-outline">${TRANSLATIONS[currentLang]['details-btn']}</a>
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (err) {
        console.error("Failed to fetch plugins", err);
        loader.innerHTML = "Error loading plugins.";
    }
}

function installPlugin(id) {
    alert(`To install this plugin, copy the URL and use the load plugin option in the settings menu of Weeb CLI.\n\nURL: https://raw.githubusercontent.com/ewgsta/weeb-cli/main/plugins/${id}.weeb`);
}
