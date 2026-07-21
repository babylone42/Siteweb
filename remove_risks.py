import glob

def replace_in_file(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

# Update about.html
replace_in_file('about.html', 'coordination entre une agence et un organisme de formation.', 'coordination entre un prestataire et un organisme de formation.')
replace_in_file('about.html', 'conseil stratégique IA', 'formation IA')

# Update index.html and index1.html
for f in ['index.html', 'index1.html']:
    replace_in_file(f, 'une agence technique et un organisme', 'un prestataire technique et un organisme')
    replace_in_file(f, 'conseil stratégique IA', 'formation IA')
    replace_in_file(f, 'Nous ne sommes pas une agence classique', 'Nous ne sommes pas un prestataire classique')
    replace_in_file(f, 'au développement (Python)', 'à la programmation (Python)')

# Update solution-chatbots.html
replace_in_file('solution-chatbots.html', '<h4>Développement &amp; Tests</h4>', '<h4>Mise en place &amp; Tests</h4>')
replace_in_file('solution-chatbots.html', '<h4>Développement & Tests</h4>', '<h4>Mise en place & Tests</h4>')
