let joinBtns = document.querySelectorAll(".sjoin");

joinBtns.forEach((e) => {
  e.addEventListener("click", (b) => {
    let sub_id = b.target.dataset.subId;

    fetch(`https://${window.location.host}/join/${sub_id}/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.action === "left") {
          b.target.style.background = "rgb(215, 218, 220)";
          b.target.style.color = "rgb(26, 26, 27)";
          b.target.innerHTML = "JOIN";
        } else {
          b.target.style.background = "transparent";
          b.target.style.color = "rgb(215, 218, 220)";
          b.target.innerHTML = "JOINED";
        }
      });
  });
});
