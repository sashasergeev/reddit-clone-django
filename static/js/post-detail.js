token = document.cookie.match(/csrftoken=(\w+)/)[1];

// deleting comments
const commentDeleteButtons = document.querySelectorAll('.btn-delete');
commentDeleteButtons.forEach(e => {
    e.addEventListener('click', b => {
        let commentId = b.target.dataset.commentId;
        fetch(`http://${window.location.host}/comment/${commentId}/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": token
            }
        }).then(res => res.json()).then(data => {
            document.querySelector(`#comment-${commentId}`).remove();
        });
    });
});

// UPVOTE DOWNVOTE COMMENTS
// upvote comments
const commentUpvoteButtons = document.querySelectorAll('.comment-upvote');
commentUpvoteButtons.forEach(e => {
    e.addEventListener('click', b => {
        let commentId = e.dataset.commentId;

        fetch(`http://${window.location.host}/comment-vote/${commentId}/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": token
            }
        }).then(res => res.json()).then(data => {
            const points = document.querySelector(`#comment-point-${commentId}`);
            if (data.action === "comment upvoted" && data.downvote_existed === false) {
                document.querySelector(`#comment-upvote-${commentId}`).style.color = 'rgb(0, 204, 153)'; // color the upvote button the teal
                points.innerHTML = parseInt(points.innerHTML) + 1;
            } else if (data.action ==="comment upvote unvoted") {
                document.querySelector(`#comment-upvote-${commentId}`).style.color = 'rgb(129, 131, 132)'; // color the upvote button the basic
                points.innerHTML = parseInt(points.innerHTML) - 1;
            } else if (data.downvote_existed === true) {
                document.querySelector(`#comment-upvote-${commentId}`).style.color = 'rgb(0, 204, 153)'; // color the upvote button the teal
                document.querySelector(`#comment-downvote-${commentId}`).style.color = 'rgb(129, 131, 132)'; // color the downvote button the basic
                points.innerHTML = parseInt(points.innerHTML) + 2;
            };
        });
    });
});

// downvote comments
const commentDownvoteButtons = document.querySelectorAll('.comment-downvote');
commentDownvoteButtons.forEach(e => {
    e.addEventListener('click', b => {
        let commentId = e.dataset.commentId;

        fetch(`http://${window.location.host}/comment-downvote/${commentId}/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": token
            }
        }).then(res => res.json()).then(data => {
            const points = document.querySelector(`#comment-point-${commentId}`);
            if (data.action === "comment downvoted" && data.upvote_existed === false) {
                document.querySelector(`#comment-downvote-${commentId}`).style.color = 'rgb(214, 138, 89)'; // color the downvote button the red
                points.innerHTML = parseInt(points.innerHTML) - 1;
            } else if (data.action ==="comment downvote unvoted") {
                document.querySelector(`#comment-downvote-${commentId}`).style.color = 'rgb(129, 131, 132)'; // color the downvote button the basic
                points.innerHTML = parseInt(points.innerHTML) + 1;
            } else if (data.upvote_existed === true) {
                document.querySelector(`#comment-downvote-${commentId}`).style.color = 'rgb(214, 138, 89)'; // color the dotnvote button the red
                document.querySelector(`#comment-upvote-${commentId}`).style.color = 'rgb(129, 131, 132)'; // color the upvote button the basic
                points.innerHTML = parseInt(points.innerHTML) - 2;
            };
        }).catch(err => console.log(err));
    });
});

// reply form for the parent comments
const commentReply = (id) => {


    let comment = document.querySelector(`#comment-${id}`);
    if (document.contains(document.querySelector("#childForm"))) {
        document.querySelector("#childForm").remove();
    }
    
    comment.insertAdjacentHTML('afterend', 
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
}

const hideForm = () => {
    document.querySelector("#childForm").remove();
}