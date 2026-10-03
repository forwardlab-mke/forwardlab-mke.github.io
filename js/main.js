/* TaLE MKE: minimal vanilla JS (nav toggle, footer year, contact form). */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    // Escape closes the menu and returns focus to the toggle.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus();
      }
    });

    // Close if the viewport grows past the mobile breakpoint.
    window.matchMedia("(min-width: 1181px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  /* ---------- Home hero rotation: pause / play ---------- */
  var heroToggle = document.querySelector(".hero-art-toggle");
  if (heroToggle) {
    heroToggle.addEventListener("click", function () {
      var art = heroToggle.closest(".hero-art");
      var paused = art.classList.toggle("is-paused");
      heroToggle.setAttribute("aria-pressed", String(paused));
      heroToggle.setAttribute("aria-label", paused ? "Play the rotating images" : "Pause the rotating images");
    });
  }

  /* ---------- Footer year ---------- */
  var year = document.getElementById("year");
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- Forms (front end only) ----------
     Applies to every <form class="js-form">. No page uses one right now (Contact uses an
     email button); kept so a form can be added later without new JavaScript.
     ======================================================================
     WIRE IN A FORM HANDLER HERE
     This site has no backend. To receive submissions, sign up for a form
     service (for example Formspree: https://formspree.io), create a form,
     and paste its endpoint below, e.g.
       var FORM_ENDPOINT = "https://formspree.io/f/abcdwxyz";
     Also set the same URL in each <form action="..."> so the forms still
     submit if JavaScript is off. Each form sends a hidden "_form" field
     (e.g. "contact") so one endpoint can serve more than one form.
     While FORM_ENDPOINT is empty, the forms validate input and show a
     notice, but nothing is sent anywhere.
     ====================================================================== */
  var FORM_ENDPOINT = "";

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function isValid(input) {
    if (input.type === "checkbox") return input.checked;
    var v = input.value.trim();
    if (!v) return false;
    if (input.type === "email") return EMAIL_RE.test(v);
    return true;
  }

  function validateField(input) {
    var ok = isValid(input);
    var err = document.getElementById(input.id + "-error");
    input.setAttribute("aria-invalid", ok ? "false" : "true");
    if (err) err.textContent = ok ? "" : (input.getAttribute("data-error") || "This field is required.");
    return ok;
  }

  Array.prototype.forEach.call(document.querySelectorAll("form.js-form"), function (form) {
    var status = form.querySelector(".form-status");
    var required = Array.prototype.slice.call(form.querySelectorAll("[required]"));

    function showStatus(text, kind) {
      status.textContent = text;
      status.className = "form-status " + (kind === "error" ? "is-error" : "is-success");
    }

    required.forEach(function (input) {
      var evt = input.type === "checkbox" ? "change" : "blur";
      input.addEventListener(evt, function () {
        if (input.type === "checkbox" || input.value.trim()) validateField(input);
      });
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.textContent = "";
      status.className = "form-status";

      var firstInvalid = null;
      required.forEach(function (input) {
        if (!validateField(input) && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) {
        firstInvalid.focus();
        return;
      }

      if (!FORM_ENDPOINT) {
        showStatus(
          "Thanks! This form is not connected yet, so nothing was sent. " +
          "Please email us directly at the address on this page.",
          "success"
        );
        return;
      }

      var button = form.querySelector("button[type=submit]");
      button.disabled = true;

      fetch(FORM_ENDPOINT, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed");
          form.reset();
          showStatus("Thanks! We received your message and will be in touch soon.", "success");
        })
        .catch(function () {
          showStatus("Sorry, something went wrong. Please email us directly instead.", "error");
        })
        .then(function () { button.disabled = false; });
    });
  });
})();
