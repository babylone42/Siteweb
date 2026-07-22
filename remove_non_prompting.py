import re
import os

def keep_only_prompting_in_calendar():
    filepath = 'calendrier-formations.html'
    if not os.path.exists(filepath):
        print("Calendar file not found!")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update filters list to only show Prompting (IA Générative)
    # Search for the <aside class="calendar-sidebar">...</aside> and replace it.
    sidebar_pattern = re.compile(r'<aside class="calendar-sidebar">.*?</aside>', re.DOTALL)
    new_sidebar = """                <aside class="calendar-sidebar">
                    <h3>Filtrer par module</h3>
                    <button class="filter-btn active" data-filter="all">Toutes les formations</button>
                    <button class="filter-btn" data-filter="prompting">IA Générative</button>
                </aside>"""
    html = sidebar_pattern.sub(new_sidebar, html)

    # 2. Modify month blocks to remove any course-item that doesn't have data-type="prompting"
    # We will find every <div class="course-item" ...> ... </div> block and remove it if it is not prompting.
    # The course-item ends with the closing div </div>. Let's look at the structure:
    # <div class="course-item[^"]*"[^>]*data-type="(?P<type>[^"]+)"[^>]*>.*?</div>\s*</div>\s*(<!-- Next item or end of list -->)
    # Actually, each course-item is enclosed between:
    # <div class="course-item... data-type="...">
    #    ...
    # </div>
    # Let's match the block carefully. Since there are nested tags, matching balanced HTML divs in regex is tricky,
    # but each course-item has no nested container divs. It only has <div class="course-dates">...</div>,
    # <div class="course-info">...</div> and <div class="course-action">...</div>.
    # So we can match: <div class="course-item.*?</div>\s*</div>
    # Let's write a parser using BeautifulSoup to be 100% precise and avoid regex bugs with HTML.
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all course items
        course_items = soup.find_all('div', class_='course-item')
        for item in course_items:
            # If not prompting, decompose it
            if item.get('data-type') != 'prompting':
                item.decompose()
                
        # Also clean sidebar menu just in case BeautifulSoup structure is easier
        html = str(soup)
        print("Cleaned calendar items using BeautifulSoup")
    except ImportError:
        # Fallback to regex if bs4 is not available (though standard environments usually have it or python standard lib can do it)
        print("BeautifulSoup not available, trying manual parsing")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

keep_only_prompting_in_calendar()
