// POPUPS
const overlay = document.querySelector(".overlay");

overlay.addEventListener("click", () => {
    if (aboutPopup.classList.contains("open")) {
        overlay.classList.toggle("open");
        aboutPopup.classList.toggle("open")
    } else if (instructionsPopup.classList.contains("open")) {
        overlay.classList.toggle("open");
        instructionsPopup.classList.toggle("open");
    }
})

const aboutButton = document.querySelector(".about-button");
const aboutReadButton = document.querySelector(".about-read")
const aboutPopup = document.querySelector(".about");

aboutButton.addEventListener("click", () => {
    overlay.classList.toggle("open");
    aboutPopup.classList.toggle("open");
})

aboutReadButton.addEventListener("click", () => {
    overlay.classList.toggle("open");
    aboutPopup.classList.toggle("open");
})

const instructionsButton = document.querySelector(".instructions-button");
const instructionsReadButton = document.querySelector(".instructions-read")
const instructionsPopup = document.querySelector(".instructions");

instructionsButton.addEventListener("click", () => {
    overlay.classList.toggle("open");
    instructionsPopup.classList.toggle("open");
})

instructionsReadButton.addEventListener("click", () => {
    overlay.classList.toggle("open");
    instructionsPopup.classList.toggle("open");
})

// DROPDOWNS
const navHeader = document.querySelector(".nav-header");
const navContent = document.querySelector(".nav-content");

navHeader.addEventListener("click", () => {
    navContent.classList.toggle("pulldown");
})

const popupHeader = document.querySelector(".popup-header");
const popupContent = document.querySelector(".popup-content");

popupHeader.addEventListener("click", () => {
    popupContent.classList.toggle("pulldown");
})

const convHeader = document.querySelector(".conv-header");
const convContent = document.querySelector(".conv-content");

convHeader.addEventListener("click", () => {
    convContent.classList.toggle("pulldown");
})

const funcHeader = document.querySelector(".func-header");
const funcContent = document.querySelector(".func-content");

funcHeader.addEventListener("click", () => {
    funcContent.classList.toggle("pulldown");
})