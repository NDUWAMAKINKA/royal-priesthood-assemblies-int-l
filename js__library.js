/*
 * Library filters.
 *
 * The library ships as complete HTML, so every recording and link is usable
 * before this file runs and stays usable if JavaScript is blocked. This script
 * only narrows the visible cards, which keeps the page fast and dependable.
 */
(function () {
  'use strict';

  var root = document.querySelector('[data-library]');
  if (!root) return;

  var items = Array.prototype.slice.call(
    root.querySelectorAll('[data-library-item]')
  );
  var search = root.querySelector('[data-library-search]');
  var clear = root.querySelector('[data-library-clear]');
  var filters = Array.prototype.slice.call(
    root.querySelectorAll('[data-library-filter]')
  );
  var count = root.querySelector('[data-library-count]');
  var empty = root.querySelector('[data-library-empty]');
  var activeCategory = 'all';

  function normalise(value) {
    var text = String(value || '').toLowerCase();
    if (typeof text.normalize === 'function') {
      text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }
    return text.trim();
  }

  function itemText(item) {
    var original = item.getAttribute('data-search') || '';
    var visible = item.textContent || '';
    return normalise(original + ' ' + visible);
  }

  function apply() {
    var query = normalise(search ? search.value : '');
    var visible = 0;

    items.forEach(function (item) {
      var matchesCategory =
        activeCategory === 'all' ||
        item.getAttribute('data-category') === activeCategory;
      var matchesQuery = !query || itemText(item).indexOf(query) !== -1;
      var show = matchesCategory && matchesQuery;
      item.hidden = !show;
      if (show) visible += 1;
    });

    if (count) {
      count.textContent =
        visible === items.length
          ? 'Showing all ' + items.length + ' resources'
          : 'Showing ' + visible + ' of ' + items.length + ' resources';
    }

    if (empty) empty.hidden = visible !== 0;
    if (clear) clear.hidden = !query;

    filters.forEach(function (button) {
      var active = button.getAttribute('data-library-filter') === activeCategory;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }

  filters.forEach(function (button) {
    button.addEventListener('click', function () {
      activeCategory = button.getAttribute('data-library-filter') || 'all';
      apply();
    });
  });

  if (search) {
    search.addEventListener('input', apply);
  }

  if (clear) {
    clear.addEventListener('click', function () {
      if (!search) return;
      search.value = '';
      search.focus();
      apply();
    });
  }

  apply();
})();
