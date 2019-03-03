// function toggleFunc() {
//   var x = $("#mainTopnav");
//
//   if (x.classname === "topnav") {
//     x.classname += " responsive";
//   } else {
//     x.className = "topnav";
//   }
// }
//
function activePageFunc() {
  var pageContainer = $(document).getElementById("navbarSupportedContent");
  var pages = pageContainer.getElementByClassName("nav-item");
  for (var i=0; i<pages.length; i++) {
    pages[i].addEventListener("click", function() {
      var current = document.getElementByClassName("active");
      current[0].classname = current[0].classname.replace(" active","");
      this.className += " active";
    });
  }
}
