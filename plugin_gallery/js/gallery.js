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
    },
    pl: {
        "hero-title": "Odkrywaj i Rozszerzaj",
        "hero-desc": "Niestandardowi dostawcy i narzędzia dla Weeb CLI.",
        "search-placeholder": "Szukaj wtyczek...",
        "no-plugins": "Nie znaleziono wtyczek.",
        "install-btn": "Zainstaluj",
        "details-btn": "Szczegóły",
        "author": "przez {author}",
        "version": "v{version}",
        "download-btn": "Pobierz .weeb",
        "back-btn": "Powrót do Galerii"
    }
};

let currentLang = localStorage.getItem('weeb-lang') || 'en';
let currentTheme = localStorage.getItem('weeb-theme') || 'dark';
let pluginsData = [];

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initLanguage();
    fetchPlugins();
    initModal();
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

function initModal() {
    const modal = document.getElementById("modal");
    const span = document.getElementsByClassName("close")[0];
    
    span.onclick = function() {
        modal.style.display = "none";
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

function showPluginDetails(id) {
    const plugin = pluginsData.find(p => p.id === id);
    if (!plugin) return;
    
    const modal = document.getElementById("modal");
    const body = document.getElementById("modal-body");
    
    body.innerHTML = `
        <div class="plugin-header">
            <img src="${plugin.image}" alt="${plugin.name}" style="width: 100%; max-height: 250px; object-fit: cover;">
            <div style="margin-top: 1rem;">
                <h2>${plugin.name}</h2>
                <div class="meta">${TRANSLATIONS[currentLang].author.replace('{author}', plugin.author)} | ${TRANSLATIONS[currentLang].version.replace('{version}', plugin.version)}</div>
            </div>
        </div>
        <div class="readme-content">
            <p>${plugin.description}</p>
            <div style="margin-top: 1.5rem;">
                <h4 style="color: var(--primary-color);">Features:</h4>
                <ul style="margin-left: 1.5rem; margin-top: 0.5rem;">
                    <li>Custom anime provider</li>
                    <li>Automatic updates</li>
                    <li>Secure execution</li>
                </ul>
            </div>
            <div style="margin-top: 2rem; display: flex; gap: 1rem;">
                <a href="#" class="btn btn-primary" onclick="installPlugin('${plugin.id}')">${TRANSLATIONS[currentLang]['download-btn']}</a>
            </div>
        </div>
    `;
    
    modal.style.display = "block";
}

async function fetchPlugins() {
    const grid = document.getElementById('plugins-grid');
    const loader = document.getElementById('loader');
    
    try {
        // Mock data for demo
        pluginsData = [
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
        renderPlugins();
    } catch (err) {
        console.error("Failed to fetch plugins", err);
        loader.innerHTML = "Error loading plugins.";
    }
}

function renderPlugins() {
    const grid = document.getElementById('plugins-grid');
    grid.innerHTML = '';
    
    pluginsData.forEach(plugin => {
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
                <a href="#" class="btn btn-outline" onclick="showPluginDetails('${plugin.id}')">${TRANSLATIONS[currentLang]['details-btn']}</a>
            </div>
        `;
        grid.appendChild(card);
    });
}

function installPlugin(id) {
    alert(`To install this plugin, copy the URL and use the load plugin option in the settings menu of Weeb CLI.\n\nURL: https://raw.githubusercontent.com/ewgsta/weeb-cli/main/plugins/${id}.weeb`);
}
