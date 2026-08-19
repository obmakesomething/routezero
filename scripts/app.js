/**
 * ROUTEZERO EDITORIAL CLIENT SCRIPT
 * - Reading Progress Bar
 * - Newsletter Subscription Form Handling
 * - Email Copy Interaction & Feedback Toast
 * - Smooth Back to Top
 * - GA4 Telemetry
 */

document.addEventListener('DOMContentLoaded', () => {
  initReadingProgress();
  initEmailCopy();
  initNewsletter();
  initBackToTop();
});

/**
 * 1. Reading Progress Bar
 */
function initReadingProgress() {
  const progressBar = document.getElementById('reading-progress');
  if (!progressBar) return;

  function updateProgress() {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight <= 0) {
      progressBar.style.width = '0%';
      return;
    }
    const currentProgress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = `${Math.min(100, Math.max(0, currentProgress))}%`;
  }

  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
}

/**
 * 2. Email Copy Interaction
 */
function initEmailCopy() {
  const emailLink = document.getElementById('email-link');
  const toast = document.getElementById('toast');
  const emailToCopy = 'krrootzero@gmail.com';

  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }

  if (emailLink) {
    emailLink.addEventListener('click', async (e) => {
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
        window.location.href = `mailto:${emailToCopy}`;
      }
    });
  }
}

/**
 * 3. Newsletter Subscription
 */
function initNewsletter() {
  const form = document.getElementById('newsletter-form');
  const emailInput = document.getElementById('newsletter-email');
  const submitBtn = document.getElementById('newsletter-submit');
  const feedback = document.getElementById('form-feedback');
  const toast = document.getElementById('toast');

  if (!form || !emailInput) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();

    if (!email || !email.includes('@')) {
      feedback.textContent = '올바른 이메일 주소를 입력해 주세요.';
      feedback.className = 'form-feedback error';
      return;
    }

    // Save locally for subscription tracking
    try {
      const subscribers = JSON.parse(localStorage.getItem('routezero_subscribers') || '[]');
      if (!subscribers.includes(email)) {
        subscribers.push(email);
        localStorage.setItem('routezero_subscribers', JSON.stringify(subscribers));
      }
    } catch (e) {
      console.warn('Storage fallback: ', e);
    }

    // GA4 Telemetry Event
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'newsletter_signup', {
        email_hash: email
      });
    }

    // Success State
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>구독 완료 ✓</span>';
    emailInput.disabled = true;
    
    feedback.textContent = '구독해 주셔서 감사합니다. 새로운 글이 발행되면 이메일로 전해드릴게요.';
    feedback.className = 'form-feedback success';

    if (toast) {
      toast.textContent = '뉴스레터 구독이 완료되었습니다!';
      toast.classList.add('show');
      setTimeout(() => {
        toast.classList.remove('show');
      }, 3000);
    }
  });
}

/**
 * 4. Smooth Back to Top
 */
function initBackToTop() {
  const topBtn = document.getElementById('back-to-top');
  if (topBtn) {
    topBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
}
