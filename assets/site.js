// Hybrid AutoPress: scroll behaviour. No dependencies.
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");
  var calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Reveal: elements rise into place once, when they enter the viewport.
  var reveals = document.querySelectorAll(".reveal");
  if (calm || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); seen.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { seen.observe(el); });
    // The first screen does not wait for the observer.
    document.querySelectorAll(".hero .reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  // Pinned stage: the step crossing the middle of the viewport picks the screenshot.
  var steps = document.querySelectorAll(".step");
  var shots = document.querySelectorAll(".stage__frame img");
  var dots = document.querySelectorAll(".stage__dots i");
  function show(index) {
    shots.forEach(function (img, i) { img.classList.toggle("is-active", i === index); });
    dots.forEach(function (dot, i) { dot.classList.toggle("is-active", i === index); });
  }
  if (steps.length && "IntersectionObserver" in window) {
    var middle = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) show(Number(entry.target.dataset.step));
      });
    }, { rootMargin: "-50% 0px -50% 0px" });
    steps.forEach(function (step) { middle.observe(step); });
  }

  // Hero: the window grows a little towards the reader while the first screen scrolls away.
  var hero = document.querySelector(".hero__shot");
  if (hero && !calm) {
    var ticking = false;
    var update = function () {
      var progress = Math.min(1, Math.max(0, window.scrollY / (window.innerHeight * 0.8)));
      hero.style.setProperty("--hero-scale", (0.94 + progress * 0.08).toFixed(4));
      ticking = false;
    };
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }
})();
