
function showPreview(event){
	debugger;
  if(event.target.files.length > 0){
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
    showDiv();
  
  } 
}


function showDiv() {
   document.getElementById('thebutton').style.display = "block"; 

}



