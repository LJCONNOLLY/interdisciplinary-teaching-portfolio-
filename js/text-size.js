// Accessible text-size control. Scales the html root font-size, so every
// rem-based size on the page (which is all of them) scales together.
// Persists across pages/visits via localStorage.
(function () {
  var STEPS = [100, 115, 130, 145, 160];
  var STORAGE_KEY = 'portfolio-text-scale';
  var root = document.documentElement;

  function currentIndex() {
    var stored = parseInt(localStorage.getItem(STORAGE_KEY), 10);
    var idx = STEPS.indexOf(stored);
    return idx === -1 ? 0 : idx;
  }

  function apply(idx) {
    idx = Math.max(0, Math.min(STEPS.length - 1, idx));
    root.style.fontSize = STEPS[idx] + '%';
    localStorage.setItem(STORAGE_KEY, STEPS[idx]);
    return idx;
  }

  // apply saved scale immediately (before controls exist) to avoid flicker
  var idx = apply(currentIndex());

  document.addEventListener('DOMContentLoaded', function () {
    var dec = document.getElementById('text-size-dec');
    var inc = document.getElementById('text-size-inc');
    var reset = document.getElementById('text-size-reset');
    if (!dec || !inc || !reset) return;

    dec.addEventListener('click', function () { idx = apply(idx - 1); });
    inc.addEventListener('click', function () { idx = apply(idx + 1); });
    reset.addEventListener('click', function () { idx = apply(0); });
  });
})();
