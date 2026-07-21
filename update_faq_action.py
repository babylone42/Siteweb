import os
import glob
import re

new_faq_html = """                        <!-- Item 1 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Comment se déroule une formation avec Babylone42 ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Nous commençons par un diagnostic gratuit de vos besoins en compétences. Ensuite, nous vous proposons un parcours pédagogique adapté. Les sessions alternent théorie et nombreux cas pratiques sur vos propres outils professionnels.</p>
                            </div>
                        </div>
                        <!-- Item 2 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Combien coûtent vos parcours de formation ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Nos tarifs varient selon la durée et le format (intra/inter-entreprises). Nous ajustons systématiquement nos propositions pour optimiser la prise en charge par les fonds de formation. Contactez-nous pour un devis précis.</p>
                            </div>
                        </div>
                        <!-- Item 3 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Mes données sont-elles sécurisées pendant les cas pratiques ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Absolument. Nous vous apprenons à configurer des environnements sécurisés (mode confidentiel, instances privées) et nous garantissons que les données utilisées en formation ne nourrissent aucun modèle public.</p>
                            </div>
                        </div>
                        <!-- Item 4 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Dois-je avoir des compétences techniques pour suivre vos formations ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Non, ce n'est pas nécessaire pour nos parcours "Literacy" ou "IA Générative". Nos formations sont conçues pour être accessibles à tous les collaborateurs, quel que soit leur niveau technique initial.</p>
                            </div>
                        </div>
                        <!-- Item 5 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Quelles technologies sont enseignées ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Nous vous formons sur les outils les plus performants du marché (ChatGPT, Claude, Midjourney), mais aussi sur des compétences métiers ciblées (Python, Copilots d'entreprise) selon votre parcours.</p>
                            </div>
                        </div>
                        <!-- Item 6 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>L'IA va-t-elle remplacer mes employés ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Non, notre approche pédagogique démontre que l'IA est un assistant (un "Copilot"). Nous formons vos collaborateurs pour qu'ils s'approprient cet outil, gagnent en productivité et se concentrent sur la valeur ajoutée de leur métier.</p>
                            </div>
                        </div>
                        <!-- Item 7 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Vos formations sont-elles éligibles aux financements ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>Oui. Nos parcours répondent aux critères de prise en charge du Plan de Développement des Compétences (OPCO). Nous vous accompagnons dans le montage de vos dossiers de financement.</p>
                            </div>
                        </div>
                        <!-- Item 8 -->
                        <div class="faq-item">
                            <div class="faq-question">
                                <h3>Au bout de combien de temps serons-nous autonomes ?</h3>
                                <i class="fas fa-chevron-down"></i>
                            </div>
                            <div class="faq-answer">
                                <p>L'autonomie est le cœur de notre pédagogie. Dès la fin de la première journée, vos équipes seront capables de mettre en application leurs nouvelles compétences sur des tâches concrètes.</p>
                            </div>
                        </div>
                        <!-- Item 9 -->
"""

new_action_text = """Il est grand temps de transformer vos équipes grâce à l'IA. Chez Babylone 42, nous concevons des parcours de formation immersifs pour permettre à vos collaborateurs d'utiliser les intelligences artificielles génératives au quotidien. Que vous souhaitiez automatiser la création de contenus, accélérer vos recherches juridiques ou comptables, ou former vos développeurs à l'IA, notre organisme est là pour vous accompagner. Notre équipe d'experts pédagogiques est prête à analyser vos besoins en compétences pour vous proposer un plan de formation adapté à votre budget et à vos objectifs. Faites le premier pas vers l'autonomie technologique de votre entreprise et contactez-nous dès aujourd'hui pour être rappelé par un conseiller formation."""

def update_files():
    html_files = glob.glob('**/*.html', recursive=True)
    for file in html_files:
        if file.startswith('archive'):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        original_html = html
        
        # Change the button text across all files
        # It's <a href="contact-page.html" class="btn btn-primary nav-btn">Diagnostic IA Gratuit</a>
        html = re.sub(r'>Diagnostic IA Gratuit<', '>Être rappelé<', html)
        html = re.sub(r'>Diagnostic IA gratuit<', '>Être rappelé<', html)
        # Some places it might be a button or span
        html = html.replace('Diagnostic IA Gratuit', 'Être rappelé')
        
        if os.path.basename(file) in ['index.html', 'index1.html']:
            # Replace FAQ content
            faq_pattern = re.compile(r'<!-- Item 1 -->.*?<!-- Item 9 -->', re.DOTALL)
            html = faq_pattern.sub(new_faq_html, html)
            
            # Replace Action text
            action_pattern = re.compile(r'Il est grand temps de transformer.*?catalyser la réussite éclatante de vos projets\.', re.DOTALL)
            html = action_pattern.sub(new_action_text, html)

            # Let's also remove the badge text "Gratuit" above Passez à l'action if it's there
            html = html.replace('<span class="badge">Diagnostic Gratuit</span>', '<span class="badge">Contact</span>')
            
        if html != original_html:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Updated {file}")

update_files()
