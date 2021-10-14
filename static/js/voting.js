let token = document.cookie.match(/csrftoken=(\w+)/)[1];

const voteHandle = (voteObj, voteType, objId) => {
  let voteCountEl;
  if (voteObj === "post") {
    voteCountEl = document.querySelector(`#votes-on-${objId}`);
  } else {
    voteCountEl = document.querySelector(`#comment-point-${objId}`);
  }
  fetch(`${window.location.origin}/${voteObj}/vote/${objId}/${voteType}/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": token,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (
        data.action === `${voteObj} upvoted` &&
        data.downvote_existed === false
      ) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}upvote-${objId}`
        ).style.color = "rgb(0, 204, 153)"; // color the upvote button the teal
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) + 1;
      } else if (data.action === `${voteObj} upvote unvoted`) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}upvote-${objId}`
        ).style.color = "rgb(129, 131, 132)"; // color the upvote button the basic
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) - 1;
      } else if (data.downvote_existed === true) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}upvote-${objId}`
        ).style.color = "rgb(0, 204, 153)"; // color the upvote button the teal
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}downvote-${objId}`
        ).style.color = "rgb(129, 131, 132)"; // color the downvote button the basic
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) + 2;
      }
      if (
        data.action === `${voteObj} downvoted` &&
        data.upvote_existed === false
      ) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}downvote-${objId}`
        ).style.color = "rgb(214, 138, 89)"; // color the downvote button the red
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) - 1;
      } else if (data.action === `${voteObj} downvote unvoted`) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}downvote-${objId}`
        ).style.color = "rgb(129, 131, 132)"; // color the downvote button the basic
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) + 1;
      } else if (data.upvote_existed === true) {
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}downvote-${objId}`
        ).style.color = "rgb(214, 138, 89)"; // color the dotnvote button the red
        document.querySelector(
          `#${voteObj === "comment" ? "comment-" : ""}upvote-${objId}`
        ).style.color = "rgb(129, 131, 132)"; // color the upvote button the basic
        voteCountEl.innerHTML = parseInt(voteCountEl.innerHTML) - 2;
      }
    })
    .catch((err) => console.log(err));
};
