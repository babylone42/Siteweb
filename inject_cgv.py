import re

with open('cgv_formatted.html', 'r', encoding='utf-8') as f:
    cgv_content = f.read()

with open('cgv.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<section style="margin-bottom: 2\.5rem;">.*?</section>', re.DOTALL)
new_html = pattern.sub('<section style="margin-bottom: 2.5rem;">\n' + cgv_content + '\n</section>', html)

with open('cgv.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
