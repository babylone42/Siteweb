import re

with open('about.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Meta
html = html.replace(
    'déployer des solutions d\'IA concrètes et former les entreprises',
    'former les entreprises et intégrer des outils IA'
)

# Text 1
html = html.replace(
    'déployer des solutions IA',
    'former leurs équipes et intégrer des outils IA'
)

# Text 2
html = html.replace(
    'Découvrir nos solutions',
    'Découvrir notre accompagnement'
)

# Text 3
html = html.replace(
    'Chaque solution est construite pour vous',
    'Chaque formation et intégration est construite pour vous'
)

# Text 4
html = html.replace(
    'solutions sont explicables, auditables et sécurisées.',
    'démarches sont explicables, auditables et sécurisées.'
)

# Text 5
html = html.replace(
    'et chaque solution que',
    'et chaque formation que'
)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated about.html texts")
