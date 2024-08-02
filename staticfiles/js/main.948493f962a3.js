let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");
// console.log(pageLinks);

if (searchForm) {
  for (let i = 0; i < pageLinks.length; i++) {
    pageLinks[i].addEventListener("click", function (e) {
      // preventing the default action of the pagination button on click
      e.preventDefault();

      // getting the value of the pagination button which has been cliked
      let page = this.dataset.page;

      // console.log(page);
      // now making a new tag inside the form which on submit will append the page value to the url
      // searchForm.innerHTML += `<input value=${page} name="page" hidden`;

      let pageInput = document.createElement("input");
      pageInput.type = "hidden";
      pageInput.name = "page";
      pageInput.value = page;
      searchForm.appendChild(pageInput);

      // submit the form using the javascript
      searchForm.submit();
    });
  }
}
