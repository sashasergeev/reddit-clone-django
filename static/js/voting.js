const postUpvoteButtons = document.querySelectorAll(".post-upvote");
let token = document.cookie.match(/csrftoken=(\w+)/)[1];

postUpvoteButtons.forEach((e) => {
  e.addEventListener("click", (b) => {
    let button = e;
    let post_id = e.dataset.postId;
    let votes_element = document.querySelector(`#votes-on-${post_id}`);
    fetch(`${window.location.origin}/vote/${post_id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.action === "post upvote unvoted") {
          button.style.color = "rgb(129, 131, 132)";
          votes_element.innerHTML = parseInt(votes_element.innerHTML) - 1;
        } else {
          button.style.color = "rgb(0, 204, 153)";
        }
        if (data.action === "post upvoted") {
          if (data.downvote_existed === false) {
            votes_element.innerHTML = parseInt(votes_element.innerHTML) + 1;
          } else {
            document.querySelector(`#downvote-${post_id}`).style.color =
              "rgb(129, 131, 132)";
            votes_element.innerHTML = parseInt(votes_element.innerHTML) + 2;
          }
        }
      })
      .catch((err) => console.log(err));
  });
});

const postDownvoteButtons = document.querySelectorAll(".post-downvote");

postDownvoteButtons.forEach((e) => {
  e.addEventListener("click", (b) => {
    let button = e;
    let post_id = e.dataset.postId;
    let votes_element = document.querySelector(`#votes-on-${post_id}`);

    fetch(`${window.location.origin}/downvote/${post_id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.action === "post downvote unvoted") {
          button.style.color = "rgb(129, 131, 132)";
          votes_element.innerHTML = parseInt(votes_element.innerHTML) + 1;
        } else {
          button.style.color = "rgb(214, 138, 89)";
        }
        if (data.action === "post downvoted") {
          if (data.upvote_existed === false) {
            votes_element.innerHTML = parseInt(votes_element.innerHTML) - 1;
          } else {
            document.querySelector(`#upvote-${post_id}`).style.color =
              "rgb(129, 131, 132)";
            votes_element.innerHTML = parseInt(votes_element.innerHTML) - 2;
          }
        }
      })
      .catch((err) => console.log(err));
  });
});
