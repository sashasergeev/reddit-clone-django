token = document.cookie.match(/csrftoken=(\w+)/)[1];

// deleting comments
const commentDeleteButtons = document.querySelectorAll(".btn-delete");
commentDeleteButtons.forEach((e) => {
  e.addEventListener("click", (b) => {
    let commentId = b.target.dataset.commentId;
    fetch(`${window.location.origin}/comment/${commentId}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        document.querySelector(`#comment-${commentId}`).remove();
      });
  });
});

// reply form for the parent comments
const commentReply = (id) => {
  let comment = document.querySelector(`#comment-${id}`);
  if (document.contains(document.querySelector("#childForm"))) {
    document.querySelector("#childForm").remove();
  }

  comment.insertAdjacentHTML(
    "afterend",
    `
            <form id="childForm" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="${token}">
                <p> <textarea name="text" cols="80" rows="10" class="post-comment-textarea" placeholder="What are you want to reply?" required="" id="id_text"></textarea></p>
                <p> 
                    <select name="parent" class="d-none" id="id_parent">
                        <option value="${id}" selected="${id}">---------</option>
                    </select>
                </p>
                <div class="post-comment-lowerline">
                    <button class="post-comment-btn">COMMENT</button>
                    <button class="post-comment-btn" onclick="hideForm()">Hide</button>
                </div>

            </form>
        `
  );
};

const hideForm = () => {
  document.querySelector("#childForm").remove();
};
