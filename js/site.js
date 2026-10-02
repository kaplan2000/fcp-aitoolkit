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
    const desktop = window.matchMedia('(min-width: 1101px)');
    desktop.addEventListener('change', () => setMenu(false));
  }
  const languages = document.querySelector('.language-picker');
  document.addEventListener('click', event => {
    if (languages && !languages.contains(event.target)) languages.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && languages?.open) {
      languages.open = false;
      languages.querySelector('summary').focus();
    }
  });
  document.querySelectorAll('.language-options a').forEach(link => {
    if (location.hash) link.hash = location.hash;
  });
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

  // 1.1.1 Smart Cache illustration. Text lives in the HTML (translated per language);
  // this only switches states.
  const demo = document.querySelector('.cache-demo');
  if (demo) {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    const run = demo.querySelector('[data-cache="run"]');
    const extend = demo.querySelector('[data-cache="extend"]');
    const reset = demo.querySelector('[data-cache="reset"]');
    let timer = 0;
    const setState = state => {
      demo.dataset.state = state;
      demo.querySelectorAll('[data-msg]').forEach(msg => { msg.hidden = msg.dataset.msg !== state; });
      const busy = state.startsWith('working');
      const started = state !== 'idle';
      run.disabled = busy;
      run.querySelector('.run-first').hidden = started;
      run.querySelector('.run-again').hidden = !started;
      extend.disabled = busy || !started || 'extended' in demo.dataset;
      reset.disabled = busy || !started;
    };
    const work = (state, done, ms) => {
      setState(state);
      timer = window.setTimeout(() => setState(done), reduce.matches ? 0 : ms);
    };
    run.addEventListener('click', () => {
      const state = demo.dataset.state;
      if (state === 'idle') work('working-full', 'done-full', 2600);
      else if (state === 'extended') {
        work('working-part', 'done-part', 1300);
        demo.dataset.extDone = '';
      } else {
        demo.dataset.state = '';
        void demo.offsetWidth; // restart the flash on repeated runs
        setState('cached');
      }
    });
    extend.addEventListener('click', () => {
      demo.dataset.extended = '';
      setState('extended');
    });
    reset.addEventListener('click', () => {
      window.clearTimeout(timer);
      delete demo.dataset.extended;
      delete demo.dataset.extDone;
      setState('idle');
      run.focus();
    });
  }

  // Smart Search illustration: filter the sample captions and mark the match.
  const search = document.querySelector('.caption-search');
  if (search) {
    const card = search.closest('.search-card');
    const rows = [...card.querySelectorAll('.search-results li')];
    const empty = card.querySelector('.search-empty');
    rows.forEach(row => { const text = row.querySelector('.result-text'); text.dataset.plain = text.textContent; });
    search.addEventListener('input', () => {
      const query = search.value.trim().toLocaleLowerCase();
      let shown = 0;
      rows.forEach(row => {
        const text = row.querySelector('.result-text');
        const plain = text.dataset.plain;
        const at = query ? plain.toLocaleLowerCase().indexOf(query) : -1;
        row.hidden = Boolean(query) && at < 0;
        text.textContent = '';
        if (at < 0) text.textContent = plain;
        else {
          const mark = document.createElement('mark');
          mark.textContent = plain.slice(at, at + query.length);
          text.append(plain.slice(0, at), mark, plain.slice(at + query.length));
        }
        if (!row.hidden) shown += 1;
      });
      empty.hidden = shown > 0;
    });
  }
})();
