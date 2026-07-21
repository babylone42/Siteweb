import os
import re
import glob

# 1. Update index.html specific texts
index_path = 'index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Title
content = content.replace(
    '<title>Babylone42 | Partenaire IA & Automatisation pour Entreprises</title>',
    '<title>Babylone42 | Formation IA & Solutions d\'Intelligence Artificielle</title>'
)

# Meta
content = content.replace(
    'content="Déployez des solutions IA concrètes (Copilots, Chatbots, Automatisation) et formez vos équipes avec Babylone42. Expertise technique et pédagogique à Marseille et en France."',
    'content="Organisme de formation spécialisé en IA, data et nouvelles technologies. Formez vos équipes et déployez des solutions d\'intelligence artificielle concrètes avec Babylone42 à Marseille et en France."'
)

# Hero H1
content = content.replace(
    '<h1>Transformez votre entreprise grâce à <span class="highlight">l\'IA opérationnelle</span></h1>',
    '<h1>Formez vos équipes et transformez votre entreprise grâce à <span class="highlight">l\'IA opérationnelle</span></h1>'
)

# Hero P
content = re.sub(
    r'Nous déployons des solutions d\'intelligence artificielle concrètes qui\s*automatisent\s*vos tâches et augmentent immédiatement la productivité de vos équipes\.',
    'Nous formons vos collaborateurs et déployons des solutions d\'intelligence artificielle concrètes qui automatisent vos tâches et augmentent immédiatement la productivité de vos équipes.',
    content
)

# RISQUE 4
content = re.sub(
    r'Babylone 42 vous accompagne pour franchir un cap décisif dans votre croissance\. Nous concevons des\s*solutions sur mesure qui s\'intègrent organiquement à vos processus existants\.',
    'Babylone 42 vous accompagne pour franchir un cap décisif dans votre transformation numérique. Nous formons vos équipes et mettons en place des outils IA adaptés à vos processus existants, en combinant expertise technique et pédagogie.',
    content
)

# RISQUE 5
old_steps = """                    <div class="service-card">
                        <i class="fas fa-search service-icon"></i>
                        <h4>1. Diagnostic IA</h4>
                        <p>Audit de vos processus, identification des gisements de
                            productivité.</p>
                    </div>

                    <div class="step-arrow">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div class="service-card">
                        <i class="fas fa-network-wired service-icon"></i>
                        <h4>2. Déploiement</h4>
                        <p>Mise en œuvre de solutions IA robustes et sécurisées.</p>
                    </div>

                    <div class="step-arrow">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div class="service-card">
                        <i class="fas fa-plug service-icon"></i>
                        <h4>3. Intégration</h4>
                        <p>Connexion fluide à vos CRM, ERP et bases de données.</p>
                    </div>"""

new_steps = """                    <div class="service-card">
                        <i class="fas fa-search service-icon"></i>
                        <h4>1. Diagnostic IA</h4>
                        <p>Audit de vos processus et identification des besoins</p>
                    </div>

                    <div class="step-arrow">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div class="service-card">
                        <i class="fas fa-network-wired service-icon"></i>
                        <h4>2. Déploiement</h4>
                        <p>Mise en place des outils IA adaptés</p>
                    </div>

                    <div class="step-arrow">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div class="service-card">
                        <i class="fas fa-plug service-icon"></i>
                        <h4>3. Intégration</h4>
                        <p>Connexion fluide à vos systèmes existants</p>
                    </div>

                    <div class="step-arrow">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div class="service-card">
                        <i class="fas fa-graduation-cap service-icon"></i>
                        <h4>4. Formation & Autonomie</h4>
                        <p>Vos équipes sont formées pour maîtriser et faire évoluer ces outils en toute autonomie</p>
                    </div>"""

content = content.replace(old_steps, new_steps)

# RISQUE 6
content = content.replace(
    'Nous ne sommes pas une agence classique.',
    'Nous ne sommes pas un prestataire classique.'
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update Footer/Links across all HTML files
# We replace >Audit & Conseil< with >Diagnostic IA & Accompagnement<
# We also find 'Audit & Conseil IA' in solution-audit.html just in case.

html_files = glob.glob('**/*.html', recursive=True)
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        updated = False
        if '>Audit & Conseil<' in file_content:
            file_content = file_content.replace('>Audit & Conseil<', '>Diagnostic IA & Accompagnement<')
            updated = True
        
        if file.endswith('solution-audit.html') and '>Audit & Conseil IA<' in file_content:
            file_content = file_content.replace('>Audit & Conseil IA<', '>Diagnostic IA & Accompagnement<')
            updated = True
            
        if updated:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(file_content)
            print(f"Updated {file}")
    except Exception as e:
        print(f"Failed to update {file}: {e}")

print("All updates applied!")
