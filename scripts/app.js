/**
 * ROUTEZERO CLIENT SCRIPT
 * - Scroll Spy for desktop & mobile navigation
 * - Seoul (KST) Live Clock
 * - Email clipboard copy with visual toast
 * - Ambient cursor glow (desktop pointer)
 * - Smooth scroll & Back to top
 * - GA4 event telemetry
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollSpy();
  initLiveClock();
  initEmailCopy();
  initCursorGlow();
  initAnalytics();
  initBackToTop();
});

/**
 * 1. Unified Scroll Spy for Desktop & Mobile Navigation
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('main > section[id]');
  const navItems = document.querySelectorAll('.nav-item, .mobile-nav-item');

  if (!sections.length || !navItems.length) return;

  const observerOptions = {
    root: null,
    rootMargin: '-20% 0px -50% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');

        navItems.forEach((link) => {
          const targetId = link.getAttribute('href')?.replace('#', '');
          if (targetId === id) {
            link.classList.add('active');
            // Scroll mobile nav container if needed
            const mobileNav = link.closest('.mobile-nav-track');
            if (mobileNav) {
              const linkRect = link.getBoundingClientRect();
              const navRect = mobileNav.getBoundingClientRect();
              if (linkRect.left < navRect.left || linkRect.right > navRect.right) {
                link.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
              }
            }
          } else {
            link.classList.remove('active');
          }
        });

        // Telemetry: Section view event
        if (typeof window.gtag === 'function') {
          window.gtag('event', 'section_view', {
            section_id: id
          });
        }
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));
}

/**
 * 2. Real-time Seoul (KST) Clock
 */
function initLiveClock() {
  const clockEl = document.getElementById('seoul-clock');
  if (!clockEl) return;

  function updateClock() {
    try {
      const now = new Date();
      const options = {
        timeZone: 'Asia/Seoul',
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      };
      const timeString = new Intl.DateTimeFormat('ko-KR', options).format(now);
      clockEl.textContent = `SEOUL: ${timeString} KST`;
    } catch (e) {
      const now = new Date();
      clockEl.textContent = `SEOUL: ${now.toTimeString().split(' ')[0]} KST`;
    }
  }

  updateClock();
  setInterval(updateClock, 1000);
}

/**
 * 3. Email Copy to Clipboard Interaction
 */
function initEmailCopy() {
  const copyButtons = document.querySelectorAll('[data-copy-email], #email-badge, #footer-email-link');
  const toast = document.getElementById('toast');
  const emailToCopy = 'krrootzero@gmail.com';

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2400);
  }

  copyButtons.forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        await navigator.clipboard.writeText(emailToCopy);
        showToast('이메일 주소가 복사되었습니다! (krrootzero@gmail.com)');
        
        if (typeof window.gtag === 'function') {
          window.gtag('event', 'copy_email', {
            email: emailToCopy
          });
        }
      } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = emailToCopy;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          showToast('이메일 주소가 복사되었습니다! (krrootzero@gmail.com)');
        } catch (e2) {
          window.location.href = `mailto:${emailToCopy}`;
        }
        document.body.removeChild(textarea);
      }
    });
  });
}

/**
 * 4. Ambient Cursor Glow (Desktop Fine Pointers Only)
 */
function initCursorGlow() {
  const glow = document.getElementById('cursor-glow');
  if (!glow) return;

  if (window.matchMedia('(pointer: fine)').matches) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;
    let isInside = true;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isInside) {
        isInside = true;
        glow.style.opacity = '1';
      }
    });

    document.addEventListener('mouseleave', () => {
      isInside = false;
      glow.style.opacity = '0';
    });

    function animate() {
      currentX += (mouseX - currentX) * 0.08;
      currentY += (mouseY - currentY) * 0.08;
      glow.style.transform = `translate3d(calc(${currentX}px - 50%), calc(${currentY}px - 50%), 0)`;
      requestAnimationFrame(animate);
    }
    animate();
  } else {
    glow.style.display = 'none';
  }
}

/**
 * 5. Outbound Links Telemetry
 */
function initAnalytics() {
  document.querySelectorAll('a[target="_blank"]').forEach((link) => {
    link.addEventListener('click', () => {
      const url = link.getAttribute('href');
      const label = link.textContent.trim();
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'outbound_click', {
          link_url: url,
          link_label: label
        });
      }
    });
  });
}

/**
 * 6. Smooth Back to Top
 */
function initBackToTop() {
  const topBtn = document.getElementById('back-to-top');
  if (topBtn) {
    topBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
