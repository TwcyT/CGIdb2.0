


  function overShow_10() {
  var showDiv_10 = document.getElementById('download_click');
  showDiv_10.style.display = 'block';
  showDiv_10.innerHTML = 'Download this file';
 }

 function outHide_10() {
  var showDiv_10 = document.getElementById('download_click');
  showDiv_10.style.display = 'none';
  showDiv_10.innerHTML = '';
 }

  function overShow_11() {
  var showDiv_11 = document.getElementById('download_click_2');
  showDiv_11.style.display = 'block';
  showDiv_11.innerHTML = 'Download this file';
 }

 function outHide_11() {
  var showDiv_11 = document.getElementById('download_click_2');
  showDiv_11.style.display = 'none';
  showDiv_11.innerHTML = '';
 }

  function overShow_12() {
  var showDiv_12 = document.getElementById('download_click_3');
  showDiv_12.style.display = 'block';
  showDiv_12.innerHTML = 'Download this file';
 }

 function outHide_12() {
  var showDiv_12 = document.getElementById('download_click_3');
  showDiv_12.style.display = 'none';
  showDiv_12.innerHTML = '';
 }



    function getPos(ev){
        var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
        var scrollLeft=document.documentElement.scrollLeft||document.body.scrollLeft;

        return{x:ev.clientX+scrollLeft,y:ev.clientY+scrollTop};
    }

document.onmousemove=function(ev)
{
var oEvent=ev||Event;
var oDiv_10=document.getElementById('download_click');
      var pos_10=getPos(oEvent);
      oDiv_10.style.left=(pos_10.x-65)+'px';
      oDiv_10.style.top=(pos_10.y-52)+'px';
var oDiv_11=document.getElementById('download_click_2');
      var pos_11=getPos(oEvent);
      oDiv_11.style.left=(pos_11.x-65)+'px';
      oDiv_11.style.top=(pos_11.y-52)+'px';
var oDiv_12=document.getElementById('download_click_3');
      var pos_12=getPos(oEvent);
      oDiv_12.style.left=(pos_12.x-65)+'px';
      oDiv_12.style.top=(pos_12.y-52)+'px';

};





