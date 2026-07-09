import os
import re

FILES = [
    {"path": "formation-video-ia-pro.html", "price": 1490, "price_indep": 1266.50, "ref": "REF-2026-VIDEOIA-001"},
    {"path": "formation-jupyter.html", "price": 420, "price_indep": 357, "ref": "REF-2026-JUPYTER-001"},
    {"path": "formation-python.html", "price": 1290, "price_indep": 1096.50, "ref": "REF-2026-PYTHON-001"},
    {"path": "formation-ml.html", "price": 1440, "price_indep": 1224, "ref": "REF-2026-ML-001"},
    {"path": "formation-dl.html", "price": 1440, "price_indep": 1224, "ref": "REF-2026-DL-001"},
    {"path": "Avocats/pack0_ia_literacy_avocats.html", "price": 490, "price_indep": 416.50, "ref": "REF-2026-AVOC-000"},
    {"path": "Avocats/pack1_ia_generative_avocats.html", "price": 990, "price_indep": 841.50, "ref": "REF-2026-AVOC-001"},
    {"path": "Avocats/pack2_prompt_engineering_avocats.html", "price": 1090, "price_indep": 926.50, "ref": "REF-2026-AVOC-002"},
    {"path": "Avocats/pack3_ia_secret_pro_avocats.html", "price": 1490, "price_indep": 1266.50, "ref": "REF-2026-AVOC-003"},
    {"path": "Comptables/pack0_ia_literacy_comptables.html", "price": 490, "price_indep": 416.50, "ref": "REF-2026-COMPT-000"},
    {"path": "Comptables/pack1_ia_generative_comptables.html", "price": 990, "price_indep": 841.50, "ref": "REF-2026-COMPT-001"},
    {"path": "Comptables/pack2_prompt_engineering_comptables.html", "price": 1090, "price_indep": 926.50, "ref": "REF-2026-COMPT-002"},
    {"path": "Comptables/pack3_ia_secret_pro_comptables.html", "price": 1490, "price_indep": 1266.50, "ref": "REF-2026-COMPT-003"}
]

TEMPLATE = """
        <!-- QUALIOPI INFORMATION BANNER -->
        <section class="section-padding" style="background: rgba(255, 255, 255, 0.02); border-top: 1px solid rgba(255, 255, 255, 0.05);">
            <div class="container" style="max-width: 960px;">
                <h2 class="section-title" style="font-size: 1.6rem; margin-bottom: 1.5rem; text-align: center;">Informations légales et pratiques</h2>
                <div class="qualiopi-grid">

                    <!-- Organisme -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-building" style="margin-right: 0.5rem;"></i> Organisme de formation</strong>
                        <strong>Babylone 42 SAS</strong><br>
                        SIRET : 992 220 707 00010<br>
                        NDA : 93132513713 — Déclaration d'activité enregistrée auprès du préfet de région Provence-Alpes-Côte d'Azur. Cet enregistrement ne vaut pas agrément de l'État.<br>
                        Démarche de certification Qualiopi en cours.
                    </div>

                    <!-- Modalités d'accès et inscription -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-clipboard-list" style="margin-right: 0.5rem;"></i> Modalités d'accès et d'inscription</strong>
                        <ol style="padding-left: 1.2rem; margin: 0.5rem 0; color: inherit; line-height: 1.8;">
                            <li>Remplir le <a href="{prefix}inscription.html" style="color: var(--primary-color);">formulaire de pré-inscription en ligne</a>.</li>
                            <li>Entretien de positionnement (téléphonique) sous <strong>48h</strong> pour valider l'adéquation du profil.</li>
                            <li>Réception de la convention de formation et du devis à retourner signés <strong>au plus tard 14 jours avant</strong> le début de la session.</li>
                        </ol>
                        Délai d'accès moyen : <strong>3 semaines</strong> entre la prise de contact et le début de la formation.<br>
                        <a href='{prefix}calendrier-formations.html' style='color: var(--primary-color);'>Voir les prochaines sessions →</a>
                    </div>

                    <!-- Tarifs et financements -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-euro-sign" style="margin-right: 0.5rem;"></i> Tarifs et financements</strong>
                        <strong>Tarif inter-entreprises :</strong> {price} € HT (exonération de TVA — art. 261.4.4° a du CGI)<br>
                        <strong>Tarif indépendant :</strong> {price_indep} € HT <small>(sur justificatif de micro-entreprise ou profession libérale)</small><br>
                        <strong>Modalités de règlement :</strong> 30% d'acompte à la signature de la convention, solde 15 jours avant le début de la formation. Facilités de paiement possibles.<br>
                        <strong>Financements :</strong> OPCO, CPF, Plan de développement des compétences, financement direct.<br>
                        Intra-entreprise : <a href='{prefix}contact-page.html' style='color: var(--primary-color);'>devis sur demande</a>.
                    </div>

                    <!-- Modalités d'évaluation -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-graduation-cap" style="margin-right: 0.5rem;"></i> Modalités d'évaluation</strong>
                        <strong>Positionnement initial :</strong> Questionnaire en ligne (15 min) + entretien téléphonique de 15 min.<br>
                        <strong>Évaluation continue :</strong> Exercices pratiques à chaque module, corrigés et commentés en séance.<br>
                        <strong>Évaluation finale :</strong> Mise en situation professionnelle (plan d'action intégration IA). <strong>Seuil de réussite : 14/20.</strong><br>
                        <strong>Évaluation à chaud :</strong> Questionnaire de satisfaction en ligne (fin de formation).<br>
                        <strong>Évaluation à froid :</strong> Questionnaire d'impact à J+30 et J+90 pour mesurer la mise en pratique des acquis.<br>
                        Attestation de réussite + badge numérique remis à l'issue.
                    </div>

                    <!-- Méthodes pédagogiques -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-laptop" style="margin-right: 0.5rem;"></i> Méthodes pédagogiques</strong>
                        <strong>30% apports théoriques / 70% ateliers pratiques</strong><br>
                        Distanciel synchrone (Microsoft Teams) — 9h00–12h30 / 13h30–17h00.<br>
                        Ressources accessibles 6 mois post-formation (bibliothèque de prompts, supports, guides).<br>
                        Taille de groupe : 4 à 12 participants maximum.
                    </div>

                    <!-- Accessibilité PSH -->
                    <div>
                        <strong style="color: var(--primary-color); display: block; margin-bottom: 0.5rem; font-size: 1.1rem;"><i class="fas fa-wheelchair" style="margin-right: 0.5rem;"></i> Accessibilité et Référent handicap</strong>
                        Référent handicap : <strong>Eulalio TORRES GARCIA</strong><br>
                        <a href="mailto:contact@babylone42.fr" style="color: var(--primary-color);">contact@babylone42.fr</a> | <a href="tel:+33773609849" style="color: var(--primary-color);">+33 7 73 60 98 49</a><br>
                        Délai de traitement des demandes PSH : <strong>3 semaines</strong> avant le début de la formation.<br>
                        <strong>Adaptations possibles :</strong> Supports modifiables, sous-titrage des vidéos, aménagement des horaires, pauses supplémentaires, matériel spécifique (en distanciel).<br>
                        <strong>Partenaires mobilisables :</strong> Agefiph, Cap Emploi Marseille, MDPH des Bouches-du-Rhône, Ressource Handicap Formation.<br>
                        <a href='{prefix}accessibilite.html' style='color: var(--primary-color); text-decoration: underline;'>Consulter notre charte d'engagement accessibilité →</a>
                    </div>

                </div>
            </div>
        </section>

        <!-- NOS INDICATEURS DE RÉSULTATS -->
        <section class="section-padding bg-light">
            <div class="container" style="max-width: 860px;">
                <h2 class="section-title" style="color: #0f172a;">Nos indicateurs <span class="highlight">de résultats</span></h2>
                <p class="section-subtitle" style="margin-bottom: 2rem;">
                    Conformément au référentiel Qualiopi (C1-I2), nous collectons et publierons les indicateurs ci-dessous dès que nos premières sessions seront complétées.
                </p>
                <div class="indicateurs-grid">
                    <div class="bento-card" style="background: white; border: 1px solid #e2e8f0; color: #0f172a; text-align: center; padding: 1.5rem;">
                        <i class="fas fa-smile" style="font-size: 1.8rem; color: var(--primary-color); margin-bottom: 0.8rem;"></i>
                        <strong style="display: block; color: #0f172a; font-size: 1rem; margin-bottom: 0.3rem;">Taux de satisfaction</strong>
                        <p style="color: #64748b; font-size: 0.88rem; margin: 0;">Enquête à chaud — questionnaire en ligne en fin de formation</p>
                        <span style="display: inline-block; margin-top: 0.8rem; background: #f1f5f9; color: #94a3b8; font-size: 0.8rem; padding: 0.2rem 0.8rem; border-radius: 20px;">En cours de collecte</span>
                    </div>
                    <div class="bento-card" style="background: white; border: 1px solid #e2e8f0; color: #0f172a; text-align: center; padding: 1.5rem;">
                        <i class="fas fa-bullhorn" style="font-size: 1.8rem; color: var(--primary-color); margin-bottom: 0.8rem;"></i>
                        <strong style="display: block; color: #0f172a; font-size: 1rem; margin-bottom: 0.3rem;">Taux de recommandation</strong>
                        <p style="color: #64748b; font-size: 0.88rem; margin: 0;">Net Promoter Score (NPS) mesuré auprès des stagiaires</p>
                        <span style="display: inline-block; margin-top: 0.8rem; background: #f1f5f9; color: #94a3b8; font-size: 0.8rem; padding: 0.2rem 0.8rem; border-radius: 20px;">En cours de collecte</span>
                    </div>
                    <div class="bento-card" style="background: white; border: 1px solid #e2e8f0; color: #0f172a; text-align: center; padding: 1.5rem;">
                        <i class="fas fa-door-open" style="font-size: 1.8rem; color: var(--primary-color); margin-bottom: 0.8rem;"></i>
                        <strong style="display: block; color: #0f172a; font-size: 1rem; margin-bottom: 0.3rem;">Taux d'abandon</strong>
                        <p style="color: #64748b; font-size: 0.88rem; margin: 0;">Nombre de ruptures de parcours en cours de formation</p>
                        <span style="display: inline-block; margin-top: 0.8rem; background: #f1f5f9; color: #94a3b8; font-size: 0.8rem; padding: 0.2rem 0.8rem; border-radius: 20px;">En cours de collecte</span>
                    </div>
                    <div class="bento-card" style="background: white; border: 1px solid #e2e8f0; color: #0f172a; text-align: center; padding: 1.5rem;">
                        <i class="fas fa-briefcase" style="font-size: 1.8rem; color: var(--primary-color); margin-bottom: 0.8rem;"></i>
                        <strong style="display: block; color: #0f172a; font-size: 1rem; margin-bottom: 0.3rem;">Impact métier</strong>
                        <p style="color: #64748b; font-size: 0.88rem; margin: 0;">Enquête à froid (J+30) — mise en pratique des compétences</p>
                        <span style="display: inline-block; margin-top: 0.8rem; background: #f1f5f9; color: #94a3b8; font-size: 0.8rem; padding: 0.2rem 0.8rem; border-radius: 20px;">En cours de collecte</span>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 1rem; font-size: 0.9rem; color: #64748b;">
                    <a href='{prefix}indicateurs-resultats.html' style='color: var(--primary-color); text-decoration: underline;'>Consulter notre méthodologie détaillée pour les indicateurs de résultats →</a>
                </p>
            </div>
        </section>

    </main>

    <footer class="mega-footer">
        <div class="container">
            <div class="footer-grid">
                <!-- Column 1: Brand & Socials -->
                <div class="footer-col brand-col">
                    <img src="{prefix}images/logo.svg" alt="Babylone42 Logo" class="footer-logo-img">
                    <p class="footer-desc">Babylone42 donne le pouvoir aux équipes de transformer des données brutes en
                        informations claires grâce à l'IA.</p>
                    <div class="footer-socials">
                        <a href="https://www.linkedin.com/company/babylone42/" target="_blank" rel="noopener noreferrer"
                            aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a>
                        <a href="https://www.instagram.com/babylone42_?igsh=YzVyamk1N3VoYXU1" target="_blank"
                            rel="noopener noreferrer" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.facebook.com/profile.php?id=61583402791597&name=xhp_nt__fb__action__open_user&locale=fr_FR"
                            target="_blank" rel="noopener noreferrer" aria-label="Facebook"><i
                                class="fab fa-facebook"></i></a>
                        <a href="https://x.com/babylone42_" target="_blank" rel="noopener noreferrer"
                            aria-label="X Twitter"><i class="fab fa-x-twitter"></i></a>
                        <a href="https://m.youtube.com/@Babylone42" target="_blank" rel="noopener noreferrer"
                            aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>

                <!-- Column 2: Accueil -->
                <div class="footer-col">
                    <h4 class="footer-title">Accueil</h4>
                    <ul class="footer-links-list">
                        <li><a href="{prefix}about.html">About us</a></li>
                        <li><a href="{prefix}interlocuteurs.html">Vos interlocuteurs</a></li>
                        <li><a href="{prefix}articles.html">Actualités</a></li>
                        <li><a href="{prefix}faq.html">FAQ</a></li>
                    </ul>
                </div>

                <!-- Column 3: Solutions -->
                <div class="footer-col">
                    <h4 class="footer-title">Solutions IA</h4>
                    <ul class="footer-links-list">
                        <li><a href="{prefix}solution-chatbots.html">Chatbots 24/7</a></li>
                        <li><a href="{prefix}solution-copilots.html">Copilots IA</a></li>
                        <li><a href="{prefix}solution-automation.html">Automatisation</a></li>
                        <li><a href="{prefix}solution-audit.html">Audit & Conseil</a></li>
                    </ul>
                </div>

                <!-- Column 4: Formations -->
                <div class="footer-col">
                    <h4 class="footer-title">Formations</h4>
                    <ul class="footer-links-list">
                        <li><a href="{prefix}formation-genai.html">IA Générative</a></li>
                        <li><a href="{prefix}formation-video-ia-pro.html">Vidéo IA Pro</a></li>
                        <li><a href="{prefix}formation-jupyter.html">Jupyter</a></li>
                        <li><a href="{prefix}formation-python.html">Python</a></li>
                        <li><a href="{prefix}formation-ml.html">Machine Learning</a></li>
                        <li><a href="{prefix}formation-dl.html">Deep Learning</a></li>
                    </ul>
                </div>

                <!-- Column 5: Contact & Newsletter -->
                <div class="footer-col newsletter-col">
                    <h4 class="footer-title">Contact & Newsletter</h4>
                    <p class="footer-contact-info">
                        <a href="mailto:contact@babylone42.fr"><i class="fas fa-envelope"></i>
                            contact@babylone42.fr</a><br>
                        <a href="tel:+330773609849"><i class="fas fa-phone-alt"></i> +33 0 7 73 60 98 49</a>
                    </p>
                    <form class="footer-newsletter-form">
                        <input type="email" placeholder="Votre email" required>
                        <button type="submit" aria-label="S'inscrire"><i class="fas fa-paper-plane"></i></button>
                    </form>
                </div>
            </div>

            <div class="footer-bottom">
                <p class="copyright">© 2025 Babylone42.  · SIRET : 992 220 707 00010 · NDA : enregistré sous le numéro 93132513713. Cet enregistrement ne vaut pas agrément de l'État.</p>
                <div class="legal-links"><a href="{prefix}indicateurs-resultats.html">Indicateurs de Résultats</a><a href="{prefix}cgv.html">CGV</a>
                    <a href="{prefix}mentions-legales.html">Mentions Légales</a>
                    <a href="{prefix}politique-confidentialite.html">Politique de Confidentialité</a>
                    <a href="{prefix}cookies.html">Paramètres des cookies</a>
                    <a href="{prefix}accessibilite.html">Accessibilité (RGAA)</a>
                </div>
            </div>
        </div>
    </footer>
"""

for f in FILES:
    path = os.path.join(r'C:\Users\eto_g\OneDrive - Babylone 42\Babylone42-2.0\Siteweb', f['path'])
    if not os.path.exists(path):
        print(f"Skipping {f['path']} (not found)")
        continue
        
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    prefix = "../" if "/" in f['path'] else ""
    
    # 1. Inject PDF link in Hero
    btn_container_regex = r'(<div style="display: ?flex; ?justify-content: ?center; ?gap: ?1rem; ?flex-wrap: ?wrap;?">)'
    if re.search(btn_container_regex, content):
        pdf_snippet = f'''<p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem;">
                            <i class="fas fa-file-pdf" style="color: var(--primary-color);"></i>
                            <a href="{prefix}programmes/{f["ref"]}.pdf" style="color: var(--primary-color); text-decoration: underline;">Télécharger le programme complet (PDF)</a>
                            &nbsp;|&nbsp; Réf. : {f["ref"]} &nbsp;|&nbsp; Dernière mise à jour : juillet 2026
                        </p>
                        '''
        if "Télécharger le programme complet (PDF)" not in content:
            content = re.sub(btn_container_regex, pdf_snippet + r'\1', content, count=1)
            
    # 2. Replace Qualiopi Banner + Footer
    if '<!-- QUALIOPI INFORMATION BANNER -->' in content:
        start_idx = content.find('<!-- QUALIOPI INFORMATION BANNER -->')
    else:
        start_idx = content.find('</main>')
        
    if start_idx != -1:
        content_top = content[:start_idx]
        new_bottom = TEMPLATE.format(
            price=f"{f['price']:.0f}" if f['price'] % 1 == 0 else f"{f['price']:.2f}".replace('.', ','),
            price_indep=f"{f['price_indep']:.0f}" if f['price_indep'] % 1 == 0 else f"{f['price_indep']:.2f}".replace('.', ','),
            prefix=prefix
        )
        content = content_top + new_bottom + "\n    <!-- MAIN SCRIPTS -->\n    <script src=\"{prefix}script.js?v=5\"></script>\n</body>\n</html>".replace("{prefix}", prefix)
        
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)
        
    print(f"Updated {f['path']}")
