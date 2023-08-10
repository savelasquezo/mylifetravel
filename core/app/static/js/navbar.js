window.addEventListener('scroll', function() {
  var myDiv = document.getElementById('myDiv');
  if (window.pageYOffset > 0) {
    myDiv.classList.add('visible');
  } else {
    myDiv.classList.remove('visible');
  }
});