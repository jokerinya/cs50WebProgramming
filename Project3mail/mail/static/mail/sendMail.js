// sending an email
const sendButton = document.getElementById('send-email-btn');
sendButton.addEventListener('click', (event) => {
  // prevent form submission
  event.preventDefault();
  // get values
  const recipients = document.getElementById('compose-recipients').value;
  const subject = document.getElementById('compose-subject').value;
  const body = document.getElementById('compose-body').value;
  // Check if any area is empty
  if (!recipients || !subject || !body) {
    // alert('Please fill out the empty areas.');
    openModal('Please fill out the empty areas!', 'btn-danger');
  } else {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.error) {
          openModal(result.error, 'btn-danger');
        } else {
          openModal(result.message, 'btn-success');
          load_mailbox('sent');
        }
      });
  }
});
