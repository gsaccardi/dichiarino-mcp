/* Copy-to-clipboard for code blocks */
document.querySelectorAll(".copy-btn").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var targetId = btn.getAttribute("data-target");
    var codeEl = document.getElementById(targetId);
    if (!codeEl) return;

    navigator.clipboard.writeText(codeEl.textContent).then(function () {
      btn.textContent = "Copied!";
      btn.classList.add("copied");
      setTimeout(function () {
        btn.textContent = "Copy";
        btn.classList.remove("copied");
      }, 2000);
    });
  });
});

/* Shrink nav on scroll */
var nav = document.querySelector(".nav");
window.addEventListener("scroll", function () {
  if (window.scrollY > 50) {
    nav.style.padding = "0.4rem 0";
  } else {
    nav.style.padding = "0.75rem 0";
  }
});
