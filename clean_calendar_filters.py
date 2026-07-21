import os
import re

def clean_calendar_filters():
    filepath = 'calendrier-formations.html'
    if not os.path.exists(filepath):
        print(f"{filepath} not found!")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update filter buttons section
    # Search for: <aside class="calendar-sidebar"> ... </aside>
    filters_old = """                <aside class="calendar-sidebar">
                    <h3>Filtrer par module</h3>
                    <button class="filter-btn active" data-filter="all">Toutes les formations</button>
                    <button class="filter-btn" data-filter="avocats">Cabinets d'Avocats</button>
                    <button class="filter-btn" data-filter="comptables">Expertise Comptable</button>
                    <button class="filter-btn" data-filter="video_ia_pro">Vidéo IA Pro</button>
                    <button class="filter-btn" data-filter="prompting">IA Générative</button>
                    <button class="filter-btn" data-filter="python">Python pour la Data</button>
                    <button class="filter-btn" data-filter="machine_learning">Machine Learning</button>
                    <button class="filter-btn" data-filter="deep_learning">Deep Learning</button>
                    <button class="filter-btn" data-filter="jupyter">Jupyter Notebook</button>
                </aside>"""

    filters_new = """                <aside class="calendar-sidebar">
                    <h3>Filtrer par module</h3>
                    <button class="filter-btn active" data-filter="all">Toutes les formations</button>
                    <button class="filter-btn" data-filter="prompting">IA Générative</button>
                    <button class="filter-btn" data-filter="video_ia_pro">Vidéo IA Pro</button>
                    <button class="filter-btn" data-filter="python">Python</button>
                    <button class="filter-btn" data-filter="jupyter">Jupyter</button>
                    <button class="filter-btn" data-filter="machine_learning">Machine Learning</button>
                    <button class="filter-btn" data-filter="deep_learning">Deep Learning</button>
                </aside>"""

    if filters_old in html:
        html = html.replace(filters_old, filters_new)
        print("Updated filter buttons in calendar")
    else:
        # Try a regex-based approach for flexibility
        pattern = re.compile(r'<aside class="calendar-sidebar">.*?</aside>', re.DOTALL)
        html, count = pattern.subn(filters_new, html)
        if count > 0:
            print("Updated filter buttons in calendar via regex")

    # 2. Update top navbar button from "Diagnostic IA Gratuit" to "Être rappelé" if present
    html = html.replace('Diagnostic IA Gratuit', 'Être rappelé')
    html = html.replace('Diagnostic IA gratuit', 'Être rappelé')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

clean_calendar_filters()
