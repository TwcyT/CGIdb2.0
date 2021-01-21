



 function annoShow_1() {
  var showDiv_1 = document.getElementById('search_anno');
  showDiv_1.style.display = 'block';
  showDiv_1.innerHTML = 'Search your interesting gene<br>for genetic interactions information.';
 }

 function annoHide_1() {
  var showDiv_1 = document.getElementById('search_anno');
  showDiv_1.style.display = 'none';
  showDiv_1.innerHTML = '';
 }
 function annoShow_2() {
  var showDiv_2 = document.getElementById('browse_anno');
  showDiv_2.style.display = 'block';
  showDiv_2.innerHTML = 'Browse the genetic interactions quickly.';
 }

 function annoHide_2() {
  var showDiv_2 = document.getElementById('browse_anno');
  showDiv_2.style.display = 'none';
  showDiv_2.innerHTML = '';
 }
 function annoShow_3() {
  var showDiv_3 = document.getElementById('type_anno_1');
  showDiv_3.style.display = 'block';
  showDiv_3.innerHTML = 'SL: Synthetic Lethality<br>SV: Synthetic Viability';
 }

 function annoHide_3() {
  var showDiv_3 = document.getElementById('type_anno_1');
  showDiv_3.style.display = 'none';
  showDiv_3.innerHTML = '';
 }
 function annoShow_4() {
  var showDiv_4 = document.getElementById('source_anno');
  showDiv_4.style.display = 'block';
  showDiv_4.innerHTML = 'Click to open the data source';
 }

 function annoHide_4() {
  var showDiv_4 = document.getElementById('source_anno');
  showDiv_4.style.display = 'none';
  showDiv_4.innerHTML = '';
 }


document.onmousemove=function(ev)
{
var oEvent=ev||Event;
var oDiv_1=document.getElementById('search_anno');
oDiv_1.style.left=(oEvent.pageX-99)+'px';
oDiv_1.style.top=(oEvent.pageY-72)+'px';
var oDiv_2=document.getElementById('browse_anno');
oDiv_2.style.left=(oEvent.pageX-75)+'px';
oDiv_2.style.top=(oEvent.pageY-52)+'px';
var oDiv_3=document.getElementById('type_anno_1');
oDiv_3.style.left=(oEvent.pageX-75)+'px';
oDiv_3.style.top=(oEvent.pageY-75)+'px';
var oDiv_4=document.getElementById('source_anno');
oDiv_4.style.left=(oEvent.pageX-110)+'px';
oDiv_4.style.top=(oEvent.pageY-52)+'px';
};




