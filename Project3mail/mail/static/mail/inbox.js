// we will check if user and sender is the same persor or not
const userName = document.getElementById('user-name').textContent;
// Use buttons to toggle between views
const inboxButton = document.getElementById('inbox');
const sentButton = document.getElementById('sent');
const archiveButton = document.getElementById('archived');
const composeButton = document.getElementById('compose');
// button event listeners
inboxButton.addEventListener('click', () => load_mailbox('inbox'));
sentButton.addEventListener('click', () => load_mailbox('sent'));
archiveButton.addEventListener('click', () => load_mailbox('archive'));
composeButton.addEventListener('click', compose_email);
// views
const emailsView = document.getElementById('emails-view');
const composeView = document.getElementById('compose-view');
const singleView = document.getElementById('single-view');

// By default, load the inbox
load_mailbox('inbox');

// Input fields
const recipientsField = document.getElementById('compose-recipients');
const subjectField = document.getElementById('compose-subject');
const mailBodyField = document.getElementById('compose-body');

function compose_email() {
  // Show compose view and hide other views
  emailsView.style.display = 'none';
  singleView.style.display = 'none';
  composeView.style.display = 'block';

  // Clear out composition fields
  recipientsField.value = '';
  subjectField.value = '';
  mailBodyField.value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  emailsView.style.display = 'block';
  singleView.style.display = 'none';
  composeView.style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view-heading').textContent = `${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }`;
  // get mails from server
  getMailbox(mailbox);
}

function showMailDetails(id) {
  // Show the single mail and hide other views
  emailsView.style.display = 'none';
  singleView.style.display = 'block';
  composeView.style.display = 'none';
  // handle single view
  handleSingleView(id);
}
