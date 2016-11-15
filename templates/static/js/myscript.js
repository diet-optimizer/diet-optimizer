console.log('ciao');
function test()
{
    // var element = document.createElement("div");
    // element.appendChild(document.createTextNode('The man who mistook his wife for a hat'));
    // document.getElementbyId('lc').appendChild(element);

    // <div class="panel panel-default" id="panel2" data-toggle="collapse" data-target="#collapse2">
    //   <div class="panel-heading" data-toggle="collapse" data-target="#collapse2">
    //     <h4 class="panel-title">
              // <a data-toggle="collapse" data-target="#collapse2" href="#collapse2" class="collapsed">Links</a></h4>
    //   </div>
    //   <div id="collapse2" class="panel-collapse collapse fade">
    //     <div class="panel-body">
    //       Drumstick beef ribs venison sirloin pork loin salami swine frankfurter cow doner short loin landjaeger shankle pig. Meatloaf swine filet mignon, shankle biltong ground round tongue pancetta jerky picanha tenderloin.
    //     </div>
    //   </div>
    // </div>

    for(var i = 0; i<6; i++){

      var panelI = document.createElement('div');
      panelI.className = "panel panel-defaul";
      panelI.id = "panel" + i;
      document.getElementById('accordion').appendChild(panelI);
      $("#panel" + i).attr("data-toggle", "#collapse");
      $("#panel" + i).attr("data-target", "#collapse" + i);
      console.log(document.getElementById('accordion'));

      var panelHeading = document.createElement('div');
      panelHeading.className = "panel-heading";
      document.getElementById('panel' + i).appendChild(panelHeading);
      $("#panel" + i + " > .panel-heading").attr("data-toggle", "#collapse");
      $("#panel" + i + " > .panel-heading").attr("data-collapse", "#collapse" + i);

      var panelTitle = document.createElement('h4');
      panelTitle.className = "panel-title"
      document.getElementById('panel' + i).getElementsByClassName("panel-heading")[0].appendChild(panelTitle)

      var a = document.createElement('a');
      a.className = "collapsed"
      document.getElementById('panel' + i).getElementsByClassName("panel-heading")[0].getElementsByClassName("panel-title")[0].appendChild(a);
      $("#panel" + i + " > .panel-heading > .panel-title > .collapsed").attr("data-toggle", "collapse");
      $("#panel" + i + " > .panel-heading > .panel-title > .collapsed").attr("data-target", "#collapse" + i);
      $("#panel" + i + " > .panel-heading > .panel-title > .collapsed").attr("href", "#collapse" + i);
      $("#panel" + i + " > .panel-heading > .panel-title > .collapsed").append('Recipe Title ' + i)

      var collapseFade = document.createElement('div');
      collapseFade.className = "panel-collapse collapse fade";
      collapseFade.id = "collapse" + i;
      document.getElementById('panel' + i).appendChild(collapseFade);

      var panelBody = document.createElement('div');
      panelBody.className = "panel-body";
      document.getElementById('panel' + i).getElementsByClassName("panel-collapse collapse fade")[0].appendChild(panelBody);
      $("#collapse" + i + " > .panel-body").append('Recipe Content ' + i);

      var sheet = document.createElement('style')
      sheet.innerHTML = "div {border: 2px solid black;}";
      document.body.appendChild(sheet);
  }
}


(function(window, document, undefined){

window.onload = init;

  function init(){
    test()
  }

})(window, document, undefined);
