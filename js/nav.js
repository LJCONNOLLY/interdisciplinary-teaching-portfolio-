// Scroll-spy: marks the nav link for the section currently in view with
// an --ink rule. The only motion on the page besides native smooth scroll.
(function () {
  var navLinks = Array.prototype.slice.call(
    document.querySelectorAll('.site-nav__links a, .philosophy-subnav a')
  );
  if (!navLinks.length) return;

  var linksById = {};
  navLinks.forEach(function (link) {
    var id = link.getAttribute('href').slice(1);
    (linksById[id] = linksById[id] || []).push(link);
  });

  var targets = Object.keys(linksById)
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (!targets.length || !('IntersectionObserver' in window)) return;

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        var links = linksById[entry.target.id] || [];
        links.forEach(function (link) {
          if (entry.isIntersecting) {
            navLinks.forEach(function (l) { l.classList.remove('is-active'); l.removeAttribute('aria-current'); });
            links.forEach(function (l) { l.classList.add('is-active'); l.setAttribute('aria-current', 'true'); });
          }
        });
      });
    },
    { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
  );

  targets.forEach(function (t) { observer.observe(t); });
})();
