import re
import glob

files = glob.glob('*.html')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove existing Video IA Pro list items to avoid duplicates
    content = re.sub(r'\s*<li><a href="formation-video-ia-pro\.html">Vidéo IA Pro</a></li>', '', content)
    
    # Add Video IA Pro after IA Générative, matching its indentation
    def replacer(match):
        indent = match.group(1)
        original = match.group(0)
        return original + '\n' + indent + '<li><a href="formation-video-ia-pro.html">Vidéo IA Pro</a></li>'
    
    content = re.sub(r'([ \t]*)<li><a href="formation-genai\.html">IA Générative</a></li>', replacer, content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Mise à jour de {len(files)} fichiers HTML terminée.")
