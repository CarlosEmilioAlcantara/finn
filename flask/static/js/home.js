document.addEventListener("DOMContentLoaded", function() {
    const texts = document.querySelectorAll(".text");
    let index = 0;

    function showText() {
        texts[index].classList.remove("active");
        index = (index + 1) % texts.length;
        texts[index].classList.add("active");
    }

    showText();

    setInterval(showText, 3000);
});
