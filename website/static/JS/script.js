const sideMenu = document.querySelector("aside ");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const darkMode = document.getElementById("dark");
const lightMode = document.getElementById("light");
let actualDate = document.getElementById("date");
var theme;
menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});
closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});
darkMode.addEventListener("click", function () {
  document.body.classList.add("dark-theme-variables");
  theme = "dark";
  localStorage.setItem("pageTheme", JSON.stringify(theme));
  console.log(theme);
});
lightMode.addEventListener("click", function () {
  document.body.classList.remove("dark-theme-variables");
  theme = "light";
  localStorage.setItem("pageTheme", JSON.stringify(theme));
});
let getTheme = JSON.parse(localStorage.getItem("pageTheme"));

if (getTheme === "dark") {
  document.body.classList = "dark-theme-variables";
} else if (getTheme === "light") {
  document.body.classList.remove("dark-theme-variables");
}
let year = new Date().getFullYear();
let month = new Date().getMonth();
let day = new Date().getDate();
actualDate.textContent = `${day}/${month}/${year}`;
