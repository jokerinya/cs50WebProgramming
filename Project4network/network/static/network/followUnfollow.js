/**
 * This js file will be downloaded only when the user is authenticated.
 * This file makes asynchronous request for server.
 * Follow and Unfollow user speciality are made here.
 */

console.log('followUnfollow.js : user is authenticated');

const followerNumEl = document.querySelector('span[followers]');
const followingNumEl = document.querySelector('span[followings]');

// Get all list elements
const btnElementsList = document.querySelectorAll('button[users]');

btnElementsList.forEach((btn) => {
  const userId = btn.getAttribute('uId');
  btn.addEventListener('click', () => followUnfollow(userId, btn), false);
});

function followUnfollow(userId, btn) {
  // getArr ile durmunu getir buna gore islem yapacak fonksiyo
  const isFollowing = btn.getAttribute('isFollowing') === 'true'; // make boolean
  // Make request and according to result change the heart class
  fetch(`/user/${userId}/follow`, {
    method: 'PUT',
    body: JSON.stringify({
      willFollow: !isFollowing,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      // update button classlist and attributes
      console.log(data);
      updateDom(btn, data);
    })
    .catch((err) => console.log(err)); // Do something with the error
}

function updateDom(btn, data) {
  const isFollowingAttr = btn.getAttribute('isFollowing');
  if (isFollowingAttr === 'false') {
    btn.classList.replace('btn-success', 'btn-danger');
    btn.innerHTML = 'Unfollow';
    btn.setAttribute('isFollowing', 'true');
  } else {
    btn.classList.replace('btn-danger', 'btn-success');
    btn.innerHTML = 'Follow';
    btn.setAttribute('isFollowing', 'false');
  }
  followerNumEl.innerHTML = data.followers;
  followingNumEl.innerHTML = data.followings;
}
