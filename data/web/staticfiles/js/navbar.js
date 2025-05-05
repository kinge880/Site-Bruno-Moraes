// static/js/navbar.js

document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.getElementById("navbar");
    window.addEventListener("scroll", () => {
    if (window.scrollY > 10) {
    navbar.classList.add("shadow-md", "bg-white");
    } else {
    navbar.classList.remove("shadow-md");
    }
});
});