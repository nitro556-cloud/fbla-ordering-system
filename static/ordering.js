/* Progressive enhancement only: Flask validates quantities and calculates totals. */
document.querySelectorAll('.quantity-control').forEach(control => {
  const input = control.querySelector('input');
  const buttons = [...control.querySelectorAll('[data-step]')];
  const refresh = () => buttons.forEach(button => {
    const value = Number(input.value);
    button.disabled = input.disabled || (Number(button.dataset.step) < 0
      ? value <= Number(input.min) : value >= Number(input.max));
  });
  buttons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      if (!input.checkValidity()) input.value = input.min;
      else if (Number(button.dataset.step) > 0) input.stepUp();
      else input.stepDown();
      input.dispatchEvent(new Event('input', {bubbles: true}));
      input.dispatchEvent(new Event('change', {bubbles: true}));
    });
  });
  input.addEventListener('input', refresh);
  refresh();
});
const settingsForm = document.querySelector('[data-settings-form]');
if (settingsForm) {
  settingsForm.addEventListener('input', () => {
    settingsForm.querySelector('[data-preview-status]').textContent = 'Your choices changed. Select Update total to review the new amount before placing your order.';
    settingsForm.querySelector('.total-preview').classList.add('is-stale');
  });
}
document.querySelectorAll('.cart-quantity-form input[name="quantity"]').forEach(input => {
  input.addEventListener('input', () => {
    const button = input.closest('form').querySelector('button.secondary');
    button.textContent = 'Save quantity';
  });
});
// Native details keeps secondary navigation usable without JavaScript.
const moreNav = document.querySelector('.more-nav');
if (moreNav) {
  document.addEventListener('click', event => { if (!moreNav.contains(event.target)) moreNav.open = false; });
  moreNav.addEventListener('keydown', event => {
    if (event.key === 'Escape') { moreNav.open = false; moreNav.querySelector('summary').focus(); }
  });
}
