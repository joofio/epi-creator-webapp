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

// Clear field-error styling and error banner when user corrects fields
document.body.addEventListener('htmx:afterSwap', function (evt) {
  if (!evt.target || evt.target.id !== 'wizard-container') return;
  var form = evt.target.querySelector('form');
  if (!form) return;
  form.addEventListener('input', function (e) {
    var field = e.target;
    if (field.classList.contains('field-error')) {
      field.classList.remove('field-error');
    }
    // If no more field-error elements remain, hide the banner
    var remaining = form.querySelectorAll('.field-error');
    var banner = form.querySelector('[data-form-errors]');
    if (remaining.length === 0 && banner) {
      banner.style.display = 'none';
    }
  });
});

// Block submit if any autocomplete has typed-but-unmatched text.
document.body.addEventListener('htmx:beforeRequest', function (evt) {
  var form = evt.target;
  if (!form || form.tagName !== 'FORM') return;
  var bad = [];
  form.querySelectorAll('[x-data*="autocomplete"]').forEach(function (el) {
    var data = Alpine.$data(el);
    if (data && data.noMatch) {
      bad.push(data.labelFieldName || data.idFieldName || '(unknown)');
    }
  });
  if (bad.length) {
    evt.preventDefault();
    alert(
      'These fields have no controlled term match and cannot be saved:\n\n  - ' +
      bad.join('\n  - ') +
      '\n\nPick from the list or clear the field.'
    );
  }
});
