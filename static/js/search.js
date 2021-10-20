const searchContainer = document.querySelector("#searchContainer");
const searchInput = document.querySelector("#search");
let style = searchContainer.style;
const isSubPageRegex = /r\/\w+/;

// SEARCH AND NOTIFICATION DROPDOWNS ONBLUR
// IS LOCATED IN 'base.html'

searchInput.addEventListener("keyup", (e) => {
  const value = e.target.value;
  if (e.key === "Enter") {
    if (isSubPageRegex.test(window.location.href)) {
      window.location.href = `${window.location.origin}/${
        window.location.href.match(isSubPageRegex)[0]
      }/search/?q=${value}`;
    } else {
      window.location.href = `${window.location.origin}/search/?q=${value}`;
    }
  }

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
  const request = await fetch(
    `${window.location.origin}/subreddits/live-search/`,
    {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": token,
      },
      body: JSON.stringify({ query: value }),
    }
  );
  const data = await request.json();
  renderResults(data, value);
};
const searchForBtn = (query) =>
  isSubPageRegex.test(window.location.href)
    ? `
  <a href="${window.location.origin}/${
        window.location.href.match(isSubPageRegex)[0]
      }/search/?q=${query}" class="search-item">
    <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="currentColor" style="height: 21px; width: 21px; margin-right: 10px;"><path d="M15.6 14l2.8 2.6a1.3 1.3 0 11-1.8 1.8l-2.8-2.7a8 8 0 111.8-1.8zm-1-4.8a5.5 5.5 0 10-5.4 5.4 5.5 5.5 0 005.4-5.4z"></path></svg>
    <span>Search for "${query}"</span>
  </a>
  `
    : `
  <a href="${window.location.origin}/search/?q=${query}" class="search-item">
    <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="currentColor" style="height: 21px; width: 21px; margin-right: 10px;"><path d="M15.6 14l2.8 2.6a1.3 1.3 0 11-1.8 1.8l-2.8-2.7a8 8 0 111.8-1.8zm-1-4.8a5.5 5.5 0 10-5.4 5.4 5.5 5.5 0 005.4-5.4z"></path></svg>
    <span>Search for "${query}"</span>
  </a>
  `;
const renderResults = (res, query) => {
  searchContainer.innerHTML = "";
  if (res.data === "No subreddits found...") {
    searchContainer.innerHTML = searchForBtn(query);
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
  searchContainer.innerHTML += searchForBtn(query);
};
