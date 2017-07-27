
// this func is to enable/disable cuisines 
$(document).ready(function(){
disableCuisines();
});
function disableCuisines() {
  // console.log("running");
if ( document.getElementById('checkAll').checked ) 
  { 
    console.log("checked");
    $('.groupCuisine').each(function(){
      // console.log("adding");
      $(this).attr("disabled",true);
    }); 
  } 
else 
  {
    console.log("unchecked");
    $('.groupCuisine').each(function(){
      // console.log("deleting");
      $(this).attr("disabled",false);
    }); 
  }
};

// this func is to enable/disable intolerances 
$(document).ready(function(){
disableIntolerances();
});
function disableIntolerances() {
if ( document.getElementById('noIntol').checked ) 
  { 
    $('.groupIntol').each(function(){
      $(this).attr("disabled",true);
    }); 
  } 
else 
  {
    $('.groupIntol').each(function(){
      $(this).attr("disabled",false);
    }); 
  }
};







