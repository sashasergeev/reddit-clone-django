const searchContainer = document.querySelector("#searchContainer");
const searchInput = document.querySelector("#search");
let style = searchContainer.style;

// SEARCH AND NOTIFICATION DROPDOWNS ONBLUR
// IS LOCATED IN 'base.html'

searchInput.addEventListener("keyup", (e) => {
  const value = e.target.value;
  if (style.display === "none" && value.length !== 0) {
    style.display = "block";
    fetchSearchResults(value);
  } else if (style.display === "block" && value.length !== 0) {
    fetchSearchResults(value);
  } else if (style.display === "block" && value.length === 0) {
    searchContainer.innerHTML = "Find subreddit!";
  }
});

const fetchSearchResults = async (value) => {
  const request = await fetch(`${window.location.origin}/subreddits/search/`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": token,
    },
    body: JSON.stringify({ query: value }),
  });
  const data = await request.json();
  renderResults(data);
};

const renderResults = (res) => {
  searchContainer.innerHTML = "";
  if (res.data === "No subreddits found...") {
    searchContainer.innerHTML = `<div class="search-item">${res.data}</div>`;
    return;
  }
  res.data.forEach(
    (e) =>
      (searchContainer.innerHTML += `
      
      <a class="search-item" href="${window.location.origin}/r/${e.name}/">
        <img class="search-item-logo" src=${e.img} alt="${e.name} logo" />
        <div class="search-item-info">
        <div>${e.name}</div>  
        <div class="search-item-membs">${e.num_members} members</div>  
        </div>  
      </a>
      
      `)
  );
};
