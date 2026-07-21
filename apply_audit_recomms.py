import os
import glob
import re

def run_audits_and_fixes():
    html_files = glob.glob('**/*.html', recursive=True)
    count_of_changes = 0

    for filepath in html_files:
        if filepath.startswith('archive'):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        orig = html

        # 1. Remplacer "Création du cabinet" par "Création de l'organisme de formation" dans la timeline (about.html)
        html = html.replace("Création du cabinet à Marseille", "Création de l'organisme de formation à Marseille")

        # 2. Encadrer "déploiement" par "déploiement pédagogique" où c'est ambigu (ex:about.html, index.html)
        html = html.replace("déploiement IA", "déploiement pédagogique de l'IA")
        html = html.replace("déploiements techniques", "déploiements pédagogiques")
        html = html.replace("réussite absolue de nos déploiements", "réussite absolue de nos déploiements pédagogiques")

        # 3. Corriger timeline 2023 -> 2025 dans about.html
        if os.path.basename(filepath) == 'about.html':
            html = html.replace('"foundingDate": "2023"', '"foundingDate": "2025"')
            html = html.replace('<div class="timeline-year">2023</div>', '<div class="timeline-year">2025</div>')

        # 4. Vérifier mentions légales : s'assurer que NDA, SIREN, DREETS (Préfet PACA) et APE sont visibles dans mentions-legales.html & footer
        if os.path.basename(filepath) == 'mentions-legales.html':
            if "Déclaration d'activité" not in html:
                mentions_patch = """                        <strong>Raison sociale :</strong> BABYLONE 42 SAS<br>
                        <strong>Forme juridique :</strong> SAS, société par actions simplifiée au capital social de 1 000 €<br>
                        <strong>Siège social :</strong> 79 rue de la Maurelle, 13013 Marseille, France<br>
                        <strong>SIREN :</strong> 992 220 707<br>
                        <strong>SIRET :</strong> 992 220 707 00010<br>
                        <strong>TVA Intracommunautaire :</strong> FR47992220707<br>
                        <strong>Code NAF / APE :</strong> 8559A (Formation continue d'adultes)<br>
                        <strong>Déclaration d'activité (NDA) :</strong> Enregistrée sous le n° 93132513713 auprès du Préfet de région PACA (DREETS). Cet enregistrement ne vaut pas agrément de l'État.<br>
                        <strong>Directeur de la publication :</strong> Eulalio TORRES<br>
                        <strong>Contact :</strong> contact@babylone42.fr | +33 0 7 73 60 98 49"""
                html = re.sub(r'<strong>Raison sociale :</strong> BABYLONE 42 SAS.*?<strong>Contact :</strong>', mentions_patch, html, flags=re.DOTALL)

        if html != orig:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            count_of_changes += 1
            print(f"Audited & Updated {filepath}")

    print(f"Completed audit changes in {count_of_changes} files.")

run_audits_and_fixes()
