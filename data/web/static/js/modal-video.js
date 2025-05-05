// static/js/modal-video.js

document.addEventListener("DOMContentLoaded", () => {
    const triggers = document.querySelectorAll("[data-video]");
    const modal = document.getElementById("videoModal");
    const iframe = document.getElementById("videoFrame");
    const closeBtn = document.getElementById("videoModalClose");
  
    triggers.forEach(trigger => {
      trigger.addEventListener("click", () => {
        const videoUrl = trigger.getAttribute("data-video");
        iframe.src = `${videoUrl}?autoplay=1`;
        modal.classList.remove("hidden");
      });
    });
  
    closeBtn.addEventListener("click", () => {
      iframe.src = "";
      modal.classList.add("hidden");
    });
});