// bring the parent element
const list = document.getElementById('list-group');

// get inside of the list
function getMailbox(mailbox) {
  // clean emails
  list.innerHTML = '';
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      console.log(emails);
      // ... do something else with emails ...
      emails.forEach((email) => {
        const el = document.createElement('a');
        el.classList.add(
          'list-group-item',
          'list-group-item-action',
          'flex-column',
          'align-items-start'
        );
        el.style.cursor = 'pointer';
        // if unread background must be black
        if (!email.read) {
          el.classList.add('bg-secondary');
        }
        // inside of email, userName comes from inbox.js
        el.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">${
              email.sender === userName ? email.recipients : email.sender
            }</h5>
            <small>${email.timestamp}</small>
          </div>
          <p class="mb-1">${email.subject}</p>`;
        // when click on the email, go to individual email
        el.addEventListener('click', () => {
          showMailDetails(email.id);
        });
        list.appendChild(el);
      });
    });
}
