const modal = document.getElementById('myModal');
const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');

// Open modal
openBtn.onclick = () => {
modal.style.display = 'block';
};

// Close modal
closeBtn.onclick = () => {
modal.style.display = 'none';
};

// Close modal if you click outside of it
window.onclick = (e) => {
if (e.target == modal) {
    modal.style.display = 'none';
}
};
