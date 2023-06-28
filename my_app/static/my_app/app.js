document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", (e) => {
    const isDropDownButton = e.target.matches(".link");
    if (!isDropDownButton && e.target.closest(".dropdown") != null) return;

    let currentDropdown;
    if (isDropDownButton) {
      currentDropdown = e.target.closest(".dropdown");
      currentDropdown.classList.toggle("active");
    }
    document.querySelectorAll(".dropdown.active").forEach((dropdown) => {
      if (dropdown === currentDropdown) return;
      dropdown.classList.remove("active");
    });
  });

  document.addEventListener("click", (e) => {
    const isDropDownButton = e.target.matches(".link-mobile");
    if (!isDropDownButton && e.target.closest(".dropdown-mobile") != null)
      return;

    let currentDropdown;
    if (isDropDownButton) {
      currentDropdown = e.target.closest(".dropdown-mobile");
      currentDropdown.classList.toggle("active");
    }
    document.querySelectorAll(".dropdown-mobile.active").forEach((dropdown) => {
      if (dropdown === currentDropdown) return;
      dropdown.classList.remove("active");
    });
  });

  document.querySelectorAll(".save").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (el.src == "https://cdn-icons-png.flaticon.com/512/1077/1077035.png") {
        el.setAttribute(
          "src",
          "https://cdn-icons-png.flaticon.com/512/1076/1076984.png"
        );
      } else {
        el.setAttribute(
          "src",
          "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"
        );
      }

      fetch(`/save/${el.dataset.listid}`)
        .then((res) => res.json())
        .then((result) => {
          if (el.classList.contains("heart")) {
            console.log("heart");
            if (document.querySelector(".title").textContent == "Saved") {
              console.log("removed");
              el.parentElement.parentElement.remove();
            }
          }
        });
    });
  });
});
