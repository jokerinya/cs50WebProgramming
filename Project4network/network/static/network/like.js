/**
 * This js file will be downloaded only when the user is authenticated.
 * This file makes asynchronous request for server. Like and Unlike speciality.
 */

console.log('like.js: user is authenticated.');
const likeHeartsList = document.querySelectorAll('.like_heart .fa'); // node list

const likeOrUnlike = (postId, el) => {
  // fa-heart-o = empty heart, fa-heart = full heart
  const isLiked = el.classList.contains('fa-heart') ? true : false;
  // Make request and according to result change the heart class
  fetch(`/post/${postId}/edit`, {
    method: 'PUT',
    body: JSON.stringify({
      isLiked: !isLiked,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (isLiked === true) {
        el.classList.replace('fa-heart', 'fa-heart-o');
      } else {
        el.classList.replace('fa-heart-o', 'fa-heart');
      }
      // update like numbers
      document.querySelector(`span[postId='${postId}']`).innerText =
        data.likeNum;
    })
    .catch((err) => console.log(err)); // Do something with the error
};

likeHeartsList.forEach((el) => {
  el.classList.add('authenticated_heart'); // cursor pointer
  const postId = el.getAttribute('postId');
  el.addEventListener('click', likeOrUnlike.bind(null, postId, el), false);
});
