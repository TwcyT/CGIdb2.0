



 function overShow_1() {
  var showDiv_1 = document.getElementById('pair_table_detail_click');
  showDiv_1.style.display = 'block';
  showDiv_1.innerHTML = 'Network Nodes List';
 }

 function outHide_1() {
  var showDiv_1 = document.getElementById('pair_table_detail_click');
  showDiv_1.style.display = 'none';
  showDiv_1.innerHTML = '';
 }

 function overShow_2() {
  var showDiv_2 = document.getElementById('table_detail_click');
  showDiv_2.style.display = 'block';
  showDiv_2.innerHTML = 'Show Details';
 }

 function outHide_2() {
  var showDiv_2 = document.getElementById('table_detail_click');
  showDiv_2.style.display = 'none';
  showDiv_2.innerHTML = '';
 }
 function overShow_3() {
  var showDiv_3 = document.getElementById('node_add');
  showDiv_3.style.display = 'block';
  showDiv_3.innerHTML = 'Add Nodes';
 }

 function outHide_3() {
  var showDiv_3 = document.getElementById('node_add');
  showDiv_3.style.display = 'none';
  showDiv_3.innerHTML = '';
 }
 function overShow_4() {
  var showDiv_4 = document.getElementById('edge_add');
  showDiv_4.style.display = 'block';
  showDiv_4.innerHTML = 'Add Edges';
 }

 function outHide_4() {
  var showDiv_4 = document.getElementById('edge_add');
  showDiv_4.style.display = 'none';
  showDiv_4.innerHTML = '';
 }
 function overShow_5() {
  var showDiv_5 = document.getElementById('savenetwork_1');
  showDiv_5.style.display = 'block';
  showDiv_5.innerHTML = 'Save Network';
 }

 function outHide_5() {
  var showDiv_5 = document.getElementById('savenetwork_1');
  showDiv_5.style.display = 'none';
  showDiv_5.innerHTML = '';
 }
 function overShow_6() {
  var showDiv_6 = document.getElementById('hot_gene_1');
  showDiv_6.style.display = 'block';
  showDiv_6.innerHTML = 'Show Hot Genes';
 }

 function outHide_6() {
  var showDiv_6 = document.getElementById('hot_gene_1');
  showDiv_6.style.display = 'none';
  showDiv_6.innerHTML = '';
 }

  function overShow_7() {
  var showDiv_7 = document.getElementById('gene_info_detail');
  showDiv_7.style.display = 'block';
  showDiv_7.innerHTML = 'Gene Information';
 }

 function outHide_7() {
  var showDiv_7 = document.getElementById('gene_info_detail');
  showDiv_7.style.display = 'none';
  showDiv_7.innerHTML = '';
 }

 function overShow_8() {
  var showDiv_8 = document.getElementById('table_detail_complex_click');
  showDiv_8.style.display = 'block';
  showDiv_8.innerHTML = 'Show Complex Details';
 }

 function outHide_8() {
  var showDiv_8 = document.getElementById('table_detail_complex_click');
  showDiv_8.style.display = 'none';
  showDiv_8.innerHTML = '';
 }

  function overShow_9() {
  var showDiv_9 = document.getElementById('table_detail_pathway_click');
  showDiv_9.style.display = 'block';
  showDiv_9.innerHTML = 'Show Pathway Details';
 }

 function outHide_9() {
  var showDiv_9 = document.getElementById('table_detail_pathway_click');
  showDiv_9.style.display = 'none';
  showDiv_9.innerHTML = '';
 }

  function overShow_10() {
  var showDiv_10 = document.getElementById('table_detail_chemical_click');
  showDiv_10.style.display = 'block';
  showDiv_10.innerHTML = 'Show Chemical Details';
 }

 function outHide_10() {
  var showDiv_10 = document.getElementById('table_detail_chemical_click');
  showDiv_10.style.display = 'none';
  showDiv_10.innerHTML = '';
 }
 function overShow_11() {
  var showDiv_11 = document.getElementById('type_anno_2');
  showDiv_11.style.display = 'block';
  showDiv_11.innerHTML = 'SL: Synthetic Lethal<br>SV: Synthetic Viability';
 }

 function outHide_11() {
  var showDiv_11 = document.getElementById('type_anno_2');
  showDiv_11.style.display = 'none';
  showDiv_11.innerHTML = '';
 }
 function overShow_12() {
  var showDiv_12 = document.getElementById('type_anno_3');
  showDiv_12.style.display = 'block';
  showDiv_12.innerHTML = 'SL: Synthetic Lethal<br>SV: Synthetic Viability';
 }

 function outHide_12() {
  var showDiv_12 = document.getElementById('type_anno_3');
  showDiv_12.style.display = 'none';
  showDiv_12.innerHTML = '';
 }


document.onmousemove=function(ev)
{
var oEvent=ev||Event;
var oDiv_1=document.getElementById('pair_table_detail_click');
oDiv_1.style.left=(oEvent.pageX-75)+'px';
oDiv_1.style.top=(oEvent.pageY-52)+'px';
var oDiv_2=document.getElementById('table_detail_click');
oDiv_2.style.left=(oEvent.pageX-55)+'px';
oDiv_2.style.top=(oEvent.pageY-52)+'px';
var oDiv_3=document.getElementById('node_add');
oDiv_3.style.left=(oEvent.pageX-49)+'px';
oDiv_3.style.top=(oEvent.pageY-52)+'px';
var oDiv_4=document.getElementById('edge_add');
oDiv_4.style.left=(oEvent.pageX-46)+'px';
oDiv_4.style.top=(oEvent.pageY-52)+'px';
var oDiv_5=document.getElementById('savenetwork_1');
oDiv_5.style.left=(oEvent.pageX-56)+'px';
oDiv_5.style.top=(oEvent.pageY-52)+'px';
var oDiv_6=document.getElementById('hot_gene_1');
oDiv_6.style.left=(oEvent.pageX-65)+'px';
oDiv_6.style.top=(oEvent.pageY-52)+'px';
var oDiv_7=document.getElementById('gene_info_detail');
oDiv_7.style.left=(oEvent.pageX-65)+'px';
oDiv_7.style.top=(oEvent.pageY-52)+'px';
var oDiv_8=document.getElementById('table_detail_complex_click');
oDiv_8.style.left=(oEvent.pageX-65)+'px';
oDiv_8.style.top=(oEvent.pageY-52)+'px';
var oDiv_9=document.getElementById('table_detail_pathway_click');
oDiv_9.style.left=(oEvent.pageX-65)+'px';
oDiv_9.style.top=(oEvent.pageY-52)+'px';
var oDiv_10=document.getElementById('table_detail_chemical_click');
oDiv_10.style.left=(oEvent.pageX-65)+'px';
oDiv_10.style.top=(oEvent.pageY-52)+'px';
var oDiv_11=document.getElementById('type_anno_2');
oDiv_11.style.left=(oEvent.pageX-75)+'px';
oDiv_11.style.top=(oEvent.pageY-68)+'px';
var oDiv_12=document.getElementById('type_anno_3');
oDiv_12.style.left=(oEvent.pageX-75)+'px';
oDiv_12.style.top=(oEvent.pageY-68)+'px';
};




