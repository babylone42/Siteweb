document.addEventListener('DOMContentLoaded', () => {

    // Smooth Scrolling for Anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Navbar Scroll Effect (Hide top row on scroll)
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const toggleScrolled = () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', toggleScrolled);
        // Initialize state on load to prevent jumping
        toggleScrolled();
    }

    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active-mobile-menu');
            hamburger.innerHTML = navLinks.classList.contains('active-mobile-menu') ? '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active-mobile-menu');
                hamburger.innerHTML = '<i class="fas fa-bars"></i>';
            });
        });
    }

    // Supabase Configuration
    const SUPABASE_URL = 'https://nzkirwiilgdlitbylxxv.supabase.co';
    const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56a2lyd2lpbGdkbGl0YnlseHh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE5NDYxNzIsImV4cCI6MjA4NzUyMjE3Mn0.xad9ed_JK-6goYodSyhhcEEiOdmro0xq2skohjGW7SE';

    // ── Email notification helper (Web3Forms – no activation needed) ──────────
    // Web3Forms sends emails to the address linked to the access key.
    // Key below is linked to contact@babylone42.fr
    const WEB3FORMS_KEY = '0a0ab618-aa84-43be-8671-9547db7ede48';

    async function sendEmailNotification(subject, fields) {
        try {
            await fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                body: JSON.stringify({
                    access_key: WEB3FORMS_KEY,
                    subject: subject,
                    from_name: 'Site Babylone42',
                    ...fields
                })
            });
        } catch (err) {
            console.error('Email notification failed:', err);
        }
    }
    // ─────────────────────────────────────────────────────────────────────────

    // Form Submission Handling (Contact via Supabase)
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Envoi en cours...';
            btn.style.opacity = '0.7';

            // Gather Data
            const activeToggle = document.querySelector('.btn-toggle.active');
            const need_type = activeToggle ? activeToggle.getAttribute('data-type') : 'solutions';

            let sub_need = '';
            if (need_type === 'solutions') {
                const selectedRadio = document.querySelector('input[name="solution_type"]:checked');
                sub_need = selectedRadio ? selectedRadio.value : 'other';
            } else {
                const checkedBoxes = document.querySelectorAll('input[name="formation_type"]:checked');
                const values = Array.from(checkedBoxes).map(cb => cb.value);
                sub_need = values.length > 0 ? values.join(', ') : 'none_selected';
            }

            const payload = {
                first_name: document.getElementById('firstname').value,
                last_name: document.getElementById('lastname').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value || null,
                need_type: need_type,
                sub_need: sub_need
            };

            try {
                const response = await fetch(`${SUPABASE_URL}/rest/v1/contacts`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset();
                    btn.innerText = originalText;
                    btn.style.opacity = '1';

                    // Reset toggles UI state visually back to Solutions
                    const solutionsBtn = document.querySelector('.btn-toggle[data-type="solutions"]');
                    if (solutionsBtn && !solutionsBtn.classList.contains('active')) {
                        solutionsBtn.click();
                    }

                    if (window.showSuccessModal) {
                        window.showSuccessModal(
                            "Message envoyé !",
                            "Votre demande a bien été reçue. Un expert Babylone42 vous recontactera très rapidement."
                        );
                    }
                } else {
                    const errorResponse = await response.text();
                    console.error('Supabase Error:', errorResponse);
                    btn.innerText = 'Erreur lors de l\'envoi ❌';
                    btn.style.backgroundColor = '#ef4444';
                    btn.style.color = '#fff';
                    setTimeout(() => {
                        btn.innerText = originalText;
                        btn.style.backgroundColor = '';
                        btn.style.opacity = '1';
                    }, 5000);
                }
            } catch (err) {
                console.error('Network Error:', err);
                btn.innerText = 'Erreur réseau ❌';
                btn.style.backgroundColor = '#ef4444';
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.opacity = '1';
                }, 5000);
            }
        });
    }

    // Newsletter Submission Handling (Supabase)
    const newsletterForms = document.querySelectorAll('.footer-newsletter-form');
    newsletterForms.forEach(nForm => {
        nForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = nForm.querySelector('input[type="email"]');
            const btn = nForm.querySelector('button');
            const email = input.value;
            if (!email) return;

            // Visual feedback
            const originalHtml = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            btn.style.opacity = '0.7';

            try {
                const response = await fetch(`${SUPABASE_URL}/rest/v1/newsletter_subscribers`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify({ email: email })
                });

                if (response.ok || response.status === 409) {
                    // 409 Conflict if email already exists, treat as success for UX
                    btn.innerHTML = originalHtml;
                    btn.style.opacity = '1';
                    input.value = '';

                    if (window.showSuccessModal) {
                        window.showSuccessModal(
                            "Inscription réussie !",
                            "Merci pour votre intérêt. Vous recevrez bientôt nos actualités IA."
                        );
                    }
                } else {
                    console.error("Erreur serveur", await response.text());
                    btn.innerHTML = '<i class="fas fa-times"></i>';
                    btn.style.backgroundColor = '#ef4444';
                    btn.style.color = '#fff';
                    btn.style.opacity = '1';
                    setTimeout(() => {
                        btn.innerHTML = originalHtml;
                        btn.style.backgroundColor = '';
                        btn.style.color = '';
                    }, 3000);
                }
            } catch (err) {
                console.error(err);
                btn.innerHTML = '<i class="fas fa-wifi"></i>';
                btn.style.backgroundColor = '#ef4444';
                btn.style.opacity = '1';
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                    btn.style.backgroundColor = '';
                }, 3000);
            }
        });
    });

    // Intersection Observer for Fade-in Animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card, .solution-item, .hero-content').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Add visible class CSS dynamically
    const style = document.createElement('style');
    style.innerHTML = `
        .visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
    // FAQ Accordion
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const item = question.closest('.faq-item');

            // Close other items (optional, but good UX)
            document.querySelectorAll('.faq-item').forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    otherItem.querySelector('.faq-answer').style.maxHeight = null;
                }
            });

            // Toggle current item
            item.classList.toggle('active');
            const answer = item.querySelector('.faq-answer');

            if (item.classList.contains('active')) {
                answer.style.maxHeight = answer.scrollHeight + "px";
            } else {
                answer.style.maxHeight = null;
            }
        });
    });

    // Number Counter Animation for Hero Stats
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const step = target / (duration / 16); // ~60fps

                let current = 0;
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        entry.target.innerText = Math.ceil(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        entry.target.innerText = target;
                    }
                };

                updateCounter();
                statsObserver.unobserve(entry.target); // Run once
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-number').forEach(stat => {
        statsObserver.observe(stat);
    });

    // Formations Carousel Logic
    const carouselTrack = document.getElementById('formations-track');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    if (carouselTrack && prevBtn && nextBtn) {
        // Calculate scroll amount based on one card width + gap
        const getScrollAmount = () => {
            const card = carouselTrack.querySelector('.solution-card');
            if (card) {
                // width + gap (approx 2rem = 32px depending on base font size)
                return card.offsetWidth + 32;
            }
            return 350; // fallback
        };

        prevBtn.addEventListener('click', () => {
            carouselTrack.parentElement.scrollBy({
                left: -getScrollAmount(),
                behavior: 'smooth'
            });
        });

        nextBtn.addEventListener('click', () => {
            carouselTrack.parentElement.scrollBy({
                left: getScrollAmount(),
                behavior: 'smooth'
            });
        });
    }

    const solCarouselTrack = document.getElementById('solutions-track');
    const solPrevBtn = document.querySelector('.prev-btn-solutions');
    const solNextBtn = document.querySelector('.next-btn-solutions');

    if (solCarouselTrack && solPrevBtn && solNextBtn) {
        const getSolScrollAmount = () => {
            const card = solCarouselTrack.querySelector('.solution-card');
            return card ? card.offsetWidth + 32 : 350;
        };
        solPrevBtn.addEventListener('click', () => {
            solCarouselTrack.parentElement.scrollBy({ left: -getSolScrollAmount(), behavior: 'smooth' });
        });
        solNextBtn.addEventListener('click', () => {
            solCarouselTrack.parentElement.scrollBy({ left: getSolScrollAmount(), behavior: 'smooth' });
        });
    }
    // --- Formations Carousel Ends ---

    // Articles Carousel Logic
    const articlesTrack = document.getElementById('articles-track');
    const prevBtnArticles = document.querySelector('.prev-btn-articles');
    const nextBtnArticles = document.querySelector('.next-btn-articles');

    if (articlesTrack && prevBtnArticles && nextBtnArticles) {
        const getArticlesScrollAmount = () => {
            const card = articlesTrack.querySelector('.solution-card');
            if (card) {
                return card.offsetWidth + 32;
            }
            return 350;
        };

        prevBtnArticles.addEventListener('click', () => {
            articlesTrack.parentElement.scrollBy({
                left: -getArticlesScrollAmount(),
                behavior: 'smooth'
            });
        });

        nextBtnArticles.addEventListener('click', () => {
            articlesTrack.parentElement.scrollBy({
                left: getArticlesScrollAmount(),
                behavior: 'smooth'
            });
        });
    }
    // --- Articles Carousel Ends ---

    // Contact Form Dynamic Logic
    const toggleBtns = document.querySelectorAll('.btn-toggle');
    const optionsSolutions = document.getElementById('options-solutions');
    const optionsFormations = document.getElementById('options-formations');

    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            toggleBtns.forEach(b => b.classList.remove('active'));
            // Add to clicked
            btn.classList.add('active');

            // Show corresponding options
            const type = btn.getAttribute('data-type');
            if (type === 'solutions') {
                optionsFormations.classList.add('hidden');
                optionsSolutions.classList.remove('hidden');
            } else {
                optionsSolutions.classList.add('hidden');
                optionsFormations.classList.remove('hidden');
            }
        });
    });

    // Global Success Modal Logic
    window.showSuccessModal = function (title, message) {
        let modal = document.getElementById('global-success-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'global-success-modal';
            modal.className = 'success-modal-overlay';
            modal.innerHTML = `
                <div class="success-modal-content">
                    <div class="success-modal-icon">
                        <i class="fas fa-check"></i>
                    </div>
                    <h3 id="success-modal-title"></h3>
                    <p id="success-modal-message"></p>
                    <button class="success-modal-close" onclick="closeSuccessModal()">Fermer</button>
                </div>
            `;
            // Add click-to-close on overlay background
            modal.addEventListener('click', (e) => {
                if (e.target === modal) closeSuccessModal();
            });
            document.body.appendChild(modal);
        }

        document.getElementById('success-modal-title').innerText = title;
        document.getElementById('success-modal-message').innerText = message;

        // Timeout to ensure display transition
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
    }

    window.closeSuccessModal = function () {
        const modal = document.getElementById('global-success-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    };

    // Intercept clicks on links containing ?formation= to store in sessionStorage (prevents loss on redirect)
    document.addEventListener('click', function (e) {
        const link = e.target.closest('a');
        if (link && link.href && link.href.includes('formation=')) {
            try {
                const url = new URL(link.href, window.location.href);
                if (url.searchParams.has('formation')) {
                    sessionStorage.setItem('preselect_formation', url.searchParams.get('formation'));
                }
            } catch (err) { }
        }
    });

    // Auto-select formation from URL parameter OR sessionStorage
    const urlParams = new URLSearchParams(window.location.search);
    let formationParam = urlParams.get('formation');

    // Check sessionStorage as fallback
    if (!formationParam) {
        formationParam = sessionStorage.getItem('preselect_formation');
    }

    if (formationParam && document.getElementById('contactForm')) {
        // Switch to "Formations" tab
        const formationsToggle = document.querySelector('.btn-toggle[data-type="formations"]');
        if (formationsToggle) {
            formationsToggle.click();
        }

        // Check the specific formation checkbox
        const formationCheckbox = document.querySelector(`input[name="formation_type"][value="${formationParam}"]`);
        if (formationCheckbox) {
            formationCheckbox.checked = true;
        }

        // Clear memory
        sessionStorage.removeItem('preselect_formation');

        // Scroll to form to make it obvious
        setTimeout(() => {
            const contactSection = document.getElementById('contact');
            if (contactSection) {
                contactSection.scrollIntoView({ behavior: 'smooth' });
            }
        }, 500);
    }

    // FAQ Toggle "Voir plus"
    const toggleFaqBtn = document.getElementById('toggle-faq-btn');
    if (toggleFaqBtn) {
        toggleFaqBtn.addEventListener('click', () => {
            const faqSection = document.getElementById('faq');
            if (faqSection) {
                faqSection.classList.toggle('show-all');
                if (faqSection.classList.contains('show-all')) {
                    toggleFaqBtn.innerHTML = 'Voir moins <i class="fas fa-chevron-up" style="margin-left: 0.5rem;"></i>';
                } else {
                    toggleFaqBtn.innerHTML = 'Voir tout <i class="fas fa-chevron-down" style="margin-left: 0.5rem;"></i>';
                }
            }
        });
    }

    // --- Floating AI Widget Injection & Logic ---
    const injectFloatingWidget = () => {
        const widgetHTML = `
            <div class="floating-widget-container">
                <div class="floating-widget-popup" id="ai-widget-popup">
                    <div class="floating-widget-header">
                        <div class="success-modal-icon" style="width: 30px; height: 30px; font-size: 14px; margin: 0;">
                            <i class="fas fa-sparkles"></i>
                        </div>
                        <span>Assistant IA Premium</span>
                    </div>
                    <div class="floating-widget-body">
                        <p>Optimisez votre relation client avec nos solutions d'IA sur-mesure. Découvrez comment nous aidons les marques d'exception.</p>
                        <a href="#contact" class="floating-widget-cta" id="widget-cta">Demander un Audit Design</a>
                    </div>
                </div>
                <button class="floating-widget-btn" id="ai-widget-btn">
                    <i class="fas fa-robot"></i>
                    <div class="floating-widget-badge">1</div>
                </button>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);

        const btn = document.getElementById('ai-widget-btn');
        const popup = document.getElementById('ai-widget-popup');
        const cta = document.getElementById('widget-cta');

        if (btn && popup) {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                popup.classList.toggle('active');
                // Hide badge when opened
                const badge = btn.querySelector('.floating-widget-badge');
                if (badge) badge.style.display = 'none';
            });

            // Close when clicking outside
            document.addEventListener('click', (e) => {
                if (!popup.contains(e.target) && !btn.contains(e.target)) {
                    popup.classList.remove('active');
                }
            });

            // Special CTA behavior
            cta.addEventListener('click', () => {
                popup.classList.remove('active');
                // Pre-fill or focus logic could go here
            });
        }
    };

    // Delay appearance for better UX
    setTimeout(injectFloatingWidget, 3000);

    // --- Devis Form Submission (Video IA Pro) ---
    const devisForm = document.getElementById('devisForm');
    if (devisForm) {
        devisForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = devisForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Envoi en cours...';
            btn.disabled = true;

            const payload = {
                first_name: document.getElementById('devis-firstname').value,
                last_name: document.getElementById('devis-lastname').value,
                email: document.getElementById('devis-email').value,
                phone: document.getElementById('devis-phone').value || null,
                need_type: 'formations',
                sub_need: `video_ia_pro (participants: ${document.getElementById('devis-participants').value}, secteur: ${document.getElementById('devis-sector').value}, message: ${document.getElementById('devis-message').value || 'none'})`
            };

            try {
                const response = await fetch(`${SUPABASE_URL}/rest/v1/contacts`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    devisForm.reset();
                    // Email notification
                    sendEmailNotification('Demande de devis - Vidéo IA Pro', {
                        Nom: payload.last_name,
                        Prenom: payload.first_name,
                        Email: payload.email,
                        Telephone: payload.phone,
                        Participants: document.getElementById('devis-participants').value,
                        Secteur: document.getElementById('devis-sector').value,
                        Message: document.getElementById('devis-message').value
                    });
                    if (window.closeModal) {
                        window.closeModal('devis-modal');
                    } else {
                        const modal = document.getElementById('devis-modal');
                        if (modal) modal.classList.remove('active');
                    }
                    if (window.showSuccessModal) {
                        window.showSuccessModal(
                            "Merci !",
                            "Notre équipe vous contacte sous 24h. Votre brochure arrive par email."
                        );
                    }
                } else {
                    throw new Error('Server error');
                }
            } catch (err) {
                console.error(err);
                btn.innerText = 'Erreur lors de l\'envoi ❌';
                btn.style.backgroundColor = '#ef4444';
                btn.style.color = '#fff';
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.color = '';
                    btn.disabled = false;
                }, 4000);
            } finally {
                btn.disabled = false;
            }
        });
    }

    // --- Beta Form Submission (Video IA Pro) ---
    const betaForm = document.getElementById('betaForm');
    if (betaForm) {
        betaForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = betaForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Envoi en cours...';
            btn.disabled = true;

            const payload = {
                nom: document.getElementById('beta-lastname').value,
                prenom: document.getElementById('beta-firstname').value,
                email: document.getElementById('beta-email').value,
                telephone: document.getElementById('beta-phone').value || null,
                entreprise: document.getElementById('beta-company').value || null,
                profil: document.getElementById('beta-profile').value,
                motivation: document.getElementById('beta-motivation').value,
                date_souhaitee: (document.querySelector('input[name="beta-date"]:checked') || {}).value || 'Non précisée'
            };

            try {
                const response = await fetch(`${SUPABASE_URL}/rest/v1/beta_testers_video_ia`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    betaForm.reset();
                    // Email notification
                    sendEmailNotification('Inscription Master Class - Vidéo IA Pro', {
                        Nom: payload.nom,
                        Prenom: payload.prenom,
                        Email: payload.email,
                        Telephone: payload.telephone,
                        Entreprise: payload.entreprise,
                        Profil: payload.profil,
                        Date_souhaitee: payload.date_souhaitee,
                        Motivation: payload.motivation
                    });
                    if (window.closeModal) {
                        window.closeModal('beta-modal');
                    } else {
                        const modal = document.getElementById('beta-modal');
                        if (modal) modal.classList.remove('active');
                    }
                    if (window.showSuccessModal) {
                        window.showSuccessModal(
                            "Merci !",
                            "Merci ! On vous contacte vite pour la prochaine session."
                        );
                    }
                } else {
                    throw new Error('Server error');
                }
            } catch (err) {
                console.error(err);
                btn.innerText = 'Erreur lors de l\'envoi ❌';
                btn.style.backgroundColor = '#ef4444';
                btn.style.color = '#fff';
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.color = '';
                    btn.disabled = false;
                }, 4000);
            } finally {
                btn.disabled = false;
            }
        });
    }

    // --- Inscription Form Submission (Video IA Pro) ---
    const inscriptionForm = document.getElementById('inscriptionForm');
    if (inscriptionForm) {
        const accomCheckModal = document.getElementById('inscription-accom-check');
        const priceDisplayModal = document.getElementById('inscription-total-price');
        
        if (accomCheckModal && priceDisplayModal) {
            accomCheckModal.addEventListener('change', () => {
                if (accomCheckModal.checked) {
                    priceDisplayModal.innerText = "1 690 €";
                } else {
                    priceDisplayModal.innerText = "1 490 €";
                }
            });
        }

        inscriptionForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = inscriptionForm.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Redirection vers le paiement...';
            btn.disabled = true;

            const hasAccompaniment = accomCheckModal ? accomCheckModal.checked : false;

            const payload = {
                first_name: document.getElementById('inscription-firstname').value,
                last_name: document.getElementById('inscription-lastname').value,
                email: document.getElementById('inscription-email').value,
                phone: document.getElementById('inscription-phone').value || null,
                need_type: 'formations',
                sub_need: `video_ia_pro (inscription, accompagnement: ${hasAccompaniment ? 'oui (+200€)' : 'non'}, entreprise: ${document.getElementById('inscription-company').value || 'none'})`
            };

            try {
                // Save lead in Supabase contacts table
                await fetch(`${SUPABASE_URL}/rest/v1/contacts`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'apikey': SUPABASE_KEY,
                        'Authorization': `Bearer ${SUPABASE_KEY}`,
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify(payload)
                });
            } catch (err) {
                console.error("Failed to save contact lead, redirecting anyway", err);
            }

            // Send email notification via Web3Forms
            sendEmailNotification('Nouvelle Inscription - Vidéo IA Pro', {
                Nom: payload.last_name,
                Prenom: payload.first_name,
                Email: payload.email,
                Telephone: payload.phone,
                Entreprise: document.getElementById('inscription-company').value,
                Accompagnement: hasAccompaniment ? 'Oui (+200€)' : 'Non'
            });

            // Redirect to correct Qonto payment link
            const redirectUrl = hasAccompaniment
                ? "https://pay.qonto.com/payment-links/019ea75f-1598-7712-b7bd-366a2717e45b?resource_id=019ea75f-1599-716a-a443-af8790d1da24"
                : "https://pay.qonto.com/payment-links/019ea68d-6c74-74a5-be80-0efc49b6f60b?resource_id=019ea68d-6c75-7048-a57f-5f6b9e044645";
            window.location.href = redirectUrl;
        });
    }

});

