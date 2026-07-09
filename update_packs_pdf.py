import os
import re

FILES = [
    {"path": "Avocats/pack0_ia_literacy_avocats.html", "ref": "REF-2026-AVOC-000"},
    {"path": "Avocats/pack1_ia_generative_avocats.html", "ref": "REF-2026-AVOC-001"},
    {"path": "Avocats/pack2_prompt_engineering_avocats.html", "ref": "REF-2026-AVOC-002"},
    {"path": "Avocats/pack3_ia_secret_pro_avocats.html", "ref": "REF-2026-AVOC-003"},
    {"path": "Comptables/pack0_ia_literacy_comptables.html", "ref": "REF-2026-COMPT-000"},
    {"path": "Comptables/pack1_ia_generative_comptables.html", "ref": "REF-2026-COMPT-001"},
    {"path": "Comptables/pack2_prompt_engineering_comptables.html", "ref": "REF-2026-COMPT-002"},
    {"path": "Comptables/pack3_ia_secret_pro_comptables.html", "ref": "REF-2026-COMPT-003"}
]

for f in FILES:
    path = os.path.join(r'C:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb', f['path'])
    if not os.path.exists(path):
        continue
        
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    prefix = "../"
    
    btn_container_regex = r'(<div class="cta-buttons-wrap">)'
    if re.search(btn_container_regex, content):
        pdf_snippet = f'''<p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem; text-align: center;">
                            <i class="fas fa-file-pdf" style="color: var(--primary-color);"></i>
                            <a href="{prefix}programmes/{f["ref"]}.pdf" style="color: var(--primary-color); text-decoration: underline;">Télécharger le programme complet (PDF)</a>
                            <br>Réf. : {f["ref"]} &nbsp;|&nbsp; Dernière mise à jour : juillet 2026
                        </p>
                        '''
        if "Télécharger le programme complet (PDF)" not in content:
            content = re.sub(btn_container_regex, pdf_snippet + r'\1', content, count=1)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Injected PDF link in {f['path']}")
