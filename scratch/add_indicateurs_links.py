import os
import re

root_dir = r"c:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine relative path
    rel_depth = os.path.relpath(os.path.dirname(filepath), root_dir)
    if rel_depth == '.':
        href = "indicateurs-resultats.html"
    else:
        # One level deep (Avocats, Comptables)
        href = "../indicateurs-resultats.html"

    # We want to insert the link to indicateurs-resultats.html inside <div class="legal-links">
    # E.g.: <div class="legal-links"><a href="cgv.html">CGV</a>...
    # We can search for <div class="legal-links"> and append the link as the first or last item inside it.
    # Let's check if the link is already there
    if href in content:
        print(f"Skipping {filepath} (link already present)")
        return

    # Let's find `<div class="legal-links">`
    pattern = r'(<div class="legal-links">)'
    if re.search(pattern, content):
        new_content = re.sub(
            pattern,
            rf'\1<a href="{href}">Indicateurs de Résultats</a>',
            content,
            count=1
        )
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"No legal-links found in {filepath}")

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.html'):
            # Skip indicateurs-resultats.html itself
            if filename == 'indicateurs-resultats.html':
                continue
            filepath = os.path.join(dirpath, filename)
            process_file(filepath)
