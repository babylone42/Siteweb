import os
import re

filePath = r"C:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb\calendrier-formations.html"

with open(filePath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the sidebar completely with only active filters for prompting
sidebar_regex = r'(<aside class="calendar-sidebar">[\s\S]*?</aside>)'
match = re.search(sidebar_regex, content)
if match:
    new_sidebar = """<aside class="calendar-sidebar">
                    <h3>Filtrer par module</h3>
                    <button class="filter-btn active" data-filter="all">Toutes les formations</button>
                    <button class="filter-btn" data-filter="prompting">IA Générative</button>
                </aside>"""
    content = content.replace(match.group(1), new_sidebar)

# Instead of block replacement, parse the HTML dynamically by finding month blocks, extracting course lists, and recreating them.
# The structure is very uniform:
# <div class="month-block" id="avril">
#     <h2 class="month-title">Avril 2026</h2>
#     <div class="course-list">
#         ... course items ...
#     </div>
#     [optional holiday-notice]
# </div>

blocks = re.findall(r'(<div class="month-block" id="[a-z]+">[\s\S]*?</div>\s*(?:<div class="holiday-notice"[\s\S]*?</div>)?\s*</div>)', content)

for block in blocks:
    # If the block doesn't contain prompting course items, remove it.
    course_items = re.findall(r'<div class="course-item[\s\S]*?</div>\s*</div>', block)
    prompting_items = [item for item in course_items if 'data-type="prompting"' in item]
    
    if not prompting_items:
        content = content.replace(block, "")
    else:
        # Recreate the list inner HTML
        list_match = re.search(r'<div class="course-list">([\s\S]*?)</div>', block)
        if list_match:
            # Clean up active state or gray outs
            cleaned_items = []
            for item in prompting_items:
                item_cleaned = item.replace(' card-disabled', '').replace(' style="pointer-events:none;"', '')
                cleaned_items.append(item_cleaned)
            new_list_inner = "\n                            " + "\n                            ".join(cleaned_items) + "\n                        "
            new_block = block.replace(list_match.group(1), new_list_inner)
            content = content.replace(block, new_block)

with open(filePath, "w", encoding="utf-8") as f:
    f.write(content)

print("Calendar cleaned up! Only IA Générative sessions remain.")
