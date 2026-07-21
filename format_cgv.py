import re

with open('scratch_cgv.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

html = []
headers = [
    "OBJET", "INSCRIPTION ET CONTRACTUALISATION", "PRIX ET MODALITÉS DE PAIEMENT",
    "Financement et Prise en Charge (OPCO)", "DÉlai de Rétractation (Particuliers)",
    "CONDITIONS D’ANNULATION ET DE REPORT", "Annulation par le Client :",
    "Annulation par l’Organisme de formation :", "DÉroulement des Formations et RÈglement IntÉrieur",
    "PropriÉtÉ Intellectuelle", "DonnÉes Personnelles (RGPD)", "AccessibilitÉ et Handicap (Qualiopi)",
    "ResponsabilitÉs", "RECLAMATIONS", "INDICATEURS DE RESULTATS", "AMÉLIORATION CONTINUE",
    "Litiges, Droit Applicable et Médiation"
]

for line in lines:
    if line in headers or line.isupper():
        html.append(f'<h2 style="color: var(--primary-color); font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem;">{line}</h2>')
    elif line.startswith("Conditions Générales de Vente") or line.startswith("Babylone 42 SAS") or line.startswith("79 rue") or line.startswith("Représentée") or line.startswith("Déclaration") or line.startswith("SIRET"):
        continue # Already in the header of the page
    elif "Tarif public inter-entreprises : 790 € HT" in line or "Tarif indépendant : 590 € HT" in line:
        pass # Skip these and replace with the combined sentence
    elif "Tous les prix sont exprimés en euros nets de TVA" in line:
        html.append(f'<p>{line}</p>')
        html.append(f'<p><strong>Les tarifs sont spécifiques à chaque formation et communiqués sur les pages dédiées de notre site internet ou sur devis.</strong></p>')
    else:
        html.append(f'<p style="margin-bottom: 1rem;">{line}</p>')

full_html = "\n".join(html)

with open('cgv_formatted.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
