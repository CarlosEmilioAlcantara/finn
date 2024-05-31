document.addEventListener("DOMContentLoaded", function() {
    const texts = document.querySelectorAll(".text");

    function hideText() {
        texts.forEach(text => text.classList.remove("active"));
    }

    function showText() {
        texts.forEach(text => text.classList.add("active"));
    }

   
    showText();

    
    setInterval(function() {
        hideText();
        setTimeout(showText, 3000); 
    }, 6000); 
});
