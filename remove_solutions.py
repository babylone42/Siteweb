import os
import glob
import re

def remove_solutions_from_html():
    html_files = glob.glob('**/*.html', recursive=True)
    count = 0
    for file in html_files:
        if file.startswith('archive'):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        original_html = html
        
        # 1. Remove nav dropdown "Solutions IA"
        # We find <li class="dropdown">...<a href="...#solutions">Solutions IA...</ul>\s*</li>
        sol_nav_pattern = re.compile(r'<li class="dropdown">\s*<a [^>]*>Solutions IA.*?</ul>\s*</li>', re.DOTALL)
        html = sol_nav_pattern.sub('', html)
        
        # 2. Remove footer column "Solutions IA"
        # We find <!-- Column 3: Solutions -->...</ul>\s*</div>
        sol_footer_pattern = re.compile(r'<!-- Column 3: Solutions -->\s*<div class="footer-col">\s*<h4 class="footer-title">Solutions IA</h4>.*?</ul>\s*</div>', re.DOTALL)
        html = sol_footer_pattern.sub('', html)
        
        # 3. Clean index.html and index1.html specific blocks
        if os.path.basename(file) in ['index.html', 'index1.html']:
            # Remove from hero CTA
            html = re.sub(r'<a href="[^"]*#solutions" class="btn btn-secondary">Solutions IA</a>\s*', '', html)
            # Remove the whole <section id="solutions">
            html = re.sub(r'<section id="solutions".*?</section>', '', html, flags=re.DOTALL)
            
        # 4. Clean contact-page.html
        if os.path.basename(file) == 'contact-page.html':
            # Hide the toggle buttons
            html = re.sub(r'<div class="toggle-buttons">.*?</div>', 
                          '<div class="toggle-buttons" style="display:none;"><button type="button" class="btn-toggle active" data-type="formations">Formations</button></div>', 
                          html, flags=re.DOTALL)
            
            # Hide options-solutions and remove required
            html = html.replace('id="options-solutions"', 'id="options-solutions" style="display:none;"')
            
            # Make options-formations visible by default
            html = html.replace('id="options-formations" class="form-group dynamic-options hidden"', 'id="options-formations" class="form-group dynamic-options"')
            html = html.replace('class="form-group dynamic-options hidden" id="options-formations"', 'class="form-group dynamic-options" id="options-formations"')

        if html != original_html:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(html)
            count += 1
            print(f"Cleaned {file}")
            
    print(f"Cleaned {count} files")

remove_solutions_from_html()
