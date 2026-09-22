(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#site-nav');
  if (menuButton && nav) {
    const setMenu = open => {
      menuButton.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    };
    menuButton.hidden = false;
    menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuButton.focus();
      }
    });
    const desktop = window.matchMedia('(min-width: 601px)');
    desktop.addEventListener('change', () => setMenu(false));
  }
  const styles = ['basic', 'highlight', 'background', 'pop', 'beast'];
  const names = ['Basic', 'Highlighted', 'Highlighted with Background', 'Pop', 'Beast Pop'];
  const buttons = document.querySelectorAll('[data-caption-style]');
  let current = 1;
  function selectStyle(index) {
    current = index;
    document.querySelectorAll('[data-style]').forEach(preview => { preview.dataset.style = styles[index]; });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.captionStyle === styles[index])));
    document.querySelectorAll('.active-style-name').forEach(label => { label.textContent = names[index]; });
    const counter = document.querySelector('.preview-top > span:last-child');
    if (counter) counter.textContent = `${String(index + 1).padStart(2, '0')} / 05`;
  }
  buttons.forEach(button => button.addEventListener('click', () => selectStyle(styles.indexOf(button.dataset.captionStyle))));
  document.querySelector('.next-style')?.addEventListener('click', () => selectStyle((current + 1) % styles.length));
  selectStyle(current);
})();
