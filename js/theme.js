/* Apply before the stylesheet to avoid a flash. No cookies or network requests. */
(() => {
  'use strict';
  const key = 'fcp-theme';
  const valid = value => ['light', 'dark', 'system'].includes(value) ? value : 'system';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = 'system';
  try { preference = valid(localStorage.getItem(key)); } catch (_) { /* Storage may be disabled. */ }
  function apply() {
    const theme = preference === 'system' ? (system.matches ? 'dark' : 'light') : preference;
    document.documentElement.dataset.theme = theme;
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'dark' ? '#17121f' : '#faf7ff';
    const select = document.querySelector('#theme-select');
    if (select) select.value = preference;
  }
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) { preference = valid(event.newValue); apply(); }
  });
  document.addEventListener('DOMContentLoaded', () => {
    apply();
    const select = document.querySelector('#theme-select');
    if (select) {
      select.disabled = false;
      select.addEventListener('change', () => {
        preference = valid(select.value);
        try { localStorage.setItem(key, preference); } catch (_) { /* Still works for this page. */ }
        apply();
      });
    }
  });
})();
