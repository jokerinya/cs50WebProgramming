const details = document.getElementById('details');

function handleSingleView(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      const el = document.createElement('table');
      el.classList.add('table', 'table-borderless', 'col-6');
      el.innerHTML = `
        <tbody>
            <tr>
                <th scope='row'>From:</th>
                <td>${email.sender}</td>
            </tr>
            <tr>
                <th scope='row'>To:</th>
                <td>${email.recipients}</td>
            </tr>
            <tr>
                <th scope='row'>Subject:</th>
                <td>${email.subject}</td>
            </tr>
            <tr>
                <th scope='row'>Time:</th>
                <td>${email.timestamp}</td>
            </tr>
        </tbody>`;
      const hr = document.createElement('hr');
      const bodyPart = document.createElement('p');
      bodyPart.innerHTML = email.body;
      bodyPart.style.whiteSpace = 'pre';

      details.innerHTML = '';
      details.appendChild(el);
      details.appendChild(hr);
      details.appendChild(bodyPart);
      details.appendChild(hr);

      // Buttons for archive and reply, check user and sender is same or not
      if (userName !== email.sender) {
        // Reply button
        const replyButton = document.createElement('button');
        replyButton.classList.add('btn', 'btn-primary', 'mr-3');
        replyButton.textContent = 'Reply';
        details.appendChild(replyButton);
        replyButton.addEventListener('click', () => {
          reply(email.sender, email.subject, email.timestamp, email.body);
        });
        // Archive button
        const archiveButton = document.createElement('button');
        archiveButton.classList.add('btn');
        if (email.archived) {
          archiveButton.classList.add('btn-warning');
          archiveButton.textContent = 'Unarchive';
        } else {
          archiveButton.classList.add('btn-success');
          archiveButton.textContent = 'Archive';
        }
        archiveButton.addEventListener(
          'click',
          archive.bind(null, email.id, email.archived),
          false
        );
        details.appendChild(archiveButton);
      }
    });

  // make email readed
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    }),
  });
}

// Archive or unarchive the email and go to the inbox page
function archive(id, archive) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archive,
    }),
  }).then((response) => {
    if (archive === true) {
      openModal('Mail is unarchived.', 'btn-warning');
    } else {
      openModal('Mail is archived.', 'btn-success');
    }
    load_mailbox('inbox');
  });
}
