// Animation for active buttons

const buttons = document.querySelectorAll('.buttons');

buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    buttons.forEach(b => b.classList.remove('active')); // remove from all
    btn.classList.add('active'); // add to clicked
  });
});

// Animation for sidebar and overlays

const sidebar = document.querySelector('.sidebar');
const openBtn = document.getElementById('open-menu');
const closeBtn = document.getElementById('close-menu');
const overlay = document.getElementById('overlay');

document.addEventListener("DOMContentLoaded", () => {
  sidebar.classList.add("collapsed");

  openBtn.addEventListener("click", () => {
    sidebar.classList.remove("collapsed");
    sidebar.classList.add("open");
    overlay.classList.add("visible");
  });

  closeBtn.addEventListener("click", () => {
    sidebar.classList.add("collapsed");
    sidebar.classList.remove("open");
    overlay.classList.remove("visible");
  });

  overlay.addEventListener("click", () => {
    sidebar.classList.add("collapsed");
    sidebar.classList.remove("open");
    overlay.classList.remove("visible");
  });
});