

var img = document.getElementById('network_results');
var cs = getComputedStyle(img);


var width = parseInt(cs.getPropertyValue('width'), 10);
var height = parseInt(cs.getPropertyValue('height'), 10);


var canvas = document.getElementById('myCanvasId');

canvas.width = width;
canvas.height = height;
