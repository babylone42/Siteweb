import os

pages = [
    ("about.html", "À propos de Babylone42"),
    ("interlocuteurs.html", "Vos Interlocuteurs"),
    ("formation-genai.html", "Formation IA Générative"),
    ("formation-jupyter.html", "Formation Jupyter"),
    ("formation-python.html", "Formation Python"),
    ("formation-ml.html", "Formation Machine Learning"),
    ("formation-dl.html", "Formation Deep Learning"),
    ("solution-audit.html", "Audit & Conseil IA"),
    ("articles.html", "Blog & Actualités IA"),
    ("faq.html", "Foire Aux Questions"),
    ("contact-page.html", "Contactez-nous"),
    ("mentions-legales.html", "Mentions Légales"),
    ("politique-confidentialite.html", "Politique de Confidentialité"),
    ("cookies.html", "Paramètres des cookies")
]

# Read index.html to extract the header and footer
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract from <html> to </nav>
header_part = content.split('<!-- HERO SECTION -->')[0]

# Extract from <footer class="mega-footer"> to </html>
footer_part = "    <!-- FOOTER -->\n" + content.split('<!-- FOOTER -->')[1]

template = """{header}

    <main class="page-content" style="padding-top: 120px; padding-bottom: 80px; min-height: 60vh;">
        <div class="container section-padding">
            <h1 class="section-title" style="margin-bottom: 2rem;">{title}</h1>
            <div style="background: rgba(255, 255, 255, 0.03); padding: 4rem 2rem; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.1); text-align: center;">
                <p style="color: #94a3b8; font-size: 1.1rem;">Page en cours de construction. Le contenu spécifique à cette section sera ajouté ici.</p>
            </div>
        </div>
    </main>

{footer}"""

for filename, title in pages:
    page_content = template.format(header=header_part, title=title, footer=footer_part)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f"Created {filename}")

print("All pages scaffolded successfully!")
