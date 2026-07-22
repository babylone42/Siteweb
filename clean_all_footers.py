import glob

def clean_footer_and_alternatives():
    html_files = glob.glob('**/*.html', recursive=True)
    count = 0

    footer_old = "Babylone42 donne le pouvoir aux équipes de transformer des données brutes en\n                        informations claires grâce à l'IA."
    footer_old_2 = "Babylone42 donne le pouvoir aux équipes de transformer des données brutes en informations claires grâce à l'IA."
    
    footer_new = "Babylone42 forme vos équipes à exploiter le potentiel de l'IA et de la data pour gagner en autonomie et en productivité."

    for file in html_files:
        if file.startswith('archive'):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        
        # Replace multi-line footer block
        content = content.replace(footer_old, footer_new)
        content = content.replace(footer_old_2, footer_new)
        # Just in case there are single line differences
        content = content.replace("Babylone42 donne le pouvoir aux équipes de transformer des données brutes en\n                        informations claires grâce à l'IA.", footer_new)
        content = content.replace("Babylone42 donne le pouvoir aux équipes de transformer des données brutes en\n                            informations claires grâce à l'IA.", footer_new)

        if content != orig:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"Cleaned footer text in {file}")

    print(f"Updated footer text on {count} files")

clean_footer_and_alternatives()
