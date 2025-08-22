const open = document.getElementById("modalOpen");
const mask = document.getElementById("mask");
const modal = document.getElementById("modal");
const close = document.getElementById("modalClose");


open.addEventListener("click", (e) => {
    e.preventDefault();
    modal.classList.add("active");
    mask.classList.add("active");
});

close.addEventListener("click", () => {
    modal.classList.remove("active");
    mask.classList.remove("active");
});

mask.addEventListener("click", () => {
    modal.classList.remove("active");
    mask.classList.remove("active");
});
