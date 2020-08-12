const button = document.querySelectorAll(".notes");
const popup = document.querySelector(".notes-overlay");
const close = document.querySelector(".close-notes");
const notesThemself = document.querySelector(".notes-themself");
const firstNote = document.querySelector(".notes-themself").innerText;

button.forEach((row, index) => {
  row.addEventListener("click", (e) => {
    if (index === 0) {
      notesThemself.innerText = firstNote;
      popup.style.display = "block";
      // console.log("first element", notesThemself.innerText);
    } else {
      notesThemself.innerText = e.target.nextElementSibling.querySelector(
        ".notes-themself"
      ).innerText;
      popup.style.display = "block";
    }
  });
  // console.log(row[0], button, firstNote);
});

close.addEventListener("click", () => {
  popup.style.display = "none";
});

popup.addEventListener("click", () => {
  popup.style.display = "none";
});
