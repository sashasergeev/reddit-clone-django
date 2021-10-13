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

// SEARCH AND NOTIFICATION DROPDOWNS ONBLUR
// IS LOCATED IN 'base.html'

const clearNotifications = () => {
  let items = document.querySelectorAll(".notification-item");
  fetch(`${window.location.origin}/notifications/clear/`, {
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

const readNotifications = () => {
  let items = document.querySelectorAll(".notification-item"); // items in navbar
  let itemsOnPage = document.querySelectorAll(".not-item"); // items on the notification page

  fetch(`${window.location.origin}/notifications/clear/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": token,
    },
  })
    .then((res) => res.json())
    .then(() => {
      items.forEach((e) => e.remove()); // removes notifications in navbars nots
      itemsOnPage.forEach(
        (e) =>
          e.classList.contains("notif-hasnt-seen") &&
          e.classList.remove("notif-hasnt-seen")
      );

      document.querySelector(".notification-badge").remove();
    })
    .catch((err) => console.log(err));
};
