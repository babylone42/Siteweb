import os
import glob
import re

# We want to match the whole <li> block for Solutions and Formations.
# The <li> starts with <li class="dropdown"> and ends with </li>
# We know the inner content contains 'Solutions IA <i' or 'Formations <i'

def swap_menu_items(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the nav-links block
    nav_match = re.search(r'(<ul class="nav-links">)(.*?)(</ul>\s*<div class="hamburger">)', html, re.DOTALL)
    if not nav_match:
        return False
        
    nav_inner = nav_match.group(2)
    
    # Within nav_inner, find the Solutions block and Formations block
    # It looks like:
    # <li class="dropdown"> ... Solutions IA ... </ul>\s*</li>
    solutions_pattern = re.compile(r'(<li class="dropdown">\s*<a [^>]*>Solutions IA.*?</ul>\s*</li>)', re.DOTALL)
    formations_pattern = re.compile(r'(<li class="dropdown">\s*<a [^>]*>Formations.*?</ul>\s*</li>)', re.DOTALL)
    
    sol_match = solutions_pattern.search(nav_inner)
    form_match = formations_pattern.search(nav_inner)
    
    if sol_match and form_match:
        sol_block = sol_match.group(1)
        form_block = form_match.group(1)
        
        # Are they adjacent? Usually it's sol_block then form_block
        # We can just string replace in nav_inner.
        # But wait, they might have whitespace between them.
        
        # Let's replace the whole sol_block + whitespace + form_block
        # with form_block + whitespace + sol_block
        
        # Find their exact positions in nav_inner
        sol_start = sol_match.start()
        sol_end = sol_match.end()
        form_start = form_match.start()
        form_end = form_match.end()
        
        if sol_end <= form_start:
            # Solutions is before Formations
            between = nav_inner[sol_end:form_start]
            new_nav_inner = nav_inner[:sol_start] + form_block + between + sol_block + nav_inner[form_end:]
            
            new_html = html.replace(nav_inner, new_nav_inner)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            return True
        elif form_end <= sol_start:
            # Already Formations before Solutions
            pass
            
    return False

html_files = glob.glob('**/*.html', recursive=True)
count = 0
for file in html_files:
    if swap_menu_items(file):
        count += 1
        print(f"Swapped in {file}")

print(f"Total swapped: {count}")
