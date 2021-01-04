const backdrop = document.querySelector('.backdrop');
const modal = document.querySelector('.my_modal');
const modalNoButton = document.getElementById('modal__action--negative');
const modalMessage = document.getElementById('modal__message');

function closeModal() {
  modal.classList.remove('open');
  setTimeout(() => {
    backdrop.classList.remove('open');
    modal.style.zIndex = -50;
    modalMessage.innerHTML = '';
    // left only btn class to the button
    modalNoButton.className = 'btn';
  }, 100);
}

function openModal(msg, btnClass) {
  modalNoButton.classList.add(btnClass);
  modal.classList.add('open');
  backdrop.classList.add('open');
  modal.style.zIndex = 200;
  modalMessage.innerHTML = msg;
  //   close after 5s
  setTimeout(() => {
    closeModal();
  }, 5000);
}

// close modal when clicked
modalNoButton.addEventListener('click', closeModal);
backdrop.addEventListener('click', closeModal);
