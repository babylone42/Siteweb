import os
import glob
import re

def update_copy_and_compliance():
    # 1. Update index.html
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            index_html = f.read()

        # Update 150+ Clients Accompagnés -> 150+ Stagiaires Accompagnés
        index_html = index_html.replace("<p>Clients Accompagnés</p>", "<p>Stagiaires Accompagnés</p>")
        index_html = index_html.replace("<p>Clients accompagnés</p>", "<p>Stagiaires accompagnés</p>")
        index_html = index_html.replace("Clients Accompagnés", "Stagiaires Accompagnés")
        index_html = index_html.replace("Clients accompagnés", "Stagiaires accompagnés")

        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("Updated index.html hero stats")

    # 2. Update about.html
    if os.path.exists('about.html'):
        with open('about.html', 'r', encoding='utf-8') as f:
            about_html = f.read()

        # SEO meta & Title
        about_html = about_html.replace(
            "<title>À Propos de Babylone42 | Cabinet IA & Automatisation à Marseille</title>",
            "<title>À Propos de Babylone42 | Organisme de Formation IA & Data à Marseille</title>"
        )
        about_html = about_html.replace(
            'content="Babylone42 est un cabinet spécialisé en Intelligence Artificielle et automatisation basé à Marseille.',
            'content="Babylone42 est un organisme de formation spécialisé en Intelligence Artificielle et Data basé à Marseille.'
        )
        about_html = about_html.replace(
            'content="Babylone42, cabinet IA Marseille,',
            'content="Babylone42, organisme de formation IA Marseille,'
        )
        about_html = about_html.replace(
            'property="og:title" content="À Propos de Babylone42 | Cabinet IA & Automatisation à Marseille"',
            'property="og:title" content="À Propos de Babylone42 | Organisme de Formation IA & Data à Marseille"'
        )
        about_html = about_html.replace(
            'name="twitter:title" content="À Propos de Babylone42 | Cabinet IA & Automatisation"',
            'name="twitter:title" content="À Propos de Babylone42 | Organisme de Formation IA & Data"'
        )

        # Body text replacement (Cabinet -> Organisme de formation)
        about_html = about_html.replace(
            "Babylone42 est un cabinet spécialisé en Intelligence Artificielle et automatisation, basé à\n                            Marseille.",
            "Babylone42 est un organisme de formation spécialisé en Intelligence Artificielle et Data, basé à\n                            Marseille."
        )
        about_html = about_html.replace(
            "Babylone42 est un cabinet spécialisé en Intelligence Artificielle et automatisation, basé à Marseille.",
            "Babylone42 est un organisme de formation spécialisé en Intelligence Artificielle et Data, basé à Marseille."
        )

        # Hero stats update in about.html:
        # In about, hero, enleve 150+ Clients accompagnees et 50+ workflos Ai deployees, et met <3 mois ROI
        # Wait, the about.html has:
        # <div class="hero-stat-row">
        #     <div class="hero-stat-item">
        #         <strong>150+</strong>
        #         <span>Clients accompagnés</span>
        #     </div>
        #     <div class="hero-stat-item">
        #         <strong>50+</strong>
        #         <span>Workflows IA déployés</span>
        #     </div>
        #     <div class="hero-stat-item">
        #         <strong>&lt; 3 mois</strong>
        #         <span>ROI constaté</span>
        #     </div>
        # </div>
        # We need to only have '< 3 mois ROI constaté' or similar?
        # Let's replace the whole <div class="hero-stat-row">...</div> with a row showing "< 3 mois ROI constaté"
        old_stat_row = """                        <div class="hero-stat-row">
                            <div class="hero-stat-item">
                                <strong>150+</strong>
                                <span>Clients accompagnés</span>
                            </div>
                            <div class="hero-stat-item">
                                <strong>50+</strong>
                                <span>Workflows IA déployés</span>
                            </div>
                            <div class="hero-stat-item">
                                <strong>&lt; 3 mois</strong>
                                <span>ROI constaté</span>
                            </div>
                        </div>"""

        new_stat_row = """                        <div class="hero-stat-row">
                            <div class="hero-stat-item">
                                <strong>&lt; 3 mois</strong>
                                <span>ROI moyen constaté après formation</span>
                            </div>
                        </div>"""
        
        if old_stat_row in about_html:
            about_html = about_html.replace(old_stat_row, new_stat_row)
        else:
            # Let's also do a more flexible replacement in case of spacing differences
            pattern = re.compile(r'<div class="hero-stat-row">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
            # Just to be safe, replace the exact strings
            about_html = re.sub(r'<strong>150\+</strong>\s*<span>Clients accompagnés</span>', '', about_html)
            about_html = re.sub(r'<strong>50\+</strong>\s*<span>Workflows IA déployés</span>', '', about_html)
            # Remove any empty stat items
            about_html = about_html.replace('<div class="hero-stat-item">\n                                \n                                \n                            </div>', '')
            about_html = about_html.replace('<div class="hero-stat-item">\n                            \n                            \n                        </div>', '')

        with open('about.html', 'w', encoding='utf-8') as f:
            f.write(about_html)
        print("Updated about.html copy")

    # 3. Clean up the footer text descriptif in all HTML files:
    # Replace: "Babylone42 donne le pouvoir aux équipes de transformer des données brutes en informations claires grâce à l'IA."
    # With: "Babylone42 forme vos équipes à exploiter le potentiel de l'IA et de la data pour gagner en autonomie et en productivité."
    # 4. Clean up "Nous ne sommes pas un prestataire classique" -> "Nous ne sommes pas un simple intervenant extérieur"
    html_files = glob.glob('**/*.html', recursive=True)
    footer_old = "Babylone42 donne le pouvoir aux équipes de transformer des données brutes en informations claires grâce à l'IA."
    footer_new = "Babylone42 forme vos équipes à exploiter le potentiel de l'IA et de la data pour gagner en autonomie et en productivité."
    
    prestataire_old = "Nous ne sommes pas un prestataire classique"
    prestataire_new = "Nous ne sommes pas un simple intervenant extérieur"

    for filepath in html_files:
        if filepath.startswith('archive'):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        content = content.replace(footer_old, footer_new)
        content = content.replace(prestataire_old, prestataire_new)

        if content != orig:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated footer/prestataire copy in {filepath}")

update_copy_and_compliance()
