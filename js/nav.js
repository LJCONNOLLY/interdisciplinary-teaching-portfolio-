// Scroll-spy for the teaching-philosophy page's in-page sub-nav: marks the
// link for the section currently in view with a terracotta rule. Cross-page
// nav uses a static aria-current="page" set in each file instead, since
// scrolling across separate pages doesn't apply. A no-op on any page
// without a .philosophy-subnav.
(function () {
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.philosophy-subnav a')
  );
  if (!navLinks.length || !('IntersectionObserver' in window)) return;

  var linksById = {};
  navLinks.forEach(function (link) {
    var id = link.getAttribute('href').slice(1);
    (linksById[id] = linksById[id] || []).push(link);
  });

  var targets = Object.keys(linksById)
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (!targets.length) return;

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (l) { l.classList.remove('is-active'); l.removeAttribute('aria-current'); });
        (linksById[entry.target.id] || []).forEach(function (l) {
          l.classList.add('is-active');
          l.setAttribute('aria-current', 'true');
        });
      });
    },
    { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
  );

  targets.forEach(function (t) { observer.observe(t); });
})();
