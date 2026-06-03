// Consolidated: focus first errored field + clear field-error styling
document.body.addEventListener('htmx:afterSwap', function (evt) {
  if (!evt.target || evt.target.id !== 'wizard-container') return;

  // Focus first errored field
  var banner = evt.target.querySelector('[data-form-errors]');
  if (banner) {
    var firstLi = banner.querySelector('li[data-field]');
    if (firstLi) {
      var rowIdx = firstLi.getAttribute('data-row');
      var fieldKey = firstLi.getAttribute('data-field');
      if (rowIdx && fieldKey && fieldKey !== '__sheet__') {
        var el = evt.target.querySelector('[name="' + fieldKey + '_' + rowIdx + '"]');
        if (el) {
          el.focus();
          el.scrollIntoView({ block: 'center', behavior: 'smooth' });
        }
      }
    }
  }

  // Clear field-error styling on input
  var form = evt.target.querySelector('form');
  if (form) {
    form.addEventListener('input', function (e) {
      var field = e.target;
      if (field.classList.contains('field-error')) {
        field.classList.remove('field-error');
      }
      var remaining = form.querySelectorAll('.field-error');
      var banner = form.querySelector('[data-form-errors]');
      if (remaining.length === 0 && banner) {
        banner.style.display = 'none';
      }
    });
  }
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
