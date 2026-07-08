const fs = require('fs');
const path = require('path');

const indexHtml = fs.readFileSync('index.html', 'utf8');

// Extract nav
const navMatch = indexHtml.match(/(<nav class="navbar">[\s\S]*?<\/nav>)/);
const headerPart = navMatch ? navMatch[1] : null;

// Extract footer
const footerMatch = indexHtml.match(/(<footer class="mega-footer">[\s\S]*?<\/footer>)/);
const footerPart = footerMatch ? footerMatch[1] : null;

if (!headerPart || !footerPart) {
    console.error("Could not find header or footer in index.html");
    process.exit(1);
}

function getHtmlFiles(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat && stat.isDirectory()) {
            if (file !== 'node_modules' && file !== '.git' && file !== 'scratch' && file !== 'pre-launch-site') {
                results = results.concat(getHtmlFiles(filePath));
            }
        } else if (file.endsWith('.html') && filePath !== path.join(__dirname, 'index.html')) {
            results.push(filePath);
        }
    });
    return results;
}

const htmlFiles = getHtmlFiles(__dirname);
let updatedCount = 0;

htmlFiles.forEach(filePath => {
    const relativePath = path.relative(__dirname, filePath);
    const depth = relativePath.split(path.sep).length - 1;
    const prefix = '../'.repeat(depth);

    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    // Adjust header and footer links prefix for subdirectories
    let adjustedHeader = headerPart;
    let adjustedFooter = footerPart;

    if (depth > 0) {
        // Find href="xxx" and prefix them if they don't start with http, mailto, tel, # or already contain ../
        const adjustLinks = (html) => {
            return html.replace(/href="([^"#:][^"]*)"/g, (match, p1) => {
                if (p1.startsWith('http') || p1.startsWith('mailto') || p1.startsWith('tel') || p1.startsWith('#') || p1.startsWith('../')) {
                    return match;
                }
                return `href="${prefix}${p1}"`;
            });
        };
        adjustedHeader = adjustLinks(headerPart);
        adjustedFooter = adjustLinks(footerPart);
    }

    // Replace nav
    if (content.match(/<nav class="navbar">[\s\S]*?<\/nav>/)) {
        content = content.replace(/<nav class="navbar">[\s\S]*?<\/nav>/, adjustedHeader);
        modified = true;
    }

    // Replace footer
    if (content.match(/<footer\b[^>]*>[\s\S]*?<\/footer>/)) {
        content = content.replace(/<footer\b[^>]*>[\s\S]*?<\/footer>/, adjustedFooter);
        modified = true;
    }

    if (modified) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated ${relativePath}`);
        updatedCount++;
    }
});

// Create calendrier-formations.html
if (!fs.existsSync('calendrier-formations.html')) {
    const template = `<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calendrier des Formations | Babylone42</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css?v=5">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
${headerPart}

    <main class="page-content" style="padding-top: 120px; padding-bottom: 80px; min-height: 60vh;">
        <div class="container section-padding">
            <h1 class="section-title" style="margin-bottom: 2rem;">Calendrier des formations</h1>
            <div style="background: rgba(255, 255, 255, 0.03); padding: 4rem 2rem; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.1); text-align: center;">
                <p style="color: #94a3b8; font-size: 1.1rem;">Page en cours de construction. Le calendrier complet sera bientôt affiché ici.</p>
            </div>
        </div>
    </main>

${footerPart}
    <script src="script.js"></script>
</body>
</html>`;
    fs.writeFileSync('calendrier-formations.html', template, 'utf8');
    console.log("Created calendrier-formations.html");
}

console.log(`\nSuccessfully updated ${updatedCount} HTML files!`);
