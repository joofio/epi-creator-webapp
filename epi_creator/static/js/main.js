// Focus the first errored field after an htmx swap so users see where
// to act, replacing the browser's native autofocus behaviour
// (suppressed because the wizard uses novalidate).
document.body.addEventListener('htmx:afterSwap', function (evt) {
  if (!evt.target || evt.target.id !== 'wizard-container') return;
  var banner = evt.target.querySelector('[data-form-errors]');
  if (!banner) return;
  var firstLi = banner.querySelector('li[data-field]');
  if (!firstLi) return;
  var rowIdx = firstLi.getAttribute('data-row');
  var fieldKey = firstLi.getAttribute('data-field');
  if (!rowIdx || !fieldKey || fieldKey === '__sheet__') return;
  // Form input names are suffixed with the row index: "name_0", "role_1", etc.
  var selector = '[name="' + fieldKey + '_' + rowIdx + '"]';
  var el = evt.target.querySelector(selector);
  if (el) {
    el.focus();
    if (typeof el.scrollIntoView === 'function') {
      el.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
  }
});
