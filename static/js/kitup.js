// static/js/kitup.js
document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-like-btn]");
  if (!btn) return;

  e.preventDefault();
  e.stopPropagation();

  const pressed = btn.getAttribute("aria-pressed") === "true";
  btn.setAttribute("aria-pressed", String(!pressed));
});
