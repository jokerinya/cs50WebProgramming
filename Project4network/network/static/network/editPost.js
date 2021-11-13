/**
 * This js file will be downloaded only when the user is authenticated.
 * This file makes asynchronous request for server.
 * Edit post speciality will be held by this file.
 */

console.log('editPost.js: user is authenticated');
// Get all edit buttons on the page
const editBtnList = document.querySelectorAll('a.edit_btn');
// Get all Edit send buttons on the page
const edittedPostSendBtnList = document.querySelectorAll(
  'button.edit_send_btn'
);
// Edit Close button list
const editCloseBtnList = document.querySelectorAll('button.edit_close_btn');

// add event listeners for editBtns
editBtnList.forEach((editBtn) => {
  const postId = editBtn.getAttribute('postId');
  editBtn.addEventListener(
    'click',
    (event) => editPostUI(event, postId),
    false
  );
});
// add event listeners for Post button server request
edittedPostSendBtnList.forEach((edittedPostSendBtn) => {
  const postId = edittedPostSendBtn.getAttribute('postId');
  edittedPostSendBtn.addEventListener('click', (event) =>
    sendPost(event, postId)
  );
});
// add event listener for Close button
editCloseBtnList.forEach((editCloseBtn) => {
  const postId = editCloseBtn.getAttribute('postId');
  editCloseBtn.addEventListener('click', (event) =>
    openCloseTextarea(postId, 'exit')
  );
});

// UI process
function openCloseTextarea(postId, process) {
  const editBtn = document.querySelector(`a.edit_btn[postId='${postId}']`);
  const cardTextEl = document.querySelector(`p.card-text[postId='${postId}']`);
  const formGroupEl = document.querySelector(
    `div.form-group[postId='${postId}']`
  );
  const textarea = document.querySelector(`textarea[postId='${postId}']`);

  if (process === 'open') {
    editBtn.classList.add('disabled');
    cardTextEl.classList.add('hidden');
    formGroupEl.classList.remove('hidden');
    textarea.value = cardTextEl.innerText;
  }
  if (process === 'close' || process === 'exit') {
    editBtn.classList.remove('disabled');
    cardTextEl.classList.remove('hidden');
    formGroupEl.classList.add('hidden');
  }
  if (process === 'close') {
    cardTextEl.innerText = textarea.value;
  }
}

// Edit Button function
function editPostUI(event, postId) {
  openCloseTextarea(postId, (process = 'open'));
}

function sendPost(event, postId) {
  const textarea = document.querySelector(`textarea[postId='${postId}']`);
  const newPost = textarea.value;
  const isValidText = new TextValidation(newPost).isValidText();
  if (isValidText) {
    sendEdittedPostToServer(event, postId, newPost).then((response) => {
      console.log(response);
      if (response.error === undefined) {
        openCloseTextarea(postId, (open = 'close'));
      } else {
        alert(`An error occured, ${response.error}.`);
        openCloseTextarea(postId, (open = 'exit'));
      }
    });
  } else {
    alert('Text is not between 1-280 chars.');
  }
}
// server request
function sendEdittedPostToServer(event, postId, newText) {
  event.preventDefault();
  return fetch(`/post/${postId}/edit`, {
    method: 'PUT',
    body: JSON.stringify({
      postId: postId,
      edittedPost: newText,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((err) => console.log(err)); // Do something with the error
}
