/* Taken from https://stackoverflow.com/questions/16200409/ajax-form-upload-progress-bar*/

var form = document.getElementById("uploadForm");
form.onsubmit = function() { 
  console.log("The form has been submitted, start progress!"); 
}
form.target = "file-upload"; 