const saveHandle = (objType, objPk) => {
  fetch(`${window.location.origin}/save/${objType}/${objPk}/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": token,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.action === "saved") {
        document.querySelector(`#${objType}-save-${objPk}`).innerHTML =
          "Unsave";
      } else {
        document.querySelector(`#${objType}-save-${objPk}`).innerHTML = "Save";
      }
    });
};
