import re

with open('calendrier-formations.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
skip = False
skip_indent = 0
for line in lines:
    if not skip and '<div class="course-item' in line and 'data-type="prompting"' not in line:
        skip = True
        skip_indent = len(line) - len(line.lstrip())
        continue
    if skip:
        if line.strip() == '</div>' and (len(line) - len(line.lstrip())) == skip_indent:
            skip = False
        continue
    out.append(line)

# Now check if any month-block has no course-items
final_out = []
i = 0
while i < len(out):
    line = out[i]
    if '<div class="month-block"' in line:
        # Check ahead to see if there is any course-item before the next month-block or end of calendar
        has_items = False
        j = i + 1
        while j < len(out) and '<div class="month-block"' not in out[j] and '<!-- FOOTER -->' not in out[j]:
            if '<div class="course-item"' in out[j]:
                has_items = True
                break
            j += 1
        
        if not has_items:
            # Skip this month-block
            # It ends with </div></div></div> usually, but let's just skip until we find <div class="month-block" or <!-- FOOTER
            i = j
            continue
    final_out.append(out[i])
    i += 1

with open('calendrier-formations.html', 'w', encoding='utf-8') as f:
    f.writelines(final_out)
