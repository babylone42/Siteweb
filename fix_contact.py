import re
with open('contact-page.html', 'r', encoding='utf-8') as f:
    text = f.read()

def repl(m):
    if 'value="prompting"' in m.group(0) or 'value="custom"' in m.group(0):
        return m.group(0)
    else:
        # Replace completely the element with an empty string or hide it. Let's hide it completely by changing the class to hidden
        return m.group(0).replace('<label class="checkbox-btn"', '<label class="checkbox-btn" style="display:none;"')

new_text = re.sub(r'<label class="checkbox-btn"><input type="checkbox" name="formation_type".*?</label>', repl, text, flags=re.DOTALL)
with open('contact-page.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
