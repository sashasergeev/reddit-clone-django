const btn = document.getElementById("notifications");
const container = document.getElementById("notification_container");

const showNotification = () => {
  if (container.style.display === "none") {
    container.style.display = "block";
    btn.style.background = "#d7dadc1a";
  } else {
    container.style.display = "none";
    btn.style.background = "none";
  }
};

window.onclick = function (e) {
  if (!e.target.matches("#notifications")) {
    if (container.style.display === "block") {
      container.style.display = "none";
      btn.style.background = "none";
    }
  }
};

const clearNotifications = () => {
  let items = document.querySelectorAll(".notification-item");
  fetch(`https://${window.location.host}/notifications/clear/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": token,
    },
  })
    .then((res) => res.json())
    .then(() => {
      items.forEach((e) => e.remove());
      document.querySelector(".notification-badge").remove();
    })
    .catch((err) => console.log(err));
};
