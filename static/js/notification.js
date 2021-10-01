const showNotification = () => {
  const container = document.getElementById("notification_container");

  if (container.style.display === "none") {
    container.style.display = "block";
  } else {
    container.style.display = "none";
  }
};
