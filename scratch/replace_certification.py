import os
import re

FILES = [
    "Avocats/pack0_ia_literacy_avocats.html",
    "Avocats/pack1_ia_generative_avocats.html",
    "Avocats/pack2_prompt_engineering_avocats.html",
    "Avocats/pack3_ia_secret_pro_avocats.html",
    "Comptables/pack0_ia_literacy_comptables.html",
    "Comptables/pack1_ia_generative_comptables.html",
    "Comptables/pack2_prompt_engineering_comptables.html",
    "Comptables/pack3_ia_secret_pro_comptables.html"
]

target_title_regex = r'<h4 style="margin-bottom: 5px; color: var\(--primary\);">Micro-certification incluse</h4>'
new_title = '<h4 style="margin-bottom: 5px; color: var(--primary);">Attestation de réussite incluse</h4>'

target_p_regex = r'<p style="font-size: 0.9em; margin: 0;">Obtention d\'un <strong>Badge numérique</strong> exclusif Babylone 42 en fin de formation, validant les acquis et la maîtrise de l\'IA abordée dans ce pack\.</p>'
new_p = '<p style="font-size: 0.9em; margin: 0;">Remise d\'une <strong>Attestation de réussite</strong> officielle Babylone 42 en fin de formation, validant les acquis et la maîtrise des compétences professionnelles évaluées.</p>'

base_dir = r"C:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb"

for rel_path in FILES:
    file_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(file_path):
        print(f"File not found: {rel_path}")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False
    
    # Check for title replacement (normal style)
    if re.search(target_title_regex, content):
        content = re.sub(target_title_regex, new_title, content)
        modified = True
    else:
        # Try with double dashes inside var(--primary) just in case
        alt_regex = r'<h4 style="margin-bottom: 5px; color: var\(--primary-color\);">Micro-certification incluse</h4>'
        if re.search(alt_regex, content):
            content = re.sub(alt_regex, '<h4 style="margin-bottom: 5px; color: var(--primary-color);">Attestation de réussite incluse</h4>', content)
            modified = True
            
    # Check for text replacement
    if re.search(target_p_regex, content):
        content = re.sub(target_p_regex, new_p, content)
        modified = True
        
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {rel_path}")
    else:
        print(f"No changes made to {rel_path}")
