// static/js/kitup.js

document.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-like-btn]");
  if (!btn) return;

  // 카드 <a> 클릭 방지
  e.preventDefault();
  e.stopPropagation();

  const pressed = btn.getAttribute("aria-pressed") === "true";
  btn.setAttribute("aria-pressed", String(!pressed));
});
