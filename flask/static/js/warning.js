// WARNING OVERLAY
const overlayWarning = document.querySelector(".overlay-warning");

overlayWarning.addEventListener("click", () => {
    if (!tooMuchWarning.classList.contains("close")) {
        overlayWarning.classList.toggle("close");
        tooMuchWarning.classList.toggle("close");
    } else if (!doNotOwnWarning.classList.contains("close")) {
        overlayWarning.classList.toggle("close");
        doNotOwnWarning.classList.toggle("close");
    }
})

// TOO MUCH TO REMOVE
const tooMuchWarning = document.querySelector(".too-much");
const tooMuchButton = document.querySelector(".too-much-button");

tooMuchButton.addEventListener("click", () => {
    overlayWarning.classList.toggle("close");
    tooMuchWarning.classList.toggle("close");
})

const doNotOwnWarning = document.querySelector(".do-not-own");
const doNotOwnButton = document.querySelector(".do-not-own-button");

doNotOwnButton.addEventListener("click", () => {
    overlayWarning.classList.toggle("close");
    doNotOwnWarning.classList.toggle("close");
})