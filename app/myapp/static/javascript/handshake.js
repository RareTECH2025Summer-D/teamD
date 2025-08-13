const tabs = document.querySelectorAll(".handshake-tabs li a");
const tabBorders = document.querySelectorAll(".handshake-tabs hr");
const contents = document.querySelectorAll(".handshake-contents li");



for (let i = 0; i < tabs.length; i++) {
    tabs[i].addEventListener("click", function(e) {
        e.preventDefault();

        for (let j = 0; j < tabs.length; j++) {
            tabs[j].classList.remove("active");
        }
        for (let j = 0; j < tabBorders.length; j++) {
            tabBorders[j].classList.remove("active");
        }
        for (let j = 0; j < contents.length; j++) {
            contents[j].classList.remove("active");
        }

        tabs[i].classList.add("active");
        tabBorders[i].classList.add("active");
        contents[i].classList.add("active");
    });
}
