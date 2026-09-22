// Preference behavior in browsers that block storage, follow system changes, or open multiple tabs.
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const source = readFileSync(new URL('../js/theme.js', `file://${__filename}`), 'utf8');
function setup({saved = null, dark = false, blocked = false} = {}) {
  const events = {}, docEvents = {}, controlEvents = {};
  const meta = {}, select = {disabled: true}, root = {dataset: {}};
  const media = {matches: dark, addEventListener: (type, fn) => events.media = fn};
  const writes = [];
  vm.runInNewContext(source, {
    window: {matchMedia: () => media, addEventListener: (type, fn) => events[type] = fn},
    document: {documentElement: root, querySelector: selector => selector === '#theme-select' ? select : meta, addEventListener: (type, fn) => docEvents[type] = fn},
    localStorage: {getItem: () => {if(blocked) throw Error('Blocked'); return saved;}, setItem: (key,value) => {if(blocked) throw Error('Blocked'); writes.push([key,value]);}}
  });
  select.addEventListener = (type, fn) => controlEvents[type] = fn;
  docEvents.DOMContentLoaded();
  return {root, media, meta, select, writes, events, choose: value => {select.value=value;controlEvents.change();}};
}
let state = setup();
assert.equal(state.root.dataset.theme, 'light');
assert.equal(state.select.value, 'system');
assert.equal(state.select.disabled, false);
state.media.matches = true; state.events.media();
assert.equal(state.root.dataset.theme, 'dark');
state.choose('light');
assert.deepEqual(state.writes, [['fcp-theme', 'light']]);
state.events.media();
assert.equal(state.root.dataset.theme, 'light');
assert.equal(state.meta.content, '#f7f7ef');
state.events.storage({key: 'fcp-theme', newValue: 'dark'});
assert.equal(state.root.dataset.theme, 'dark');
state.events.storage({key: null, newValue: null});
assert.equal(state.select.value, 'system');
state = setup({saved:'<script>alert(1)</script>'});
assert.equal(state.select.value, 'system');
state = setup({saved:'dark'});
assert.equal(state.root.dataset.theme, 'dark');
state = setup({blocked:true});
state.choose('dark');
assert.equal(state.root.dataset.theme, 'dark');
console.log('Theme checks passed: system changes, persistence, cross-tab updates, invalid values and unavailable storage.');
