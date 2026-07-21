import os
import glob
import re

def fix_contact_form_in_index():
    for filename in ['index.html', 'index1.html']:
        if not os.path.exists(filename):
            continue
            
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Update Badge text above "Passez à l'action" if still Diagnostic IA
        html = html.replace('Diagnostic IA\n                        Gratuit', 'Contact')
        html = html.replace('Diagnostic IA Gratuit', 'Contact')

        # 2. Hide or replace service-toggle
        html = re.sub(
            r'<div class="form-group service-toggle">.*?</div>\s*</div>',
            '<div class="form-group service-toggle" style="display:none;"><div class="toggle-buttons"><button type="button" class="btn-toggle active" data-type="formations">Formations</button></div></div>',
            html,
            flags=re.DOTALL
        )

        # 3. Hide options-solutions completely
        sol_options_pattern = re.compile(r'<div class="form-group dynamic-options" id="options-solutions">.*?</div>\s*</div>', re.DOTALL)
        html = sol_options_pattern.sub('<div class="form-group dynamic-options" id="options-solutions" style="display:none;"></div>', html)

        # 4. Show options-formations by default (remove hidden class)
        html = html.replace('class="form-group dynamic-options hidden" id="options-formations"', 'class="form-group dynamic-options" id="options-formations"')
        html = html.replace('id="options-formations" class="form-group dynamic-options hidden"', 'id="options-formations" class="form-group dynamic-options"')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated contact form in {filename}")

fix_contact_form_in_index()
