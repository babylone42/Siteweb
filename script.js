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

    // Form Submission Handling (Mock)
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = form.querySelector('button');
            const originalText = btn.innerText;

            btn.innerText = 'Envoi en cours...';
            btn.style.opacity = '0.7';

            setTimeout(() => {
                btn.innerText = 'Message envoyé ! ✅';
                btn.style.backgroundColor = '#109B80';
                btn.style.color = '#fff';
                form.reset();
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.opacity = '1';
                }, 3000);
            }, 1500);
        });
    }

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

});
