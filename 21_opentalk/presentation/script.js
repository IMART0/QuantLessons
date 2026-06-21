// JS для презентации - ЛФМШ "Квант"

document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.slide');
  const nextBtn = document.getElementById('next-btn');
  const prevBtn = document.getElementById('prev-btn');
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const counter = document.getElementById('slide-counter');
  const progressBar = document.getElementById('progress-bar');
  
  let currentSlideIndex = 0;

  function updateSlides() {
    slides.forEach((slide, index) => {
      if (index === currentSlideIndex) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    // Обновление счетчика
    if (counter) {
      counter.textContent = `${currentSlideIndex + 1} / ${slides.length}`;
    }

    // Обновление прогресс-бара
    if (progressBar) {
      const percentage = ((currentSlideIndex + 1) / slides.length) * 100;
      progressBar.style.width = `${percentage}%`;
    }
  }

  function nextSlide() {
    if (currentSlideIndex < slides.length - 1) {
      currentSlideIndex++;
      updateSlides();
    }
  }

  function prevSlide() {
    if (currentSlideIndex > 0) {
      currentSlideIndex--;
      updateSlides();
    }
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.error(`Ошибка перевода в полноэкранный режим: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  }

  // Обработчики кнопок
  if (nextBtn) nextBtn.addEventListener('click', nextSlide);
  if (prevBtn) prevBtn.addEventListener('click', prevSlide);
  if (fullscreenBtn) fullscreenBtn.addEventListener('click', toggleFullscreen);

  // Клавиатурная навигация
  document.addEventListener('keydown', (e) => {
    switch(e.key) {
      case 'ArrowRight':
      case ' ':
      case 'PageDown':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'f':
      case 'F':
        toggleFullscreen();
        break;
    }
  });

  // Инициализация
  updateSlides();
});
