const button = document.querySelectorAll(".notes");
const popup = document.querySelector(".notes-overlay");
const close = document.querySelector(".close-notes");
const notesThemself = document.querySelector(".notes-themself");

button.forEach((row) => {
  row.addEventListener("click", (e) => {
    notesThemself.innerText = e.target.nextElementSibling.querySelector(
      ".notes-themself"
    ).innerText;
    popup.style.display = "block";
  });
});

close.addEventListener("click", () => {
  popup.style.display = "none";
});

popup.addEventListener("click", () => {
  popup.style.display = "none";
});
