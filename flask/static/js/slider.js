var myIndex = 0;
carouselOne();
carouselTwo();

function carouselOne() {
  var i;
  var x = document.getElementsByClassName("slider__img-1");

  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }

  myIndex++;
  if (myIndex > x.length) {myIndex = 1}    
  x[myIndex-1].style.display = "block";  

  setTimeout(carouselOne, 2000); // Change image every 2 seconds
}

function carouselTwo() {
  var i;
  var y = document.getElementsByClassName("slider__img-2");

  for (i = 0; i < y.length; i++) {
    y[i].style.display = "none";  
  }

  myIndex++;
  if (myIndex > y.length) {myIndex = 1}    
  y[myIndex-1].style.display = "block";  

  setTimeout(carouselTwo, 4000); // Change image every 5 seconds
}