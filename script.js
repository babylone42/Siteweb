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

    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.background = '#111111';
                navLinks.style.padding = '2rem';
            }
        });
    }

    // Supabase Configuration
    const SUPABASE_URL = 'https://nzkirwiilgdlitbylxxv.supabase.co';
    const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56a2lyd2lpbGdkbGl0YnlseHh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE5NDYxNzIsImV4cCI6MjA4NzUyMjE3Mn0.xad9ed_JK-6goYodSyhhcEEiOdmro0xq2skohjGW7SE';

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

});
