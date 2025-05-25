// LOGIN modal controls
const loginModal = document.getElementById('loginModal');
const openLoginBtn = document.getElementById('openModalBtn');
const closeLoginBtn = document.getElementById('closeLoginModalBtn');

// REGISTER modal controls
const registerModal = document.getElementById('registerModal');
const closeRegisterBtn = document.getElementById('closeRegisterModalBtn');
const showRegisterBtn = document.getElementById('showRegisterModal');

// Open login modal
openLoginBtn.onclick = () => {
    loginModal.style.display = 'block';
};

// Close login modal
closeLoginBtn.onclick = () => {
    loginModal.style.display = 'none';
};

// Open register modal from "Sign Up" link
showRegisterBtn.onclick = (e) => {
    e.preventDefault(); // Prevent link redirect
    loginModal.style.display = 'none';
    registerModal.style.display = 'block';
};

// Close register modal
closeRegisterBtn.onclick = () => {
    registerModal.style.display = 'none';
};

// Close modals when clicking outside
// window.onclick = (e) => {
//     if (e.target === loginModal) {
//         loginModal.style.display = 'none';
//     }
//     if (e.target === registerModal) {
//         registerModal.style.display = 'none';
//     }
// };


// Show login modal from the "Already have an account?" link
const showLoginBtn = document.getElementById('showLoginModal');

showLoginBtn.onclick = (e) => {
    e.preventDefault();
    registerModal.style.display = 'none';
    loginModal.style.display = 'block';
};


