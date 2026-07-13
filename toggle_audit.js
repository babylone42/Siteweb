// Script pour activer/désactiver le mode Audit Qualiopi sur le site web
// Usage : 'node toggle_audit.js enable' pour activer le mode audit (masquer les formations)
//         'node toggle_audit.js disable' pour tout remettre en ligne

const fs = require('fs');
const path = require('path');

const action = process.argv[2];
if (action !== 'enable' && action !== 'disable') {
    console.error("Usage: node toggle_audit.js [enable|disable]");
    process.exit(1);
}

const isAudit = (action === 'enable');

// 1. Liste des fichiers HTML à modifier à la racine
const ROOT_FILES = [
    'about.html',
    'accessibilite.html',
    'articles.html',
    'calendrier-formations.html',
    'cgv.html',
    'contact-page.html',
    'cookies.html',
    'faq.html',
    'formation-genai.html',
    'indicateurs-resultats.html',
    'interlocuteurs.html',
    'mentions-legales.html',
    'politique-confidentialite.html',
    'solution-audit.html',
    'solution-automation.html',
    'solution-chatbots.html',
    'solution-copilots.html'
];

// Classes CSS d'audit à injecter dans le <head>
const STYLE_BLOCK = `    <style id="audit-styles">
        .link-disabled {
            opacity: 0.4 !important;
            cursor: not-allowed !important;
            pointer-events: none !important;
            text-decoration: line-through !important;
        }
        a.link-disabled {
            pointer-events: none !important;
        }
        .card-disabled {
            opacity: 0.45 !important;
            cursor: not-allowed !important;
            filter: grayscale(80%) !important;
            pointer-events: none !important;
        }
    </style>
</head>`;

ROOT_FILES.forEach(fileName => {
    const filePath = path.join(__dirname, fileName);
    if (!fs.existsSync(filePath)) return;

    let content = fs.readFileSync(filePath, 'utf8');

    if (isAudit) {
        // --- 1. Injection des styles d'audit dans le <head> ---
        if (!content.includes('id="audit-styles"')) {
            content = content.replace('</head>', STYLE_BLOCK);
        }

        // --- 2. Neutralisation des formations dans les menus / footers ---
        // Remplacer les liens vers les autres formations par des liens désactivés
        // Cabinets d'Avocats
        content = content.replace(/href="Avocats\/brochure_generale_avocats\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/Avocats\/brochure_generale_avocats\.html"/g, 'href="#" class="link-disabled"');
        
        // Expertise Comptable & Audit
        content = content.replace(/href="Comptables\/brochure_generale_comptables\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/Comptables\/brochure_generale_comptables\.html"/g, 'href="#" class="link-disabled"');

        // Vidéo IA Pro
        content = content.replace(/href="formation-video-ia-pro\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/formation-video-ia-pro\.html"/g, 'href="#" class="link-disabled"');

        // Jupyter
        content = content.replace(/href="formation-jupyter\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/formation-jupyter\.html"/g, 'href="#" class="link-disabled"');

        // Python
        content = content.replace(/href="formation-python\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/formation-python\.html"/g, 'href="#" class="link-disabled"');

        // Machine Learning
        content = content.replace(/href="formation-ml\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/formation-ml\.html"/g, 'href="#" class="link-disabled"');

        // Deep Learning
        content = content.replace(/href="formation-dl\.html"/g, 'href="#" class="link-disabled"');
        content = content.replace(/href="\.\.\/formation-dl\.html"/g, 'href="#" class="link-disabled"');

    } else {
        // --- 1. Retrait des styles d'audit ---
        content = content.replace(/<style id="audit-styles">[\s\S]*?<\/style>\s*<\/head>/g, '</head>');

        // --- 2. Restauration des liens d'origine ---
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Cabinets d'Avocats<\/a>/g, 'href="Avocats/brochure_generale_avocats.html"$1>Cabinets d\'Avocats</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Expertise Comptable & Audit<\/a>/g, 'href="Comptables/brochure_generale_comptables.html"$1>Expertise Comptable & Audit</a>');

        content = content.replace(/href="#" class="link-disabled">Vidéo IA Pro<\/a>/g, 'href="formation-video-ia-pro.html">Vidéo IA Pro</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Vidéo IA Pro<\/a>/g, 'href="formation-video-ia-pro.html"$1>Vidéo IA Pro</a>');

        content = content.replace(/href="#" class="link-disabled">Jupyter<\/a>/g, 'href="formation-jupyter.html">Jupyter</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Jupyter<\/a>/g, 'href="formation-jupyter.html"$1>Jupyter</a>');

        content = content.replace(/href="#" class="link-disabled">Python<\/a>/g, 'href="formation-python.html">Python</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Python<\/a>/g, 'href="formation-python.html"$1>Python</a>');

        content = content.replace(/href="#" class="link-disabled">Machine Learning<\/a>/g, 'href="formation-ml.html">Machine Learning</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Machine Learning<\/a>/g, 'href="formation-ml.html"$1>Machine Learning</a>');

        content = content.replace(/href="#" class="link-disabled">Deep Learning<\/a>/g, 'href="formation-dl.html">Deep Learning</a>');
        content = content.replace(/href="#" class="link-disabled"( style="padding-left:\s*1.5rem;")?>Deep Learning<\/a>/g, 'href="formation-dl.html"$1>Deep Learning</a>');
    }

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Processed ${fileName}`);
});

// 3. Gestion spécifique de calendrier-formations.html
const calPath = path.join(__dirname, 'calendrier-formations.html');
if (fs.existsSync(calPath)) {
    let calContent = fs.readFileSync(calPath, 'utf8');
    if (isAudit) {
        // Sauvegarder calendrier original s'il n'existe pas déjà
        if (!fs.existsSync(path.join(__dirname, 'calendrier-formations-original.html'))) {
            fs.writeFileSync(path.join(__dirname, 'calendrier-formations-original.html'), calContent, 'utf8');
        }
        
        // Remplacer les boutons filtres inactifs de la sidebar par du grisé
        calContent = calContent.replace(/<button class="filter-btn" data-filter="avocats">Cabinets d'Avocats<\/button>/g, '<button class="filter-btn link-disabled" data-filter="avocats" style="pointer-events:none;">Cabinets d\'Avocats</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="comptables">Expertise Comptable<\/button>/g, '<button class="filter-btn link-disabled" data-filter="comptables" style="pointer-events:none;">Expertise Comptable</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="video_ia_pro">Vidéo IA Pro<\/button>/g, '<button class="filter-btn link-disabled" data-filter="video_ia_pro" style="pointer-events:none;">Vidéo IA Pro</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="python">Python pour la Data<\/button>/g, '<button class="filter-btn link-disabled" data-filter="python" style="pointer-events:none;">Python pour la Data</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="machine_learning">Machine Learning<\/button>/g, '<button class="filter-btn link-disabled" data-filter="machine_learning" style="pointer-events:none;">Machine Learning</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="deep_learning">Deep Learning<\/button>/g, '<button class="filter-btn link-disabled" data-filter="deep_learning" style="pointer-events:none;">Deep Learning</button>');
        calContent = calContent.replace(/<button class="filter-btn" data-filter="jupyter">Jupyter Notebook<\/button>/g, '<button class="filter-btn link-disabled" data-filter="jupyter" style="pointer-events:none;">Jupyter Notebook</button>');

        // Griser ou masquer les items de cours qui ne sont pas data-type="prompting"
        calContent = calContent.replace(/<div class="course-item([^"]*)" data-type="(?!prompting)([a-zA-Z0-9_-]+)"/g, '<div class="course-item$1 card-disabled" data-type="$2" style="pointer-events:none;"');
        
    } else {
        // Restaurer le calendrier d'origine s'il a été sauvegardé
        const calOrigPath = path.join(__dirname, 'calendrier-formations-original.html');
        if (fs.existsSync(calOrigPath)) {
            const originalCal = fs.readFileSync(calOrigPath, 'utf8');
            fs.writeFileSync(calPath, originalCal, 'utf8');
            console.log("Restored original calendrier-formations.html");
        }
    }
    fs.writeFileSync(calPath, calContent, 'utf8');
}

console.log(`\nAudit mode successfully ${action}d!`);
