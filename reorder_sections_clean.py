import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Modify descriptions in solutions to include 'formation'
html = html.replace(
    'Des assistants virtuels intelligents disponibles en continu pour r&eacute;pondre aux questions, qualifier les leads et r&eacute;soudre les probl&egrave;mes r&eacute;currents.',
    'Formation et accompagnement &agrave; la cr&eacute;ation d\'assistants virtuels intelligents disponibles en continu pour r&eacute;pondre aux questions et automatiser votre support.'
)

html = html.replace(
    'Des assistants virtuels intelligents disponibles en continu pour répondre aux questions, qualifier les leads et résoudre les problèmes récurrents.',
    'Formation et accompagnement à la création d\'assistants virtuels intelligents disponibles en continu pour répondre aux questions et automatiser votre support.'
)

html = html.replace(
    'Des IA sur-mesure int&eacute;gr&eacute;es &agrave; vos outils (Word, Excel, CRM) pour r&eacute;diger, analyser des donn&eacute;es et vous assister au quotidien.',
    'Formation de vos &eacute;quipes &agrave; l\'int&eacute;gration et l\'utilisation de copilotes intelligents pour r&eacute;diger, analyser des donn&eacute;es et vous assister.'
)

html = html.replace(
    'Des IA sur-mesure intégrées à vos outils (Word, Excel, CRM) pour rédiger, analyser des données et vous assister au quotidien.',
    'Formation de vos équipes à l\'intégration et l\'utilisation de copilotes intelligents pour rédiger, analyser des données et vous assister.'
)

html = html.replace(
    'Mise en place de flux de travail autonomes via Make ou Zapier pour relier vos applications et &eacute;liminer la double saisie.',
    'Formation et accompagnement &agrave; la mise en place de flux de travail autonomes (via Make/Zapier) pour automatiser vos processus.'
)

html = html.replace(
    'Mise en place de flux de travail autonomes via Make ou Zapier pour relier vos applications et éliminer la double saisie.',
    'Formation et accompagnement à la mise en place de flux de travail autonomes (via Make/Zapier) pour automatiser vos processus.'
)

html = html.replace(
    'Audit complet de vos processus existants pour identifier les t&acirc;ches &agrave; faible valeur ajout&eacute;e qui peuvent &ecirc;tre automatis&eacute;es ou optimis&eacute;es.',
    'Audit complet et accompagnement p&eacute;dagogique pour identifier les t&acirc;ches automatisables et structurer un plan de formation IA adapt&eacute;.'
)

html = html.replace(
    'Audit complet de vos processus existants pour identifier les tâches à faible valeur ajoutée qui peuvent être automatisées ou optimisées.',
    'Audit complet et accompagnement pédagogique pour identifier les tâches automatisables et structurer un plan de formation IA adapté.'
)


# Reorder sections: Move <section id="formations"> before <section id="solutions">
solutions_match = re.search(r'(<section id="solutions".*?</section>)', html, re.DOTALL)
targets_match = re.search(r'(<section id="targets".*?</section>)', html, re.DOTALL)
formations_match = re.search(r'(<section id="formations".*?</section>)', html, re.DOTALL)

if solutions_match and targets_match and formations_match:
    start_idx = html.find('<section id="solutions"')
    end_idx = html.find('</section>', html.find('<section id="formations"')) + 10
    
    original_block = html[start_idx:end_idx]
    
    # We want: Formations -> Targets -> Solutions
    new_block = formations_match.group(1) + '\n\n' + targets_match.group(1) + '\n\n' + solutions_match.group(1)
    
    html = html.replace(original_block, new_block)
    
# Swap Hero buttons
hero_cta_old = """                <div class="hero-cta">
                    <a href="#solutions" class="btn btn-primary">Solutions IA</a>
                    <a href="#formations" class="btn btn-secondary">Formations</a>
                </div>"""
hero_cta_new = """                <div class="hero-cta">
                    <a href="#formations" class="btn btn-primary">Formations</a>
                    <a href="#solutions" class="btn btn-secondary">Solutions IA</a>
                </div>"""
html = html.replace(hero_cta_old, hero_cta_new)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("All updates applied!")
