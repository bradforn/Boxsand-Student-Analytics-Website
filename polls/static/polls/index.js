
var twitary = document.getElementsByClassName("twit")
 var searchbutton = document.getElementById("navbar-search-button")
 var searchbar = document.getElementById("navbar-search-input")
 var hidden = document.getElementsByClassName('hidden')
 var twitbutton = document.getElementById('create-twit-button')
 var createmodal = document.getElementById('create-twit-modal')
 var twittext = document.getElementById("twit-text-input")
 var author = document.getElementById("twit-attribution-input")

// unhides twit modal
 function modal (event) {
     hidden[0].style.display = "initial";
     hidden[1].style.display = "initial";
 }

 function canceltwit (event){
   var currElem = event.target;
   if(currElem.getAttribute('class') === 'modal-cancel-button' || currElem.getAttribute('class') === "modal-close-button"){
     hidden[0].style.display = "none";
     hidden[1].style.display = "none";
     twittext.value = '';
     author.value = '';
   }
   if (currElem.getAttribute('class') === 'modal-accept-button'){
     if (twittext.value === '' || author.value === '') {
       alert("Please make sure the author and message has been entered");
       }
     createtwit(twittext.value, author.value);
   }
 }

twitbutton.addEventListener('click', modal);
createmodal.addEventListener('click',canceltwit);
searchbutton.addEventListener('click', searchs);
