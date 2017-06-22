$(document).ready(function() {
  $.get("http://127.0.0.1:5000/stories").done(function(data) {
       alert("YO");
  });
});
