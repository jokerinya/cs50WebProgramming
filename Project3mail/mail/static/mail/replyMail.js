function reply(sender, subject, timestamp, body) {
  console.log(sender, subject, timestamp, body);
  //  First clean the input fields
  compose_email();
  // Fill the input fields of inbox.html
  recipientsField.value = sender;
  // Check the status of the subject
  console.log(subject);
  if (!subject.startsWith('Re: ')) {
    subject = 'Re: ' + subject;
  }
  subjectField.value = subject;
  // for body add time
  body = `"On ${timestamp} ${sender} wrote:"\n '${body}'`;
  mailBodyField.value = body;
}
