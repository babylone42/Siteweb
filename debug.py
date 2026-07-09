import re
import os

path = r'C:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb\Avocats\pack2_prompt_engineering_avocats.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

btn_container_regex = r'(<div style="display: ?flex; ?justify-content: ?center; ?gap: ?1rem; ?flex-wrap: ?wrap;?">)'
m = re.search(btn_container_regex, content)
if m:
    print('Found btn container')
else:
    print('Btn container not found!')
    # find where it could be inserted
    idx = content.find('<a href="../inscription')
    if idx != -1:
        print("Surrounding buttons:")
        print(content[idx-200:idx+200])
